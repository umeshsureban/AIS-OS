---
name: meeting-intelligence
description: Process Fathom meetings into reviewed Google Drive packets and handle explicit APPROVE/SKIP distribution through Hermes. Use for meeting summaries, transcripts, action items, approval status, or the scheduled meeting pipeline. Do not use for ordinary calendar lookup or unsupervised email sending.
metadata:
  bike-method-phase: "1"
  three-ms-attribution: "Adapted from The Three Ms of AI™ © 2026 Nate Herk."
---

# Meeting Intelligence

Build and operate the supervised pipeline:

`Fathom → review packet in Google Drive → Hermes Telegram approval → Gmail distribution`

Phase 1 is training wheels. Never distribute meeting content or create client-facing tasks without an exact approval token from Umesh ji.

## Modes

Choose one mode from the request. If the request is ambiguous, default to `status`.

- **poll**: find new Fathom meetings, create Drive review packets, and return approval cards for Hermes to deliver.
- **approve**: distribute one pending packet after an exact `APPROVE MI-<recording_id>` instruction.
- **skip**: mark one pending packet skipped after an exact `SKIP MI-<recording_id>` instruction.
- **status**: report pending, failed, delivered, and skipped meetings without exposing transcript text.
- **dry-run**: validate connections and list meeting metadata only. Do not fetch transcript or summary content.

## Sources and destinations

- Fathom is the source for meeting metadata, summary, and transcript.
- `/opt/data/meeting-client-mapping.json` maps participant email addresses to client folders.
- Google Drive stores review packets under `Meeting Intelligence/{Client}/{YYYY-MM-DD}_{safe-title}_{recording-id}/`.
- `/opt/data/meeting-watcher-state.json` is the runtime state on Hermes.
- `/opt/data/ais-os-clone/.agents/skills/meeting-intelligence/scripts/state_tool.py` performs atomic, validated approval-state transitions on Hermes.
- Hermes cron delivery is the Telegram notification path. In a scheduled run, return the approval card as the final response; do not call a second Telegram sender.

Read [references/state-schema.md](references/state-schema.md) before changing state or handling approval.

## Poll workflow

1. Load and validate the state with `python /opt/data/ais-os-clone/.agents/skills/meeting-intelligence/scripts/state_tool.py --state /opt/data/meeting-watcher-state.json validate`.
2. Use Composio discovery to confirm active Fathom and Google Drive connections. Use the configured accounts; never place account IDs or credentials in committed files.
3. List Fathom meetings using a 48-hour overlap before `last_check`. Keep pagination filters stable and follow `next_cursor` until empty or all meetings in the overlap are collected.
4. Ignore any `recording_id` already present in `processed_ids` or `distribution`.
5. For each new meeting, fetch its Fathom summary and transcript. Do not send either to a remote workbench or unrelated processor without explicit permission.
6. Exclude Umesh ji from external recipients. Resolve the first matching participant email through the client mapping; otherwise use `Unsorted`.
7. Find or create the deterministic Drive folder containing the recording ID. Before creating each file, search that exact parent for the intended filename. Reuse an existing match instead of duplicating it.
8. Create three files: `Summary.md`, `Transcript.md`, and `Action_Items.md`. The summary must distinguish explicit decisions from inferred suggestions. Action items need owner, due date, and confidence when available; use `Unassigned` or `Not stated` rather than guessing.
9. Write a payload JSON outside the repository and call `state_tool.py prepare`. Store Drive folder/file IDs, participant names/emails, counts, and a short non-sensitive preview. Do not store the full transcript in state.
10. Return one compact approval card per meeting with Drive link, recipient list, action/open-question counts, and exact commands:
   - `APPROVE MI-<recording_id>`
   - `SKIP MI-<recording_id>`
11. Advance `last_check` only after the poll completes with the state tool's `--state /opt/data/meeting-watcher-state.json touch-check` command. Failed meetings remain unprocessed and must be retried from the overlap window.

If no new meetings exist, update `last_check` and return exactly `[SILENT]` during cron execution.

## Approval workflow

1. Require one exact token: `APPROVE MI-<recording_id>`. Bare `APPROVE` is insufficient when any meeting is pending.
2. Run `state_tool.py claim` with the token. Stop if the record is missing, terminal, already sending, or the token differs.
3. Re-read the Drive artifact metadata and show the exact recipients in the execution trace. The approval token authorizes distribution only for that stored recipient set and packet.
4. Send one Gmail message per recipient to avoid exposing participant addresses to each other. Include the reviewed summary and Drive link; do not attach the raw transcript unless explicitly requested.
5. If a client-to-ClickUp-list mapping exists, create approved action items only after duplicate checks. If no mapping exists, leave tasks in the packet and report that task creation was skipped.
6. Record provider message IDs with `state_tool.py complete`. If any send fails, call `state_tool.py fail`; never silently retry or mark delivered.

## Skip and status

- `SKIP MI-<recording_id>` calls `state_tool.py skip`. It sends nothing.
- Status mode calls `state_tool.py status` and reports counts plus recording IDs, titles, dates, and Drive links. Do not display participant emails unless Umesh ji asks.

## Safety and failure rules

- Polling and packet creation are supervised L2 work. Distribution is always L1 with explicit approval.
- Never change Fathom, Drive, Gmail, ClickUp, or Telegram connections as part of a run.
- Never infer recipients from transcript text. Use stored Fathom invitee emails only.
- Never email Umesh ji as an external participant and never send to an empty recipient set.
- Never overwrite terminal states (`delivered` or `skipped`) or reuse a completed approval token.
- Preserve raw provider errors in runtime logs but keep credentials, cursors, and transcript content out of repository files and chat summaries.
- A partial packet is `error`, not `pending_approval`. Approval is available only when all required Drive artifacts are present.

## Acceptance checks

- `python scripts/test_state_tool.py` passes.
- Dry-run confirms Fathom and Drive connectivity without reading meeting content.
- A synthetic meeting can move `pending_approval → sending → delivered` and `pending_approval → skipped`, while wrong or repeated tokens fail.
- The Hermes cron is pinned to its intended provider/model, points at the AIS-OS workdir, has this skill attached, and is paused until Umesh ji authorizes the first live-content run.
