# Brain Vault — Complete Implementation Guide

**Date:** September 5, 2026  
**Author:** Maya (Hermes Agent) for Umesh ji  
**Version:** 1.0  
**Repo:** github.com/umeshsureban/AIS-OS

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Architecture Overview](#architecture-overview)
3. [Implementation Phases](#implementation-phases)
4. [File Structure](#file-structure)
5. [Tool Configurations](#tool-configurations)
6. [Cron Jobs](#cron-jobs)
7. [Dashboard Setup](#dashboard-setup)
8. [Maintenance](#maintenance)
9. [Troubleshooting](#troubleshooting)

---

## Executive Summary

Brain Vault is a **centralized memory system** for AITOmate Systems that allows three AI tools (Hermes Agent, Claude Code, Codex) to share one source of truth. All content lives as plain markdown files in a Git-backed vault, ensuring no vendor lock-in and full portability.

### Key Features

- **Multi-tool memory**: Hermes, Claude Code, and Codex all read/write the same vault
- **Visual dashboard**: Obsidian graph view + web dashboard at brain.aitomate.cloud
- **Version-controlled**: All changes tracked via GitHub
- **Auto-sync**: Nightly sync cron + end-of-session write-back
- **Framework-driven**: Nate Herk's 3Ms + 4Cs frameworks built-in

### What's Live

| Component | URL/Path |
|-----------|----------|
| GitHub Repo | github.com/umeshsureban/AIS-OS |
| Dashboard | brain.aitomate.cloud |
| Vault Path | /opt/data/ais-os-clone |

---

## Architecture Overview

### High-Level Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    OBSIDIAN (Laptop)                     │
│              Open AIS-OS folder as vault                 │
│              Graph View = built-in dashboard             │
└─────────────────────────────────────────────────────────┘
                            │
                            │ Git Sync
                            ▼
┌─────────────────────────────────────────────────────────┐
│              BRAIN VAULT (GitHub)                        │
│                                                         │
│  CLAUDE.md ← Claude Code reads this                   │
│  AGENTS.md ← Codex reads this (identical copy)        │
│  MEMORY.md ← All tools share this                     │
│  SOUL.md   ← Hermes personality                       │
│                                                         │
│  context/        ← About you, business, clients        │
│  references/     ← 3Ms framework, 4Cs framework       │
│  decisions/      ← Append-only decision log            │
│  projects/       ← VNA, Alan, Jaguar Villa, etc.       │
│  connections.md  ← Registry of connected systems       │
│                                                         │
│  .claude/skills/ ← /onboard, /audit, /level-up         │
└─────────────────────────────────────────────────────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │  Hermes  │  │ Claude   │  │  Codex   │
        │  Agent   │  │  Code    │  │          │
        │ (always- │  │ (on-     │  │ (on-     │
        │  on VPS) │  │  demand) │  │  demand) │
        └──────────┘  └──────────┘  └──────────┘
```

### Tool Roles

| Tool | Role | When Active |
|------|------|-------------|
| **Hermes Agent** | Always-on runtime, cron jobs, messaging | 24/7 on VPS |
| **Claude Code** | Coding, building, complex reasoning | On-demand |
| **Codex** | Terminal coding tasks | On-demand |
| **Obsidian** | Visual dashboard, graph view, knowledge browsing | On laptop |

---

## Implementation Phases

### Phase 1: Clone & Setup (Day 1) — COMPLETED

| Step | Task | Status |
|------|------|--------|
| 1.1 | Clone AIS-OS repo | ✅ Done |
| 1.2 | Configure brain.yaml | ✅ Done |
| 1.3 | Set up raw/ folder | ✅ Done |
| 1.4 | Set up wiki/ folder | ✅ Done |
| 1.5 | Push to GitHub | ✅ Done |

### Phase 2: Migrate Content (Day 1-2) — COMPLETED

| Step | Task | Status |
|------|------|--------|
| 2.1 | Create MEMORY.md | ✅ Done |
| 2.2 | Create context/about.md | ✅ Done |
| 2.3 | Create context/business.md | ✅ Done |
| 2.4 | Create context/clients.md | ✅ Done |
| 2.5 | Create references/3ms-framework.md | ✅ Done |
| 2.6 | Create references/4cs-framework.md | ✅ Done |
| 2.7 | Create project files (10 clients) | ✅ Done |

### Phase 3: Connect Tools (Day 2-3) — COMPLETED

| Step | Task | Status |
|------|------|--------|
| 3.1 | Configure Hermes Agent (.hermes.md) | ✅ Done |
| 3.2 | Configure Claude Code (CLAUDE.md) | ✅ Done |
| 3.3 | Configure Codex (AGENTS.md) | ✅ Done |
| 3.4 | Open vault in Obsidian | ✅ Done by user |
| 3.5 | Run /obsidian-second-brain | ✅ N/A (using built-in graph) |

### Phase 4: Automate (Day 4-5) — COMPLETED

| Step | Task | Status |
|------|------|--------|
| 4.1 | Set up nightly sync cron | ✅ Done |
| 4.2 | Configure morning brief | ✅ Done |
| 4.3 | Configure nightly consolidation | ✅ Done |
| 4.4 | Configure weekly review | ✅ Done |
| 4.5 | Configure health check | ✅ Done |
| 4.6 | Set up end-of-session write-back | ✅ Done |

### Phase 5: Dashboard & HTTPS (Day 5) — COMPLETED

| Step | Task | Status |
|------|------|--------|
| 5.1 | Create dashboard.html | ✅ Done |
| 5.2 | Add brain.aitomate.cloud DNS record | ✅ Done |
| 5.3 | Deploy nginx config | ✅ Done |
| 5.4 | Test dashboard live | ✅ Done |

---

## File Structure

```
brain-vault/
├── _index.md                     ← Vault-wide index (auto-built)
├── log.md                        ← Operation history
├── brain.yaml                    ← Authority boundaries
│
├── CLAUDE.md                     ← Claude Code routing
├── AGENTS.md                     ← Codex routing (identical)
├── MEMORY.md                     ← Shared memory (all tools)
├── SOUL.md                       ← Hermes personality
├── .hermes.md                    ← Hermes Agent project context
│
├── context/
│   ├── about.md                  ← About Umesh ji
│   ├── business.md               ← AITOmate Systems
│   └── clients.md                ← All clients & prospects
│
├── references/
│   ├── 3ms-framework.md         ← Nate Herk's 3Ms
│   └── 4cs-framework.md         ← Nate Herk's 4Cs
│
├── decisions/
│   └── log.md                    ← Append-only decisions
│
├── projects/
│   ├── aitomate-systems.md
│   ├── alan.md
│   ├── anand-hiremath.md
│   ├── jaguar-villa.md
│   ├── kumaraswamy.md
│   ├── saurabh-divekar.md
│   ├── seedwise.md
│   ├── solowarrior.md
│   ├── ss-vinfra.md
│   └── vna.md
│
├── raw/                          ← Drop sources here
├── wiki/                         ← Auto-generated pages
├── archives/                     ← Old files
│
└── .claude/
    └── skills/
        ├── onboard/SKILL.md
        ├── audit/SKILL.md
        └── level-up/SKILL.md
```

---

## Tool Configurations

### Hermes Agent (.hermes.md)

**Location:** `/opt/data/ais-os-clone/.hermes.md`  
**Purpose:** Auto-loaded by Hermes when working in vault directory

Key rules:
- Read MEMORY.md first for active deals/clients
- Projects folder has client details
- Decisions are append-only
- End-of-session write-back required
- Communication: Address as "Umesh ji"

### Claude Code (CLAUDE.md)

**Location:** `/opt/data/ais-os-clone/CLAUDE.md`  
**Purpose:** Auto-loaded when Claude Code opens vault directory

Key rules:
- Same content as AGENTS.md
- Tool routing to context/, projects/, references/
- Memory rules for shared state

### Codex (AGENTS.md)

**Location:** `/opt/data/ais-os-clone/AGENTS.md`  
**Purpose:** Auto-loaded when Codex opens vault directory

Key rules:
- Identical to CLAUDE.md
- Portable across AI tools

### brain.yaml

**Location:** `/opt/data/ais-os-clone/brain.yaml`  
**Purpose:** Authority boundaries (who can write what)

```yaml
write_prefixes:
  hermes: ["context/", "decisions/", "MEMORY.md", "wiki/"]
  claude_code: ["context/", "decisions/", "MEMORY.md", "projects/", "wiki/"]
  codex: ["context/", "decisions/", "MEMORY.md", "projects/", "wiki/"]
```

---

## Cron Jobs

| # | Name | Job ID | Schedule | Time (IST) | Purpose |
|---|------|--------|----------|------------|---------|
| 1 | Brain Vault Sync | 2eb892a94d34 | 18:30 UTC | 12:00 AM | Nightly git sync |
| 2 | Brain Vault Morning Brief | aca0c1830c19 | 02:00 UTC | 7:30 AM | Daily status |
| 3 | Brain Vault Nightly Consolidation | 29bd8a31011c | 19:00 UTC | 12:30 AM | Consolidate vault |
| 4 | Brain Vault Weekly Review | 8b5bc6550ab3 | Mon 02:00 UTC | Mon 7:30 AM | Weekly summary |
| 5 | Brain Vault Health Check | a72cc9b0c632 | 12:00 UTC | 5:30 PM | Vault integrity |

### Cron Job Details

#### Brain Vault Sync (2eb892a94d34)
```bash
cd /opt/data/ais-os-clone
git pull --rebase --autostash --quiet
git add -A
git commit --quiet -m "chore(sync): brain vault snapshot $(date)"
git push --quiet
```

#### Brain Vault Morning Brief (aca0c1830c19)
- Reads MEMORY.md, projects/, decisions/log.md
- Generates concise morning brief (<200 words)
- Covers active deals, priorities, pending actions

#### Brain Vault Nightly Consolidation (29bd8a31011c)
- Pulls latest from GitHub
- Reads all project files
- Updates MEMORY.md with current state
- Commits and pushes

#### Brain Vault Weekly Review (8b5bc6550ab3)
- Comprehensive weekly review
- Deal progression, client updates, vault health
- Saves to decisions/weekly-review-YYYY-WNN.md

#### Brain Vault Health Check (a72cc9b0c632)
- Checks file integrity
- Verifies git status
- Tests remote sync
- Reports HEALTHY / NEEDS ATTENTION

---

## Dashboard Setup

### brain.aitomate.cloud

**DNS Record:**
- Type: A
- Name: brain
- Value: 72.60.103.200
- TTL: 300

**Nginx Config:** `/etc/nginx/sites-enabled/nginx-brain.aitomate.cloud.conf`

**Deploy Script:** `/opt/data/hermes-vps-clone/deploy-brain.sh`

**Deploy Process:**
1. GitHub repo updated
2. Nightly cron pulls changes
3. Dashboard files copied to /var/www/brain.aitomate.cloud/
4. Nginx reloaded

---

## Maintenance

### Daily

- Morning brief arrives at 7:30 AM IST
- Check Telegram for cron job notifications

### Weekly

- Weekly review every Monday at 7:30 AM IST
- Review deals, client updates, vault health

### Monthly

- Check GitHub for stale branches
- Update project files as deals progress
- Review and archive old files

### Adding New Clients

1. Create `projects/<client-name>.md`
2. Update `context/clients.md`
3. Update `MEMORY.md`
4. Commit and push

### Updating Deal Stages

1. Edit `projects/<client-name>.md`
2. Update `MEMORY.md` active deals section
3. Commit and push

---

## Troubleshooting

### Issue: brain.aitomate.cloud not loading

**Check DNS:**
```bash
nslookup brain.aitomate.cloud
# Should return 72.60.103.200
```

**Check Nginx:**
```bash
systemctl status nginx
nginx -t
```

**Check Dashboard Files:**
```bash
ls -la /var/www/brain.aitomate.cloud/
```

**Check Deploy Log:**
```bash
tail -20 /var/log/brain-deploy.log
```

### Issue: Cron job not running

**Check Crontab:**
```bash
crontab -l
```

**Check Cron Logs:**
```bash
journalctl -u cron --since "1 hour ago"
```

**Manual Run:**
```bash
bash /opt/data/hermes-vps-clone/deploy-brain.sh
```

### Issue: Changes not syncing

**Manual Sync:**
```bash
cd /opt/data/ais-os-clone
git pull --rebase --autostash
git add -A
git commit -m "manual sync"
git push
```

**Check Git Status:**
```bash
cd /opt/data/ais-os-clone
git status
git log --oneline -5
```

### Issue: Obsidian graph not showing links

**Solution:**
1. Ensure notes have wikilinks: `[[note-name]]`
2. Rebuild graph: Ctrl+G or click graph icon
3. Check Filters panel — disable any active filters

---

## Frameworks

### The 3Ms Framework (Nate Herk)

| M | Meaning | Application |
|---|---------|-------------|
| **Mindset** | Default Shift, Function Breakdown, Curiosity Rule | "To what extent can AI be leveraged here?" |
| **Method** | Find Constraint → EAD → Map Process → Pick Autonomy Level → Tie to KPI | Systematic decision-making |
| **Machine** | Lego Principle, Validation Chain, Bike Method, Intern Rule, Kill Switch | Build workflows, not agents |

### The Four Cs of an AIOS (Nate Herk)

| # | Layer | One-liner | Test |
|---|-------|-----------|------|
| 1 | **Context** | Knows your business | Fresh session answers "what does this business do?" |
| 2 | **Connections** | Reaches your stuff | "What's on my calendar tomorrow?" → live data |
| 3 | **Capabilities** | Knows how to do the work | Short phrase triggers multi-step workflow |
| 4 | **Cadence** | Runs without being asked | Laptop closed. Brief lands in inbox. |

### Dependency Graph

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

## Security

| Feature | Implementation |
|---------|---------------|
| **GitHub Auth** | PAT token for pushes (rotated regularly) |
| **DNS** | A record pointing to VPS IP |
| **Nginx** | Security headers (X-Frame-Options, X-Content-Type-Options, X-XSS-Protection) |
| **Cache** | HTML never cached, assets cached 1 hour |
| **Hidden Files** | Denied via nginx config |
| **API Keys** | Stored in .env, never in vault |

---

## Appendix: Source Repos

| Repo | URL | Purpose |
|------|-----|---------|
| Brain Vault | github.com/umeshsureban/AIS-OS | Centralized memory |
| VPS Config | github.com/umeshsureban/hermes_VPS | VPS configuration |
| AIS-OS (original) | github.com/nateherkai/AIS-OS | Framework inspiration |

---

## Quick Commands Reference

```bash
# === VAULT ===
cd /opt/data/ais-os-clone

# Pull latest
git pull --rebase --autostash

# Stage, commit, push
git add -A && git commit -m "update" && git push

# Check status
git status && git log --oneline -5

# === DASHBOARD ===
# Deploy manually
bash /opt/data/hermes-vps-clone/deploy-brain.sh

# Check dashboard
curl -sI http://localhost

# Check nginx
systemctl status nginx
nginx -t

# === CRON ===
# List cron jobs
crontab -l

# Check cron logs
journalctl -u cron --since "1 hour ago"
```

---

*Document prepared by Maya (Hermes Agent) for Umesh ji*  
*Date: September 5, 2026*  
*Version: 1.0*
