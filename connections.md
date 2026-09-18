# Connections

Registry of systems the AIOS can reach. A configured integration is not considered working until a safe read succeeds. Never store tokens, account IDs, cursors, or private payloads here.

Connection evidence is runtime-specific. A missing app connection in the inspected Codex Composio session does not prove that Hermes, the VPS, another Composio session, or a direct API lacks access.

| # | Domain | System and route | Status | Last successful read / limitation |
|---|---|---|---|---|
| 1 | Integration layer | Composio For You in Codex | Verified operational | Live discovery and eight read-only app checks succeeded 2026-09-18 |
| 2 | Revenue / Financials | No canonical system registered | Undocumented | No source was declared or checked as of 2026-09-18 |
| 3 | Customer interactions / CRM | HubSpot via Composio For You | Verified read-only access | Account-info read succeeded 2026-09-18; current CRM records require a scoped query |
| 4 | Calendar | Google Calendar via Composio For You | Verified read access | Calendar-list read succeeded 2026-09-18 |
| 5 | Email | Gmail via Composio For You | Verified read access | Mailbox-profile read succeeded 2026-09-18; message content was not inspected |
| 6 | Project / task tracking | ClickUp via Composio For You | Verified read access | Workspace-list read succeeded 2026-09-18; use the default account unless another is named |
| 7 | Meeting intelligence | Fathom + Google Drive via Composio; Hermes native Telegram review; Gmail distribution | Source read and Drive packet writes verified; live content run pending | Metadata-only Fathom read and Google Drive account read succeeded 2026-09-18. A synthetic Drive packet with `Summary.md`, `Transcript.md`, and `Action_Items.md` was created, verified by IDs/parent, then recoverably trashed. Hermes gateway `terminal.cwd` is `/opt/data/ais-os-clone`, so Telegram approvals load the shared skill. Live meeting-content extraction and outbound distribution remain untested pending explicit authorization. |
| 8 | Knowledge / files | Local Git checkout + GitHub `umeshsureban/AIS-OS` | Verified read access | GitHub identity read and local/VPS commit alignment verified 2026-09-18 |
| 9 | Content / social | YouTube, LinkedIn, Facebook via Composio For You | Verified read access | Channel/profile/managed-page reads succeeded 2026-09-18 |
| 10 | Content / social | X, Instagram, WhatsApp Business via Composio For You | Not active in inspected Codex session | This does not establish availability in Hermes, another Composio session, or direct integrations |

## Safe access rules

- Use Composio For You discovery before any app call. Execute only after an active connection is confirmed.
- Default to read-only identity, profile, list, or account-info checks. Sending, posting, updating, or deleting requires the user's explicit task authorization.
- Keep credentials and provider account identifiers out of this file and chat logs.
- Treat `MEMORY.md` as a summary, not proof of current external state. Query the live system when freshness matters.

## Reproducible checks

- GitHub: authenticated-user profile.
- ClickUp: authorized workspace list.
- HubSpot: account info; use a narrowly scoped CRM search for client status.
- Gmail: mailbox profile; use bounded search only for a specific user request.
- Google Calendar: calendar list, then bounded event query.
- YouTube: authenticated channel statistics.
- LinkedIn: authenticated profile only.
- Facebook: managed Pages with fields restricted to `id,name,category,link` so Page tokens are never returned.

When a missing domain is connected, record the mechanism, safe query route, successful-read date, and known limitation here. Add `references/{tool}-api.md` only when the integration needs details beyond this registry.
