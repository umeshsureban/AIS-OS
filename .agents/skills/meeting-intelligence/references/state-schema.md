# Meeting intelligence state

Runtime file: `/opt/data/meeting-watcher-state.json`

The file is private runtime state. It is not committed to AIS-OS.

## Top-level shape

```json
{
  "schema_version": 2,
  "last_check": "ISO-8601 UTC timestamp",
  "processed_ids": [183583974],
  "distribution": {
    "183583974": {}
  }
}
```

Existing top-level keys not owned by this workflow must be preserved.

## Distribution entry

Required before approval:

- `recording_id`: Fathom recording ID.
- `approval_token`: exactly `MI-<recording_id>`.
- `status`: `pending_approval`, `sending`, `send_failed`, `delivered`, or `skipped`.
- `title`, `meeting_date`, `participant_names`, `participant_emails`, `client_folder`.
- `distribution_allowed`: `true` only when at least one external invitee email is stored. Internal-only packets remain reviewable but cannot be claimed for sending.
- `drive_folder_id`, `drive_link`, and `artifact_file_ids` containing `summary`, `transcript`, and `action_items`.
- `created_at`, `updated_at`.

Optional fields include `summary_preview`, `action_item_count`, `open_question_count`, `attempt_id`, `message_ids`, `delivered_at`, `skipped_at`, and `last_error`.

## Allowed transitions

```text
missing → pending_approval
pending_approval → sending
pending_approval → skipped
send_failed → sending           # requires the same explicit token again
sending → delivered
sending → send_failed
```

`delivered` and `skipped` are terminal. `sending` cannot be claimed again automatically because an interrupted provider response may already have sent mail.

## Approval boundary

The token authorizes only the stored packet and exact stored recipient set. Any recipient or artifact change invalidates the approval: return the record to `pending_approval`, update `updated_at`, and require the token again in a new user message.
