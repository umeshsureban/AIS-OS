#!/usr/bin/env python3
"""Synthetic tests for Telegram approval-card rendering and state updates."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import send_approval_card as card


def entry() -> dict:
    return {
        "recording_id": "101",
        "approval_token": "MI-101",
        "status": "pending_approval",
        "title": "Synthetic Client Review",
        "meeting_date": "2026-09-18T10:00:00Z",
        "participant_emails": ["client@example.test"],
        "distribution_allowed": True,
        "drive_link": "https://drive.example.test/folder",
        "artifact_file_ids": {
            "summary": "summary-synthetic",
            "transcript": "transcript-synthetic",
            "action_items": "actions-synthetic",
        },
        "action_item_count": 2,
        "open_question_count": 1,
    }


def main() -> None:
    text = card.build_card(entry(), "101")
    assert "APPROVE MI-101" not in text
    assert "client@example.test" in text
    keyboard = card.reply_keyboard("101")
    assert keyboard["keyboard"][0][0]["text"] == "APPROVE MI-101"
    assert keyboard["keyboard"][0][1]["text"] == "SKIP MI-101"
    internal_keyboard = card.reply_keyboard("202", allow_approve=False)
    assert internal_keyboard["keyboard"] == [[{"text": "SKIP MI-202"}]]

    bad = entry()
    bad["status"] = "delivered"
    try:
        card.build_card(bad, "101")
        raise AssertionError("terminal meeting rendered an approval card")
    except ValueError:
        pass

    with tempfile.TemporaryDirectory() as temp_dir:
        state_path = Path(temp_dir) / "state.json"
        state_path.write_text(json.dumps({
            "schema_version": 2,
            "last_check": None,
            "processed_ids": [101],
            "distribution": {"101": entry()},
        }), encoding="utf-8")
        with patch.object(card, "resolve_chat_id", return_value="123"), \
             patch.object(card, "telegram_token", return_value="123:abcdefghijklmnopqrstuvwxyzABCDEFGHIJ"), \
             patch.object(card, "post_message", return_value="message-1"), \
             patch("sys.argv", ["send_approval_card.py", "--state", str(state_path), "--recording-id", "101"]):
            assert card.main() == 0
        saved = json.loads(state_path.read_text(encoding="utf-8"))
        assert saved["distribution"]["101"]["approval_notification"]["status"] == "sent"
        assert saved["distribution"]["101"]["approval_notification"]["message_id"] == "message-1"

    print("meeting-intelligence approval-card tests passed")


if __name__ == "__main__":
    main()
