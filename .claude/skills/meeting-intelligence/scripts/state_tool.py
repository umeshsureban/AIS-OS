#!/usr/bin/env python3
"""Atomic state transitions for the supervised meeting-intelligence workflow."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TERMINAL = {"delivered", "skipped"}
CLAIMABLE = {"pending_approval", "send_failed"}
REQUIRED_ARTIFACTS = {"summary", "transcript", "action_items"}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def default_state() -> dict[str, Any]:
    return {
        "schema_version": 2,
        "last_check": None,
        "processed_ids": [],
        "distribution": {},
    }


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return default_state()
    with path.open("r", encoding="utf-8") as handle:
        state = json.load(handle)
    if not isinstance(state, dict):
        raise ValueError("state must be a JSON object")
    state.setdefault("schema_version", 2)
    state.setdefault("last_check", None)
    state.setdefault("processed_ids", [])
    state.setdefault("distribution", {})
    if not isinstance(state["processed_ids"], list):
        raise ValueError("processed_ids must be a list")
    if not isinstance(state["distribution"], dict):
        raise ValueError("distribution must be an object")
    return state


def atomic_write(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(state, handle, indent=2, ensure_ascii=False, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def canonical_id(value: Any) -> str:
    text = str(value).strip()
    if not text or not text.isdigit():
        raise ValueError("recording_id must contain digits only")
    return text


def validate_entry(recording_id: str, entry: dict[str, Any]) -> None:
    if not isinstance(entry, dict):
        raise ValueError(f"distribution[{recording_id}] must be an object")
    status = entry.get("status")
    if status in {"pending_approval", "sending", "send_failed"}:
        if entry.get("approval_token") != f"MI-{recording_id}":
            raise ValueError(f"distribution[{recording_id}] has an invalid approval_token")
        recipients = entry.get("participant_emails")
        if not isinstance(recipients, list) or not all(isinstance(item, str) for item in recipients):
            raise ValueError(f"distribution[{recording_id}] participant_emails must be a list")
        artifacts = entry.get("artifact_file_ids")
        if not isinstance(artifacts, dict) or not REQUIRED_ARTIFACTS.issubset(artifacts):
            raise ValueError(f"distribution[{recording_id}] is missing required artifact IDs")


def validate_state(state: dict[str, Any]) -> None:
    for raw_id, entry in state["distribution"].items():
        validate_entry(canonical_id(raw_id), entry)


def payload_from(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    required = {
        "recording_id",
        "title",
        "meeting_date",
        "participant_names",
        "participant_emails",
        "client_folder",
        "drive_folder_id",
        "drive_link",
        "artifact_file_ids",
    }
    missing = sorted(required - payload.keys())
    if missing:
        raise ValueError(f"payload missing: {', '.join(missing)}")
    recording_id = canonical_id(payload["recording_id"])
    if not isinstance(payload["participant_names"], list):
        raise ValueError("participant_names must be a list")
    if not isinstance(payload["participant_emails"], list):
        raise ValueError("participant_emails must be a list")
    artifacts = payload["artifact_file_ids"]
    if not isinstance(artifacts, dict) or not REQUIRED_ARTIFACTS.issubset(artifacts):
        raise ValueError("artifact_file_ids must include summary, transcript, and action_items")
    payload["recording_id"] = recording_id
    payload["participant_emails"] = sorted({item.strip().lower() for item in payload["participant_emails"] if item.strip()})
    return payload


def command_validate(args: argparse.Namespace) -> dict[str, Any]:
    state = load_state(args.state)
    validate_state(state)
    return {"ok": True, "distribution_count": len(state["distribution"])}


def command_status(args: argparse.Namespace) -> dict[str, Any]:
    state = load_state(args.state)
    validate_state(state)
    if args.recording_id:
        recording_id = canonical_id(args.recording_id)
        entry = state["distribution"].get(recording_id)
        if not entry:
            legacy_pending = state.get("pending_delivery", {})
            legacy = legacy_pending.get(recording_id) if isinstance(legacy_pending, dict) else None
            if not isinstance(legacy, dict):
                raise ValueError(f"meeting {recording_id} not found")
            return {
                "recording_id": recording_id,
                "title": legacy.get("title"),
                "meeting_date": legacy.get("meeting_date") or legacy.get("date"),
                "status": f"legacy_{legacy.get('status', 'pending')}",
                "drive_link": legacy.get("drive_link") or (legacy.get("drive_links") or {}).get("root"),
                "recipient_count": 0,
            }
        return {
            "recording_id": recording_id,
            "title": entry.get("title"),
            "meeting_date": entry.get("meeting_date") or entry.get("date"),
            "status": entry.get("status"),
            "drive_link": entry.get("drive_link") or (entry.get("drive_links") or {}).get("root"),
            "recipient_count": len(entry.get("participant_emails") or entry.get("sent_to") or []),
        }
    counts: dict[str, int] = {}
    meetings = []
    for recording_id, entry in state["distribution"].items():
        status = entry.get("status", "unknown")
        counts[status] = counts.get(status, 0) + 1
        meetings.append({"recording_id": recording_id, "title": entry.get("title"), "status": status})
    legacy_pending = state.get("pending_delivery", {})
    if isinstance(legacy_pending, dict):
        for recording_id, entry in legacy_pending.items():
            recording_id = canonical_id(recording_id)
            if recording_id in state["distribution"]:
                continue
            raw_status = entry.get("status", "pending") if isinstance(entry, dict) else "pending"
            status = f"legacy_{raw_status}"
            counts[status] = counts.get(status, 0) + 1
            meetings.append({
                "recording_id": recording_id,
                "title": entry.get("title") if isinstance(entry, dict) else None,
                "status": status,
            })
    return {"counts": counts, "meetings": meetings}


def command_touch_check(args: argparse.Namespace) -> dict[str, Any]:
    state = load_state(args.state)
    timestamp = args.timestamp or now_utc()
    try:
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("timestamp must be ISO-8601") from exc
    state["last_check"] = timestamp
    atomic_write(args.state, state)
    return {"last_check": timestamp, "ok": True}


def command_prepare(args: argparse.Namespace) -> dict[str, Any]:
    state = load_state(args.state)
    payload = payload_from(args.payload)
    recording_id = payload["recording_id"]
    existing = state["distribution"].get(recording_id)
    if existing and existing.get("status") in TERMINAL | {"sending"}:
        raise ValueError(f"meeting {recording_id} is already {existing.get('status')}")
    created_at = (existing or {}).get("created_at", now_utc())
    entry = {
        **(existing or {}),
        **payload,
        "recording_id": recording_id,
        "approval_token": f"MI-{recording_id}",
        "approval_notification": {"status": "pending"},
        "distribution_allowed": bool(payload["participant_emails"]),
        "status": "pending_approval",
        "created_at": created_at,
        "updated_at": now_utc(),
    }
    validate_entry(recording_id, entry)
    state["schema_version"] = 2
    state["distribution"][recording_id] = entry
    legacy_pending = state.get("pending_delivery")
    if isinstance(legacy_pending, dict):
        legacy_pending.pop(recording_id, None)
    processed_value: Any = int(recording_id)
    if processed_value not in state["processed_ids"] and recording_id not in state["processed_ids"]:
        state["processed_ids"].append(processed_value)
    atomic_write(args.state, state)
    return {"recording_id": recording_id, "status": entry["status"], "approval_token": entry["approval_token"]}


def require_token(recording_id: str, entry: dict[str, Any], token: str) -> None:
    if token != f"MI-{recording_id}" or token != entry.get("approval_token"):
        raise ValueError("approval token does not match the stored meeting")


def command_claim(args: argparse.Namespace) -> dict[str, Any]:
    state = load_state(args.state)
    recording_id = canonical_id(args.recording_id)
    entry = state["distribution"].get(recording_id)
    if not entry:
        raise ValueError(f"meeting {recording_id} not found")
    require_token(recording_id, entry, args.token)
    if entry.get("status") not in CLAIMABLE:
        raise ValueError(f"meeting {recording_id} cannot be claimed from {entry.get('status')}")
    if not entry.get("distribution_allowed") or not entry.get("participant_emails"):
        raise ValueError(f"meeting {recording_id} has no external recipients")
    attempt_id = uuid.uuid4().hex
    entry.update({"status": "sending", "attempt_id": attempt_id, "attempted_at": now_utc(), "updated_at": now_utc()})
    atomic_write(args.state, state)
    return {"recording_id": recording_id, "status": "sending", "attempt_id": attempt_id, "entry": entry}


def command_complete(args: argparse.Namespace) -> dict[str, Any]:
    state = load_state(args.state)
    recording_id = canonical_id(args.recording_id)
    entry = state["distribution"].get(recording_id)
    if not entry or entry.get("status") != "sending" or entry.get("attempt_id") != args.attempt_id:
        raise ValueError("meeting is not owned by this sending attempt")
    if not args.message_id:
        raise ValueError("at least one provider message ID is required")
    entry.update({"status": "delivered", "message_ids": args.message_id, "delivered_at": now_utc(), "updated_at": now_utc()})
    atomic_write(args.state, state)
    return {"recording_id": recording_id, "status": "delivered", "message_ids": args.message_id}


def command_fail(args: argparse.Namespace) -> dict[str, Any]:
    state = load_state(args.state)
    recording_id = canonical_id(args.recording_id)
    entry = state["distribution"].get(recording_id)
    if not entry or entry.get("status") != "sending" or entry.get("attempt_id") != args.attempt_id:
        raise ValueError("meeting is not owned by this sending attempt")
    entry.update({"status": "send_failed", "last_error": args.error, "updated_at": now_utc()})
    atomic_write(args.state, state)
    return {"recording_id": recording_id, "status": "send_failed"}


def command_skip(args: argparse.Namespace) -> dict[str, Any]:
    state = load_state(args.state)
    recording_id = canonical_id(args.recording_id)
    entry = state["distribution"].get(recording_id)
    if not entry:
        raise ValueError(f"meeting {recording_id} not found")
    require_token(recording_id, entry, args.token)
    if entry.get("status") != "pending_approval":
        raise ValueError(f"meeting {recording_id} cannot be skipped from {entry.get('status')}")
    entry.update({"status": "skipped", "skipped_at": now_utc(), "updated_at": now_utc()})
    atomic_write(args.state, state)
    return {"recording_id": recording_id, "status": "skipped"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate").set_defaults(handler=command_validate)
    status = subparsers.add_parser("status")
    status.add_argument("--recording-id")
    status.set_defaults(handler=command_status)

    touch_check = subparsers.add_parser("touch-check")
    touch_check.add_argument("--timestamp")
    touch_check.set_defaults(handler=command_touch_check)

    prepare = subparsers.add_parser("prepare")
    prepare.add_argument("--payload", type=Path, required=True)
    prepare.set_defaults(handler=command_prepare)

    for name, handler in (("claim", command_claim), ("skip", command_skip)):
        command = subparsers.add_parser(name)
        command.add_argument("--recording-id", required=True)
        command.add_argument("--token", required=True)
        command.set_defaults(handler=handler)

    complete = subparsers.add_parser("complete")
    complete.add_argument("--recording-id", required=True)
    complete.add_argument("--attempt-id", required=True)
    complete.add_argument("--message-id", action="append", required=True)
    complete.set_defaults(handler=command_complete)

    fail = subparsers.add_parser("fail")
    fail.add_argument("--recording-id", required=True)
    fail.add_argument("--attempt-id", required=True)
    fail.add_argument("--error", required=True)
    fail.set_defaults(handler=command_fail)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = args.handler(args)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=os.sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
