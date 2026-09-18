#!/usr/bin/env python3
"""Send a Meeting Intelligence Telegram card with exact-command reply buttons."""

from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from state_tool import atomic_write, load_state, now_utc, validate_entry


TEST_RECORDING_ID = "000000000"


def canonical_id(value: Any) -> str:
    text = str(value).strip()
    if not text.isdigit():
        raise ValueError("recording_id must contain digits only")
    return text


def reply_keyboard(recording_id: str, *, allow_approve: bool = True) -> dict[str, Any]:
    buttons = []
    if allow_approve:
        buttons.append({"text": f"APPROVE MI-{recording_id}"})
    buttons.append({"text": f"SKIP MI-{recording_id}"})
    return {
        "keyboard": [buttons],
        "resize_keyboard": True,
        "one_time_keyboard": True,
        "selective": True,
        "input_field_placeholder": f"Review MI-{recording_id}",
    }


def build_card(entry: dict[str, Any], recording_id: str) -> str:
    if entry.get("status") != "pending_approval":
        raise ValueError(f"meeting {recording_id} is not pending approval")
    if entry.get("approval_token") != f"MI-{recording_id}":
        raise ValueError("stored approval token does not match recording ID")
    drive_link = str(entry.get("drive_link") or "").strip()
    if not drive_link.startswith("https://"):
        raise ValueError("meeting has no valid Drive link")
    recipients = [str(item) for item in (entry.get("participant_emails") or [])]
    recipient_text = ", ".join(recipients) if recipients else "Internal only — approval is disabled"
    return "\n".join([
        "🧠 Meeting Intelligence review",
        f"ID: MI-{recording_id}",
        f"Title: {entry.get('title') or 'Untitled meeting'}",
        f"Date: {entry.get('meeting_date') or 'Not stated'}",
        f"Recipients: {recipient_text}",
        f"Action items: {entry.get('action_item_count', 0)}",
        f"Open questions: {entry.get('open_question_count', 0)}",
        f"Drive packet: {drive_link}",
        "",
        "Tap one exact command below. Distribution still passes through the stored state checks.",
    ])


def resolve_chat_id(explicit: str | None) -> str:
    if explicit:
        value = explicit.strip()
    else:
        from hermes_cli.config import get_env_value

        value = str(get_env_value("TELEGRAM_HOME_CHANNEL") or "").strip()
        if not value:
            value = str(get_env_value("TELEGRAM_ALLOWED_USERS") or "").split(",", 1)[0].strip()
    match = re.search(r"-?\d+", value)
    if not match:
        raise ValueError("Telegram chat ID is not configured")
    return match.group(0)


def telegram_token() -> str:
    from hermes_cli.config import get_env_value

    token = str(get_env_value("TELEGRAM_BOT_TOKEN") or "").strip()
    if not re.fullmatch(r"\d+:[A-Za-z0-9_-]{30,}", token):
        raise ValueError("Telegram bot token is not configured")
    return token


def post_message(token: str, chat_id: str, text: str, keyboard: dict[str, Any]) -> str:
    endpoint = f"https://api.telegram.org/bot{token}/sendMessage"
    body = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "reply_markup": keyboard,
        "disable_web_page_preview": True,
    }).encode("utf-8")
    request = urllib.request.Request(endpoint, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Telegram HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Telegram network error: {exc.reason}") from exc
    if not result.get("ok"):
        raise RuntimeError(f"Telegram rejected the card: {result.get('description', 'unknown error')}")
    message_id = str((result.get("result") or {}).get("message_id") or "").strip()
    if not message_id:
        raise RuntimeError("Telegram response omitted message_id")
    return message_id


def test_card() -> tuple[str, dict[str, Any]]:
    text = "\n".join([
        "🧪 Meeting Intelligence button test",
        "Synthetic only. No meeting content or distribution is attached.",
        "The buttons below verify Telegram keyboard delivery. Do not tap them.",
    ])
    return text, reply_keyboard(TEST_RECORDING_ID)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path)
    parser.add_argument("--recording-id")
    parser.add_argument("--chat-id")
    parser.add_argument("--retry", action="store_true")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    try:
        chat_id = resolve_chat_id(args.chat_id)
        token = telegram_token()
        if args.test:
            text, keyboard = test_card()
            message_id = post_message(token, chat_id, text, keyboard)
            print(json.dumps({"ok": True, "mode": "test", "message_id": message_id}, sort_keys=True))
            return 0
        if not args.state or not args.recording_id:
            raise ValueError("--state and --recording-id are required outside test mode")
        recording_id = canonical_id(args.recording_id)
        state = load_state(args.state)
        entry = state["distribution"].get(recording_id)
        if not isinstance(entry, dict):
            raise ValueError(f"meeting {recording_id} not found")
        validate_entry(recording_id, entry)
        notice = entry.get("approval_notification") or {}
        if notice.get("status") == "sent" and not args.retry:
            raise ValueError("approval card was already sent; use --retry only after confirming it is missing")
        text = build_card(entry, recording_id)
        try:
            allow_approve = bool(entry.get("distribution_allowed") and entry.get("participant_emails"))
            message_id = post_message(
                token,
                chat_id,
                text,
                reply_keyboard(recording_id, allow_approve=allow_approve),
            )
        except Exception as exc:
            entry["approval_notification"] = {
                "status": "failed",
                "failed_at": now_utc(),
                "error": str(exc),
            }
            entry["updated_at"] = now_utc()
            atomic_write(args.state, state)
            raise
        entry["approval_notification"] = {
            "status": "sent",
            "sent_at": now_utc(),
            "message_id": message_id,
        }
        entry["updated_at"] = now_utc()
        atomic_write(args.state, state)
        print(json.dumps({"ok": True, "recording_id": recording_id, "message_id": message_id}, sort_keys=True))
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=__import__("sys").stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
