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
