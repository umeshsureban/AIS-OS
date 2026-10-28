# Connections

Registry of systems the AIOS can reach. A configured integration is not considered working until a safe read succeeds. Never store tokens, account IDs, cursors, or private payloads here.

Connection evidence is runtime-specific. A missing app connection in one Composio session does not prove that Hermes, the VPS, another session, or a direct API lacks access.

Last full refresh: 2026-10-28 (reads via Composio in Claude Code, plus the Hermes meeting job run on the VPS).

| # | Domain | System and route | Status | Refresh interval | Last successful read / limitation |
|---|---|---|---|---|---|
| 1 | Integration layer | Composio (connections list and tool discovery) | Verified operational | 30 days | Discovery and eight app reads succeeded 2026-10-28 |
| 2 | Revenue / Financials | Not connected, by decision (2026-10-29) | No source needed now | Review when payments move to an invoicing or accounting tool, otherwise at each quarterly review | Payments are cash or UPI and are recorded per client in `MEMORY.md` and `projects/`. There is no bank, accounting, or payment API. `MEMORY.md` is a hand-kept summary, not a ledger. A GST filing reminder exists as a Hermes cron; no filing data source is registered. |
| 3 | Customer interactions / CRM | HubSpot via Composio | Verified; use read-only | 30 days | Granted-scopes read succeeded 2026-10-28 (token excluded). The token also carries write scopes (contacts, companies, deals, users). Treat it as read-only unless a task authorizes writes (AIOS-20261028-06). Current CRM stage for deals is unverified; use a scoped query. |
| 4 | Calendar | Google Calendar via Composio | Verified read access | 30 days | Calendar-list read succeeded 2026-10-28 (first page of calendars returned) |
| 5 | Email | Gmail via Composio | Verified read access | 30 days | Mailbox-profile read succeeded 2026-10-28. The connected mailbox is the Maya business account, not Umesh ji's personal one. Message content was not inspected. |
| 6 | Project / task tracking | ClickUp via Composio | Verified read access | 30 days | Workspace-list read succeeded 2026-10-28; use the default account unless another is named |
| 7 | Meeting intelligence | Fathom + Google Drive via Composio; Hermes cron `meeting-intelligence-pipeline`; Telegram reply-keyboard review; Gmail distribution | Connections and job verified; live meeting content still untested | 7 days (the job polls daily, so each run is a read) | The job, pinned to the Claude subscription provider, completed on 2026-10-28 (18:50, 19:03, 19:30 UTC; the 18:59 run confirmed Fathom and Drive active) and returned `[SILENT]` because there were no new meetings. State validates. A synthetic Drive packet and a synthetic Telegram card with exact-command buttons were verified on 2026-09-18. Real meeting extraction, a live approval card, and outbound email are untested. |
| 8 | Knowledge / files | Local Git checkout + GitHub `umeshsureban/AIS-OS` | Verified read access | 30 days | GitHub identity read succeeded 2026-10-28. Local `main` and origin were aligned on 2026-10-28; the VPS pulls at its next sync. |
| 9 | Content / social | YouTube, LinkedIn, Facebook via Composio | Verified read access | 30 days | Channel statistics, profile, and managed-Page reads succeeded 2026-10-28 (one Page). Facebook reads use restricted fields so Page tokens are never returned. |
| 10 | Content / social | X, Instagram, WhatsApp Business | Not connected in Composio (connections list, 2026-10-28) | Re-check when a task needs one, otherwise every 90 days | Instagram posting failed earlier through Composio (S3 staging URLs, see `MEMORY.md` lessons). |

## Refresh policy

- A domain counts as **fresh** when its last successful read is inside the interval above. Past the interval, run its reproducible check below and update the date here. A stale row is not proof of a broken connection, only of unverified access.
- Volatile records (CRM stage, tasks, calendar events) must be queried live when the answer matters. The date here only says the route worked.
- The weekly review and `/audit` are the places to check these dates. Do not edit a date without a successful read.
- Failures should be reported, not hidden: an expired or failing connection must be written in the Status column with the date and error, not replaced by an old success.

## Safe access rules

- Use Composio discovery before any app call. Execute only after an active connection is confirmed.
- Default to read-only identity, profile, list, or account-info checks. Sending, posting, updating, or deleting requires the user's explicit task authorization.
- Keep credentials and provider account identifiers out of this file and chat logs.
- Treat `MEMORY.md` as a summary, not proof of current external state. Query the live system when freshness matters.

## Reproducible checks

- GitHub: authenticated-user profile.
- ClickUp: authorized workspace list.
- HubSpot: granted scopes with the token excluded (or account info); use a narrowly scoped CRM search for client status.
- Gmail: mailbox profile; use bounded search only for a specific user request.
- Google Calendar: calendar list (small page), then bounded event query.
- YouTube: authenticated channel statistics (`mine`).
- LinkedIn: authenticated profile only.
- Facebook: managed Pages with fields restricted to `id,name,category,link` so Page tokens are never returned.
- Meeting intelligence: `hermes cron list` and `hermes cron runs <job>` on the VPS, then `state_tool.py validate`. A run that returns `[SILENT]` with status `ok` proves the Fathom and Drive routes, not meeting content.

When a missing domain is connected, record the mechanism, safe query route, refresh interval, successful-read date, and known limitation here. Add `references/{tool}-api.md` only when the integration needs details beyond this registry.
