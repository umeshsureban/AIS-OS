# Decisions Log

Append-only record of meaningful decisions and why they were made. `/level-up` Phase 2 (Method interview) writes scoped automation specs here. You can also append manually whenever you decide something worth remembering.

**Format per entry:**

```
## YYYY-MM-DD — Short title

**Decision:** what was decided.

**Why:** the reasoning, constraints, and what would change your mind.

**Alternatives considered:** what else was on the table.

**Owner:** who's accountable.
```

Keep it terse. Future-you will thank present-you for capturing the *why*, not just the *what*.

---

## 2026-09-06 - Audit evidence and routing maintenance

**Decision:** Ship audit rubric v2 and a small /link skill. Audit scores working evidence across the Four Cs, checks operating-manual routing and freshness, and passes one concrete gap into /level-up. A selected repair can improve an existing workflow instead of creating another skill.

**Why:** File counts, configured keys, named rituals, and recent edits do not prove an operational AIOS. Source findability and freshness need explicit checks.

**Alternatives considered:** Keeping presence-based scoring or requiring a hot cache. Neither reliably establishes retrieval quality or successful execution.

## 2026-09-06 - Portable skills and automatic audit history

**Decision:** Ship all four skills for Claude Code and Codex, with bundled resources, matching operating manuals, and a script for regenerating Codex copies. Audit reports are saved automatically, preserve previous runs, and track findings across comparable inspections.

**Why:** Students need the same shared guidance when switching assistants and evidence of actual improvements over time. Intentional runtime adaptations, unknown verification, and confirmed defects are reported separately.

## 2026-09-06 - Portable 3D Brain skill

**Decision:** Add `/3d-brain` for Claude Code and Codex. Ask for a name and categories, map selected local folders, and scaffold a bundled, configurable application with spherical placement, Cinema, and interactive growth replay.

**Why:** Shipping the working renderer preserves the intended appearance and interactions across AIOS installations. A prose-only prompt would produce inconsistent recreations. User config and graph data remain local; the public package includes only code, documentation, dependency notices, and fictional test inputs.

## 2026-09-06 - Add ongoing context interviews

**Decision:** Adapt Herk-2's grill-me skill for the student kit and ship matching Claude/Codex packages. Save every answer to brainstorms/, preserve resumable Q&A history, and update canonical context only with confirmed facts during requested context-building sessions.

**Why:** Onboarding is an initial snapshot. Ongoing interviews capture changing priorities, decisions, and preferences while keeping tentative ideas distinct from current business facts.

## 2026-09-06 — Client Closures + SeedWise Payment

**Decision:** Closed VNA (Sravan), SoloWarrior (Parijat), and Alan (Mark Industries). Recorded SeedWise 2nd payment of ₹50K cash via Praveen Mudhol.

**Why:** User instructed to close these clients. SeedWise payment received in cash, updating from "Payment Pending" to "Active".

**Alternatives considered:** None — user directive.

**Owner:** Umesh

## 2026-09-17
- [Action]: Repaired Hermes job `nightly-hermes-vps-sync` (`830f2997467c`) by pinning it to `openai-codex` / `gpt-6-astra`; manual verification completed successfully and the VPS repository is clean and aligned with `origin/main`.
- [Lesson]: Hermes drift protection skips unpinned cron jobs after the global inference provider or model changes; pin each intended job explicitly after a model migration.
- [Decision]: Supersede the temporary Astra pin and prohibit Astra for Hermes scheduled jobs. Assign 6 lightweight jobs to GPT-5.6 Luna, 9 business workflow jobs to GPT-5.6 Terra, and the meeting-intelligence pipeline to GPT-5.6 Sol.
- [Why]: Scheduled work should use the lowest-cost model tier that reliably matches its complexity; explicit pins also prevent drift protection from skipping jobs after global model changes.

## 2026-09-18 — Shared-brain authority repair

**Decision:** Use one deterministic authority ladder across Claude, Codex, and Hermes: live systems for external records, `MEMORY.md` for the current cross-tool summary, project pages for detail, the decision log for rationale, and context pages for stable facts. Remove volatile status copies from routing files.

**Why:** The same Git vault was synchronized, but duplicated deal and scheduler facts could still produce different answers. Elimination is the right first step: remove duplicate state instead of automating another synchronization layer.

**Process:** Audit finding triggers the repair; canonical files supply current truth; routing, context, index, and connection files are reconciled; deterministic checks compare manuals, resolve paths, scan duplicate headings, and sample current facts; the updated vault is the destination.

**Autonomy:** L1, human-reviewed repair. Repository files may be committed and synchronized; no client-facing app writes, sends, posts, or account changes.

**KPI:** Cut sampled cross-runtime current-state conflicts from two confirmed conflicts to zero and make every declared concrete route resolve. Bucket: lower operating cost through fewer wrong-answer corrections.

**Alternatives considered:** Keep multiple summaries synchronized or add another cache. Rejected because volatile duplicates create maintenance work and source ambiguity.

**Framework:** Adapted from The Three Ms of AI™ © 2026 Nate Herk.

## 2026-09-18 — Supervised meeting intelligence

**Decision:** Build Bike Phase 1 as one shared `/meeting-intelligence` skill. Poll Fathom with a 48-hour overlap, deduplicate by recording ID, create a complete packet in Google Drive, and ask for Telegram review. Distribution requires the exact token `APPROVE MI-<recording_id>`; `SKIP MI-<recording_id>` closes a packet without sending.

**Why:** Meeting notes and actions need a reliable path without risking unreviewed client communication. Eliminate duplicate scripts and senders, automate packet preparation, and keep client-facing distribution at human-approved L1 autonomy. Internal-only meetings may create packets but cannot be distributed.

**Method:** Trigger: pinned Hermes cron. Data: Fathom meeting metadata, summary, transcript, invitees, and client mapping. Transform: normalized summary, transcript, action items, open questions, and recipient preview. Decision: exact approval or skip token. Destination: Google Drive packet, Telegram review card, then one Gmail message per stored external invitee; ClickUp is optional only when a mapping exists.

**KPI:** Packet ready within 15 minutes of a completed meeting, zero missed action items in reviewed packets, and zero unapproved distributions.

**Alternatives considered:** Fully automatic distribution or a second Telegram sender. Rejected because they increase communication risk and duplicate the Hermes delivery channel.

**Owner:** Umesh

**Framework:** Adapted from The Three Ms of AI™ © 2026 Nate Herk.

## 2026-10-28 — Verify Hermes skill inventory on the VPS

**Decision:** Close audit gap AIOS-20260918-03 as a read-only verification, using a prompt-only runbook at `references/hermes-vps-skill-check.md`. Result: 7/7 skills on disk in the Hermes container, 0/7 in `hermes skills list --source local --enabled-only`, and `link` loads in a fresh oneshot session when given its explicit path. Discovery by name is unproven, so the gap is narrowed, not closed.

**Why:** `.hermes.md` implied all seven skills work in Hermes, but only meeting-intelligence had production evidence. Eliminate was not possible (the claim needs evidence). Automate: about 90% is a deterministic list-and-diff with no AI step. Manual: SSH approval and judging mismatches.

**Method:** Trigger: manual, after any skill change. Data: VPS `.agents/skills`, Hermes inventory, local skill folders. Transform: diff three name lists. Decision: 7/7 pass, otherwise finding. Destination: this log and the runbook.

**Autonomy:** L1. Read-only SSH and one oneshot read; no trust, install, or config change.

**KPI:** Bucket: cut costs (fewer wrong-answer corrections). Skills with direct VPS evidence went from 1/7 to 7/7 on disk and 7/7 loadable by path. Inventory registration is still 0/7.

**Alternatives considered:** Running `hermes skills trust` to force registration. Deferred; it changes VPS config and needs explicit approval.

**Owner:** Umesh

**Framework:** Adapted from The Three Ms of AI™ © 2026 Nate Herk.

## 2026-10-29 — Re-pin meeting-intelligence-pipeline off unsupported Sol

**Decision:** Move Hermes job `72e7debe2186` (`meeting-intelligence-pipeline`) from `gpt-5.6-sol` to `gpt-5.6-terra` on `openai-codex`, reasoning effort unchanged (medium), explicitly pinned. This supersedes the 2026-09-17 assignment of Sol to this job. Previous settings for rollback: model `gpt-5.6-sol`, provider `openai-codex`, medium.

**Why:** Audit finding AIOS-20261028-01. The job failed 3 times in a row (last 2026-10-28T18:00Z) with HTTP 400: Sol is not supported with Codex on a ChatGPT account. Every other job on the same provider runs on Luna or Terra and completes on time, so Terra is the nearest supported tier. Eliminate was not possible: the pipeline is the only supervised path for meeting packets.

**Method:** Trigger: existing Hermes cron schedule, unchanged. Data: Fathom metadata and transcript, client mapping. Transform: packet, action items, recipient preview. Decision: exact `APPROVE`/`SKIP MI-<recording_id>` token. Destination: Google Drive packet, Telegram review card. Only the model pin changes.

**Autonomy:** L1, unchanged. No distribution without an exact approval token. The repair edits one VPS job's model setting and nothing else.

**KPI:** Bucket: lower cost (fewer missed meetings and manual follow-ups). Metric: consecutive failures of this job, from 3 to 0 on the next due run, then packet ready within 15 minutes of a completed meeting (original KPI).

**Alternatives considered:** Switch the account or provider to make Sol work (larger change, unverified). Run the job forcibly to test (side effects in Drive and Telegram, and the request was to confirm a due run).

**Owner:** Umesh

**Framework:** Adapted from The Three Ms of AI™ © 2026 Nate Herk.

## 2026-10-29 — Meeting pipeline moves to Claude Sonnet 5.5 (supersedes Terra pin)

**Decision:** Re-pin Hermes job `72e7debe2186` (`meeting-intelligence-pipeline`) from `gpt-5.6-terra` / `openai-codex` (set earlier today) to `claude-sonnet-5-5` on the `anthropic` provider, reasoning effort unchanged (medium), explicitly pinned. Rollback options: `gpt-5.6-terra` on `openai-codex`, or the original `gpt-5.6-sol` (rejected by the ChatGPT-account Codex route).

**Why:** Umesh asked for a supported Claude model. Audit finding AIOS-20261028-01 (3 consecutive failures on Sol). The `anthropic` provider has a pooled API key, and a one-turn test call to `claude-sonnet-5-5` returned correctly from the Hermes container. OpenRouter was not used: its key is exhausted (402). The default `claude-subscription-directsdk-experimental` route was not used: Claude Code is not installed on the VPS.

**Method:** Unchanged from the 2026-10-29 entry above: same schedule, data sources, approval-token gate, and Drive and Telegram destinations. Only the model and provider pin change.

**Autonomy:** L1, unchanged. No client distribution without an exact approval token.

**KPI:** Bucket: lower cost (fewer missed meetings). Metric: consecutive failures from 3 to 0 on the next due run (2026-10-29 18:00 UTC). Watch API spend: this job now bills per token on the Anthropic key instead of the ChatGPT-account route.

**Policy note:** This departs from the 2026-09-17 tier policy (Sol for this job). The tier policy line in `MEMORY.md` still names Sol and needs a manual update.

**Alternatives considered:** Terra on `openai-codex` (works, already applied before this request). OpenRouter Claude (exhausted credit).

**Owner:** Umesh

**Framework:** Adapted from The Three Ms of AI™ © 2026 Nate Herk.

## 2026-10-29 — Meeting pipeline moves to Claude subscription (supersedes API pin)

**Decision:** Re-pin Hermes job `72e7debe2186` (`meeting-intelligence-pipeline`) from `claude-sonnet-5-5` on the `anthropic` API provider to model `sonnet` on `claude-subscription-directsdk-experimental`, reasoning effort unchanged (medium), pinned. Rollback options: `gpt-5.6-terra` on `openai-codex` (no API), or the API pin.

**Why:** Umesh does not want per-token API billing for this job. Claude Code is already installed and logged in with the claude.ai account inside the Hermes container (`CLAUDE_SUBSCRIPTION_DIRECTSDK_COMMAND` in `/opt/data/.env` points to a working 2.1.310 binary; a second 2.1.312 copy was also installed at `/opt/data/tools/claude-code` and is redundant). A one-turn test through the subscription provider returned correctly. This also removes the 3-failure Sol error (AIOS-20261028-01) pending the next due run.

**Method / Autonomy:** Unchanged. Same schedule, sources, approval-token gate (L1), Drive and Telegram destinations.

**KPI:** Consecutive failures of this job from 3 to 0 on the next due run (2026-10-29 18:00 UTC), with zero API spend for this job.

**Risk:** The provider is marked experimental. If the run fails, roll back to Terra on `openai-codex`.

**Owner:** Umesh

**Framework:** Adapted from The Three Ms of AI™ © 2026 Nate Herk.

## 2026-10-29 — Meeting pipeline job routed through the meeting-intelligence skill

**Decision:** Replace the saved prompt of Hermes job `72e7debe2186` with a short poll-mode prompt that reads `.agents/skills/meeting-intelligence/SKILL.md` by path and follows it, and set the job workdir to `/opt/data/ais-os-clone`. The skill is referenced by path, not attached by name, because Hermes does not list repo skills (AIOS-20260918-03). The previous prompt was a legacy flow with a loose "Reply APPROVE" token and its own state handling; its full saved config is backed up locally in the session scratchpad and the old text is in the prior job config.

**Why:** The legacy prompt contradicted the 2026-09-18 decision (exact `APPROVE MI-<recording_id>` token, state validated by `state_tool.py`). The job also lacked the skill and workdir the skill's own acceptance checks require.

**State migration:** The new flow's validator rejected `/opt/data/meeting-watcher-state.json` because 7 legacy `pending_approval` records (Sep 15 to Oct 17, all client folder Unsorted, no stored recipients, nothing ever sent) had no valid approval tokens. With Umesh's approval, all 7 were marked `skipped` with a reason and timestamp; nothing else changed. Backup: `/opt/data/meeting-watcher-state.json.bak-20261028-legacy-migration`. State now validates.

**Test results (2026-10-28):** Test 1 failed safely at validation (nothing created or sent). Test 2, after migration: connections active, state valid, no new Fathom meetings; the agent declined to rebuild 2 legacy-queue meetings (175849733, 180318188, internal-only, no external invitee) and the run was recorded as failed. Still open: decide whether to skip or rebuild those 2.

**Autonomy:** L1 for distribution, unchanged. No emails, tasks, or client-facing sends occurred.

**KPI:** Job run status: `ok` on a nightly run with the skill prompt; zero loose-token approvals possible.

**Owner:** Umesh

**Framework:** Adapted from The Three Ms of AI™ © 2026 Nate Herk.

## 2026-10-29 — Legacy-queue meetings skipped; skill-based pipeline run passes

**Decision:** With Umesh's approval, moved the last 2 legacy `pending_delivery` meetings (175849733, 180318188; internal-only, never sent) into `distribution` as `skipped` with a reason and cleared the legacy queue. Backup: `/opt/data/meeting-watcher-state.json.bak-20261028-legacy-queue`. State validates (11 records: 1 delivered, 10 skipped).

**Result:** Test run at 2026-10-28T19:03Z on the skill-based prompt, Claude subscription provider, completed with `[SILENT]` (no new meetings) and the job shows `ok`. This closes the model failure behind AIOS-20261028-01 and the stale-prompt gap. Still unproven: a run with a real new meeting (Drive packet, Telegram card, exact-token approval), and tonight's scheduled 18:00 UTC run.

**Framework:** Adapted from The Three Ms of AI™ © 2026 Nate Herk.

## 2026-10-29 — Reconcile local checkout with the rebuilt origin history

**Decision:** Move local `main` onto `origin/main` (`cf2d3c2`), which was rebuilt as a new history on 2026-09-24 ("restore corrupted repo") and shares no ancestor with the old local history. The old 42 commits are kept on local branch `backup/pre-rebuild-2026-10-28` (tip `df839ef`). Local-only work was preserved: today's `decisions/log.md` entries (appended unchanged), the `references/hermes-vps-skill-check.md` runbook, and the Business Email Infrastructure section, merged into origin's current `MEMORY.md`. One stale line in `MEMORY.md` was updated: the meeting-intelligence pipeline now runs on the Claude subscription provider, not Sol. A whitespace-only line-ending change in `references/3ms-framework.md` was dropped (content identical).

**Why:** Audit finding AIOS-20261028-02. Local sessions read a 40-day-old `MEMORY.md` (Anand shown at 80% instead of Dead). Eliminate was not possible; the fix is a one-time deterministic reconcile. A merge would have been meaningless with no common ancestor, and tree comparison showed origin's content matched the old local tree except `MEMORY.md`, 5 weekly reviews, 3 project files and one raw file.

**Process:** Trigger: audit finding. Data: `git fetch`, tree diff, backups. Transform: branch, stash, checkout, manual merge of three files. Decision: push only with explicit approval. Destination: local main, then origin if approved.

**Autonomy:** L1. No force push, no history rewrite on origin. Backups: branch above, git stash `pre-reconcile 2026-10-29`, and copies in the session scratchpad.

**KPI:** Local `HEAD` equals origin; the sampled current-state probe (Anand's status) agrees across local and VPS memory; local-only content survives. Bucket: lower cost (fewer wrong-answer corrections).

**Finding:** origin tracks 34 loose objects under `.git.broken/`, re-added after the 2026-09-24 removal. Not changed here; noted for a separate cleanup.

**Owner:** Umesh

**Framework:** Adapted from The Three Ms of AI™ © 2026 Nate Herk.

## 2026-10-29 — Align stale client stages with MEMORY.md

**Decision:** Treat `MEMORY.md` as the single source for deal and client stage and align the downstream copies to it: `context/clients.md` (Anand now Dead, Kumaraswamy "CRM stage unverified", SeedWise current delivery), `projects/anand-hiremath.md` (Dead, no next actions, history kept), `projects/aitomate-systems.md` (Kumaraswamy). The hard-coded client and lead list in the Knowledge base section of `AGENTS.md` and `CLAUDE.md` was replaced by a pointer to `MEMORY.md`, `projects/` and `context/clients.md`. The two "older stage" reconciliation notes in `MEMORY.md` were updated to say the pages were aligned. `projects/kumaraswamy.md` already matched and was not changed.

**Why:** Audit finding AIOS-20260917-01. Three of five changing-fact probes agreed; Anand (Dead vs 80%) and Kumaraswamy (unverified vs Appointment Scheduled 20%) disagreed across files, and the manuals broke their own no-volatile-status rule. Eliminate first: removing the copy from the manuals beats keeping it in sync.

**Process:** Trigger: audit finding. Data: `MEMORY.md` (2026-10-28 consolidation) and the git history of the Dead write-back (2026-09-24). Transform: manual edits to six files, no new facts invented. Decision: `MEMORY.md` wins on conflict. Destination: vault files, then origin.

**Autonomy:** L1, human-requested repair; no client-facing action. Contact details (emails, phones) were left as they were.

**KPI:** Bucket: lower cost (fewer wrong-answer corrections). Metric: changing-fact probes that agree across files, from 3 of 5 to 5 of 5.

**Open:** The live CRM stage for both deals is still unverified; `MEMORY.md` says so. Kumaraswamy's 2026-10-03 review outcome is not recorded.

**Owner:** Umesh

**Framework:** Adapted from The Three Ms of AI™ © 2026 Nate Herk.
