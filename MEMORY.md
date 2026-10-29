# Shared Memory

This file is the shared memory layer for all AI tools: Hermes Agent, Claude Code, and Codex.

**Last Updated:** 2026-10-29T19:01:24Z (nightly consolidation; reconciled against all `projects/` files — no material status changes found)

---

## Active Deals & Prospects

### Kumaraswamy
- **Location:** West Bengal, Siligudi, India
- **Phone:** +91 9363751502
- **Status (2026-09-29, Umesh update):** Requirements discussion held with Kumaraswamy and the spiritual group. Their side will deliver the landing page; Umesh / AITOmate Systems will deliver AI-enabled WhatsApp automation.
- **Deal Stage:** Live CRM stage is not verified. The prior recorded stage was Appointment Scheduled (20%); do not assume closed-won.
- **Latest clarification:** Kumaraswamy's team will provide Guruji's profile/biodata.
- **Review:** Saturday, 3 October 2026. This was not a final delivery deadline; no outcome is recorded in the vault as of 2026-10-29.
- **Next Actions:** Capture the review outcome plus WhatsApp automation scope and landing-page handoff; confirm commercial terms and delivery dates; prepare a design document for approval before implementation.

### Anand Hiremath
- **Location:** Australia
- **Company:** Education SaaS
- **Email:** anandp.hiremath@gmail.com; anandp.hiremath@googlemail.com
- **Phone:** +61 415 181 698
- **Deal Stage:** Dead — not agreed.
- **Status:** Demo video sent; offer not accepted. No active follow-up.
- **Reconciliation:** `projects/anand-hiremath.md` and `context/clients.md` were aligned to this stage on 2026-10-29. This file stays the authority until a new live CRM update is available.

---

## Active Clients

### Basavaraj (Jaguar Villa)
- **Email:** jaguar.villas@gmail.com
- **Status:** Engagement review pending; payment/status pending resolution.
- **Last Recorded Update:** 2026-09-09 WhatsApp message requesting electricity bill.
- **Actions:** Complete engagement-review follow-up; obtain electricity bill for KYC documentation — **PENDING / AGEING**.

### Darshan (SeedWise)
- **Email:** agrosaathi.it@gmail.com
- **Status:** Active — payments received, including the second ₹50,000 cash payment via Praveen Mudhol.
- **Current Delivery:** Mobile app delivery to Google Play Store — **PENDING / AGEING**.

### Sanjay (SSVInfra)
- **Primary Email:** sanjay@ssvinfra.net
- **Projects Email:** projects@ssvinfra.net
- **Status:** Active — documentation pending.
- **Last Recorded Update:** 2026-09-09 WhatsApp to the new Jalandhar issue email address; Bheemu reported an email-accessibility issue.
- **Actions:** Collect client documentation; resolve email-accessibility issue — **PENDING / AGEING**.

### Saurabh Divekar
- **Status:** Active client.
- **Last Recorded Update:** 2026-09-09; waiting for mobile number from Diwakar representative.
- **Action:** Follow up for mobile number — **PENDING / AGEING**.

---

## Closed Clients

### Sravan Kumar (VNA)
- **Location:** Hyderabad
- **Status:** Closed.
- **Services:** GBP, LinkedIn, WhatsApp lead gen (50 students), review automation.

### Alan (Mark Industries)
- **Status:** Closed (free audit sent, no conversion).
- **Follow-up:** Retired when the deal was closed on 2026-09-06.

### Parijat (SoloWarrior)
- **Status:** Closed.

---

## Pipeline Summary

| Metric | Count |
|--------|-------|
| Active Clients | 4 |
| Closed Clients | 3 |
| Open Deals / New Leads | 1 (Kumaraswamy — requirements discussed; CRM stage unverified) |
| Dead Deals / New Leads | 1 (Anand Hiremath — Dead / not agreed; shared-memory reconciliation governs) |
| Total Tracked Client & Deal Records | 9 |
| Total Deals / Prospects | 2 |
| Pending Action Items (active clients + open deals) | 9 |
| Ageing Action Groups (last recorded update before 2026-10-14 or no current timestamp) | 4 |
| Explicitly Overdue Delivery Deadlines | 0 |
| Overdue Scheduled-Outcome Capture | 1 (Kumaraswamy review — 2026-10-03; 26 days overdue as of 2026-10-29) |

**Deal-stage reconciliation:** `projects/anand-hiremath.md`, `projects/aitomate-systems.md`, and `context/clients.md` were aligned to the stages above on 2026-10-29. On any future conflict, this file governs until a new live CRM update is available.

**Ageing and overdue note:** Basavaraj, SeedWise, SSVInfra, and Saurabh have pending delivery/follow-up groups without a current update. Kumaraswamy’s review was scheduled for 2026-10-03 and has no captured outcome as of 2026-10-29; outcome capture is 26 days overdue, but this is not evidence of an overdue delivery. No delivery action has a recorded due date, so the four ageing groups are stalled rather than formally overdue.

---

## Business Email Infrastructure

### aitomate.cloud
- **Status:** Cloudflare Email Routing is active and ready.
- **Inbound routes:**
  - `info@aitomate.cloud` → `maya.aitomate@gmail.com`
  - `mayaAI@aitomate.cloud` → `maya.aitomate@gmail.com`
  - Cloudflare displays the second address as `mayaai@aitomate.cloud`; email addresses are case-insensitive.
- **Catch-all:** Disabled.
- **Gmail outbound:** “Send as” is enabled for `Aitomate <info@aitomate.cloud>`.
- **Default Gmail sender:** Remains `maya.aitomate@gmail.com`.
- **Outbound validation:** A test to `umesh.sureban@gmail.com` succeeded and displayed `Aitomate <info@aitomate.cloud>` as the sender.
- **Validation limitation:** Gmail deduplicated the sent and received test into one message, so independent SPF/DKIM/DMARC results were not exposed through the connected Maya account.
- **DNS preservation:** All 25 original DNS records were preserved. Five Cloudflare email records were added. All records remain DNS-only.
- **Authoritative nameservers:**
  - `rosalyn.ns.cloudflare.com`
  - `stanley.ns.cloudflare.com`
- **DNS recovery backup:** `C:\Users\DELL\Documents\Codex\2026-09-18\chec\outputs\aitomate-cloud-dns-backup.json`
- **Credential handling:** The Gmail app password was not stored or displayed.
- **Migration deadline:** Gmail's third-party “Send as” SMTP method is temporary and is expected to end in January 2027. Migrate outbound mail to Google Workspace or a dedicated SMTP provider before then.

---

## Lessons Learned

### Technical
- YouTube uploads via Composio MCP require H.264 Baseline Profile 3.0 — High Profile fails with 'Can't process file'
- Instagram posting via Composio MCP fails — S3 staging URLs not accessible during publish step
- Host VPS root crontab is populated; Hermes application jobs run through the internal Docker scheduler, not Linux cron
- Hermes cron jobs must be explicitly pinned after a global provider/model change or drift protection skips them to prevent unintended spend
- Hermes cron model policy: Luna for lightweight checks/reminders, Terra for multi-tool business workflows, the meeting-intelligence pipeline runs on the Claude subscription provider (`sonnet`, pinned 2026-10-29) because Sol is rejected by the Codex ChatGPT route; do not use Astra for scheduled jobs

### Communication
- Address Umesh ji as "Umesh ji" — never "Sir Ji" or "Surji"
- Respectful Hindi: "आप" + "Umesh ji"
- Respectful Kannada: "ನೀವು" + "Umesh ji"
- Never informal ("तुम"/"ನಿನ್ನು")

### Preferences
- Prefers direct action over excessive confirmation
- Shares info in fragments, expects piecing together
- Corrects assumptions immediately
- Wants me to verify data himself rather than asking