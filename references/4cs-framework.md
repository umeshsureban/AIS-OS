# The Four Cs of an AIOS™

> *The Four Cs of an AIOS™ is a trademark of Nate Herk. © 2026 Nate Herk.*

The Four Cs framework evaluates and builds your AI Operating System architecture in dependency order:

---

## C1: Context — Knows Your Business

**Question:** Does a fresh Claude session answer "what does this business do and who works here?" without browsing?

**What it includes:**
- About you (Umesh ji)
- About your business (AITOmate Systems)
- About your clients and prospects
- About your priorities this quarter

**Where it lives:** `context/` folder

**Test:** Open a new session. Ask "What does my business do?" → should answer without reading files.

---

## C2: Connections — Reaches Your Stuff

**Question:** Can your AIOS reach live data without paste? "What's on my calendar tomorrow and what tasks are due?"

**What it includes:**
- ClickUp (tasks, projects)
- HubSpot (deals, contacts)
- Composio MCP (tools)
- X/Twitter, LinkedIn, Facebook, Instagram, YouTube (social)
- WhatsApp Business (messaging)
- Gmail (email)

**Where it lives:** `connections.md`

**Test:** Ask "What tasks are due today?" → should pull from ClickUp, not ask you to paste.

---

## C3: Capabilities — Knows How to Do the Work

**Question:** Does a short phrase trigger a multi-step workflow that produces an artifact?

**What it includes:**
- `/onboard` — setup wizard
- `/audit` — Four-Cs gap report
- `/level-up` — weekly 3Ms interview
- Custom skills as you build them

**Where it lives:** `.claude/skills/`

**Test:** Run `/audit` → should produce a gap report without further input.

---

## C4: Cadence — Runs Without Being Asked

**Question:** Laptop closed. A brief lands in the inbox. A teammate messages it and gets a real answer.

**What it includes:**
- Nightly sync cron
- Morning brief agent
- Weekly review agent
- Vault-health check agent
- End-of-session write-back loop

**Where it lives:** Hermes Agent cron jobs

**Test:** Close laptop. Tomorrow morning → Telegram brief should arrive.

---

## Dependency Graph

```
Context (C1) — Non-skippable
    ↓
Connections (C2) ← Can build in parallel
    ↓
Capabilities (C3) ← Can build in parallel
    ↓
Cadence (C4) — Last. Don't automate workflows that don't work manually.
```

---

## The Litmus Test

For any piece of information, ask: *"In a year, will it be good for me to have this memory?"*

- **Yes** → Core brain (context/, MEMORY.md)
- **No** → Fetch from original source when needed (don't store in core brain)

---

## Your Current Status (September 4, 2026)

| C | Status | Score |
|---|--------|-------|
| Context | ✅ Populated with business, clients, deals | 18/25 |
| Connections | ⚠️ Partial — ClickUp, HubSpot, Composio wired | 16/25 |
| Capabilities | ✅ /onboard, /audit, /level-up skills present | 15/25 |
| Cadence | ⚠️ 9 cron jobs active, but end-of-session write-back missing | 12/25 |
| **Total** | | **61/100** |

---

*See `references/3ms-framework.md` for the thinking framework that complements the Four Cs.*
