#!/usr/bin/env python3
"""Behavioral tests for state_tool.py using only synthetic data."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).with_name("state_tool.py")


def run(*args: str, expect: int = 0) -> dict:
    result = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)
    if result.returncode != expect:
        raise AssertionError(f"expected {expect}, got {result.returncode}: {result.stderr or result.stdout}")
    stream = result.stdout if expect == 0 else result.stderr
    return json.loads(stream)


def payload(recording_id: int) -> dict:
    return {
        "recording_id": recording_id,
        "title": "Synthetic Client Review",
        "meeting_date": "2026-09-18T10:00:00Z",
        "participant_names": ["Example Client"],
        "participant_emails": ["client@example.test"],
        "client_folder": "Example_Client",
        "drive_folder_id": "folder-synthetic",
        "drive_link": "https://drive.example.test/folder-synthetic",
        "artifact_file_ids": {
            "summary": "summary-synthetic",
            "transcript": "transcript-synthetic",
            "action_items": "actions-synthetic",
        },
        "action_item_count": 2,
        "open_question_count": 1,
    }


def main() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        state = root / "state.json"
        first_payload = root / "meeting-101.json"
        first_payload.write_text(json.dumps(payload(101)), encoding="utf-8")

        prepared = run("--state", str(state), "prepare", "--payload", str(first_payload))
        assert prepared == {"approval_token": "MI-101", "recording_id": "101", "status": "pending_approval"}
        run("--state", str(state), "claim", "--recording-id", "101", "--token", "wrong", expect=2)
        claimed = run("--state", str(state), "claim", "--recording-id", "101", "--token", "MI-101")
        assert claimed["status"] == "sending" and claimed["attempt_id"]
        run("--state", str(state), "claim", "--recording-id", "101", "--token", "MI-101", expect=2)
        completed = run(
            "--state", str(state), "complete", "--recording-id", "101",
            "--attempt-id", claimed["attempt_id"], "--message-id", "msg-synthetic",
        )
        assert completed["status"] == "delivered"
        run("--state", str(state), "skip", "--recording-id", "101", "--token", "MI-101", expect=2)

        second_payload = root / "meeting-202.json"
        second_payload.write_text(json.dumps(payload(202)), encoding="utf-8")
        run("--state", str(state), "prepare", "--payload", str(second_payload))
        skipped = run("--state", str(state), "skip", "--recording-id", "202", "--token", "MI-202")
        assert skipped["status"] == "skipped"

        internal_payload = root / "meeting-303.json"
        internal_data = payload(303)
        internal_data["participant_names"] = []
        internal_data["participant_emails"] = []
        internal_payload.write_text(json.dumps(internal_data), encoding="utf-8")
        prepared_internal = run("--state", str(state), "prepare", "--payload", str(internal_payload))
        assert prepared_internal["status"] == "pending_approval"
        run("--state", str(state), "claim", "--recording-id", "303", "--token", "MI-303", expect=2)

        legacy_state = json.loads(state.read_text(encoding="utf-8"))
        legacy_state["pending_delivery"] = {
            "404": {"title": "Legacy Synthetic Meeting", "status": "awaiting_telegram_connection"}
        }
        state.write_text(json.dumps(legacy_state), encoding="utf-8")
        legacy_status = run("--state", str(state), "status")
        assert legacy_status["counts"]["legacy_awaiting_telegram_connection"] == 1

        legacy_payload = root / "meeting-404.json"
        legacy_payload.write_text(json.dumps(payload(404)), encoding="utf-8")
        run("--state", str(state), "prepare", "--payload", str(legacy_payload))
        migrated_state = json.loads(state.read_text(encoding="utf-8"))
        assert "404" not in migrated_state["pending_delivery"]

        validated = run("--state", str(state), "validate")
        assert validated == {"distribution_count": 4, "ok": True}
        status = run("--state", str(state), "status")
        assert status["counts"] == {"delivered": 1, "pending_approval": 2, "skipped": 1}
        touched = run("--state", str(state), "touch-check", "--timestamp", "2026-09-18T12:00:00Z")
        assert touched == {"last_check": "2026-09-18T12:00:00Z", "ok": True}
        run("--state", str(state), "touch-check", "--timestamp", "not-a-time", expect=2)

    print("meeting-intelligence state tests passed")


if __name__ == "__main__":
    main()
