---
bike-method-phase: 1  # Phase 1 — Training wheels. Run manually first.
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
---

# Hermes VPS skill check (prompt-only runbook)

Purpose: confirm the seven AIOS skills are present and usable by Hermes on the VPS. Read-only. Run by hand, review every output.

Rules:
- Read-only commands only. No `hermes skills trust`, install, or config change without explicit approval.
- Use the IP, not the hostname: the pinned host key is stored under `72.60.103.200`. Never disable host key checking.
- The repo lives inside the Hermes container, not on the VPS host.

## Targets

- SSH: `root@72.60.103.200` with `~/.ssh/hermes_vps`
- Container: `hermes-workspace-5hqv-hermes-agent-1`
- Repo dir in container: `/opt/data/ais-os-clone`
- Expected skills (7): 3d-brain, audit, grill-me, level-up, link, meeting-intelligence, onboard

## Step 1 — On disk

```
ssh -i ~/.ssh/hermes_vps -o BatchMode=yes root@72.60.103.200 \
  'docker exec -w /opt/data/ais-os-clone hermes-workspace-5hqv-hermes-agent-1 ls .agents/skills'
```
Pass: all 7 names listed. Compare with local `.claude/skills` and `.agents/skills`.

## Step 2 — In the Hermes inventory

```
... sh -c "hermes skills list --source local --enabled-only" | grep -E "│ (3d-brain|audit|grill-me|level-up|link|meeting-intelligence|onboard) "
```
Pass: 7 rows. Empty output means repo skills are not registered in the inventory.

## Step 3 — Fresh-session load (one non-meeting skill)

```
... sh -c "hermes chat --oneshot --max-turns 4 --run-budget 120 -q '<read-only prompt naming .agents/skills/link/SKILL.md>'"
```
Pass: Hermes returns the skill's frontmatter name and first step. Note: naming the path proves file access, not discovery by name.

## Last run: 2026-10-28

| Step | Result |
|---|---|
| 1 On disk | Pass, 7/7 present |
| 2 Inventory | Fail, 0/7 listed (45 older skills listed) |
| 3 Load `link` | Pass by explicit path, 12s, 2 tool calls, nothing modified |

Open question: does Hermes discover repo skills by name (for example when a user says `/link`) without the path? Test with `hermes chat -s link` or an unprompted request, then decide whether trusting or registering the project is worth it. Needs explicit approval.
