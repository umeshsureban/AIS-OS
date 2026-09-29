# Shared Memory

This file is the shared memory layer for all AI tools: Hermes Agent, Claude Code, and Codex.

**Last Updated:** 2026-09-29T12:23:32Z (nightly consolidation)

---

## Active Deals & Prospects

### Anand Hiremath
- **Location:** Australia
- **Company:** Education SaaS
- **Email:** anandp.hiremath@gmail.com
- **Additional Email:** anandp.hiremath@googlemail.com
- **Phone:** +61 415 181 698
- **Deal Stage:** Dead — not agreed
- **Status:** Demo video sent; offer not accepted.
- **Next Actions:** None.
- **Reconciliation:** `projects/anand-hiremath.md` still shows “Decision Maker Bought-In (80%)” and follow-up actions, but this shared memory is the later manual authority reconciliation and governs until a new live CRM update is available.

### Kumaraswamy
- **Location:** West Bengal, Siligudi, India
- **Phone:** +91 9363751502
- **Deal Stage:** Appointment Scheduled (20%)
- **Status:** Arranging an initial requirements meeting with his spiritual Guru client (last recorded update: Sep 9).
- **Next Actions:** Follow up via WhatsApp; schedule the initial requirements meeting; prepare automation proposal — **PENDING / AGEING**

---

## Active Clients

### Basavaraj (Jaguar Villa)
- **Email:** jaguar.villas@gmail.com
- **Status:** Engagement review pending; payment/status pending resolution.
- **Last Recorded Update:** Sep 9 WhatsApp message requesting electricity bill.
- **Actions:** Complete engagement-review follow-up; obtain electricity bill for KYC documentation — **PENDING / AGEING**

### Darshan (SeedWise)
- **Email:** agrosaathi.it@gmail.com
- **Status:** Active — payments received, including the second ₹50,000 cash payment via Praveen Mudhol.
- **Current Delivery:** Mobile app delivery to Google Play Store.
- **Actions:** Deliver the mobile app to Google Play Store; confirm automation deliverables; collect app/mobile-testing feedback — **PENDING / AGEING**

### Sanjay (SSVInfra)
- **Primary Email:** sanjay@ssvinfra.net
- **Projects Email:** projects@ssvinfra.net
- **Status:** Active — documentation pending.
- **Last Recorded Update:** Sep 9 WhatsApp to the new Jalandhar issue email address; Bheemu reported email-accessibility issue.
- **Actions:** Collect client documentation; resolve email-accessibility issue — **PENDING / AGEING**

### Saurabh Divekar
- **Status:** Active client.
- **Last Recorded Update:** Sep 9; waiting for mobile number from Diwakar representative.
- **Action:** Follow up for mobile number — **PENDING / AGEING**

---

## Closed Clients

### Sravan Kumar (VNA)
- **Location:** Hyderabad
- **Status:** Closed
- **Services:** GBP, LinkedIn, WhatsApp lead gen (50 students), review automation.

### Alan (Mark Industries)
- **Status:** Closed (free audit sent, no conversion).
- **Follow-up:** Retired when the deal was closed on 2026-09-06.

### Parijat (SoloWarrior)
- **Status:** Closed

---

## Pipeline Summary

| Metric | Count |
|--------|-------|
| Active Clients | 4 |
| Closed Clients | 3 |
| Open Deals / New Leads | 1 (Kumaraswamy — Appointment Scheduled, 20%) |
| Dead Deals / New Leads | 1 (Anand Hiremath — Dead / not agreed) |
| Total Tracked Client & Deal Records | 9 |
| Open Action Items (active clients + open deals) | 11 |
| Ageing Action Groups (>5 days since recorded update) | 5 |
| Explicitly Overdue Items (dated deadline missed) | 0 |

**Ageing note:** Every open action group was last updated on Sep 9, approximately 20 days before this consolidation. No action has a recorded due date, so they are ageing/stalled rather than formally overdue.

---

## Lessons Learned

### Technical
- YouTube uploads via Composio MCP require H.264 Baseline Profile 3.0 — High Profile fails with 'Can't process file'
- Instagram posting via Composio MCP fails — S3 staging URLs not accessible during publish step
- Host VPS root crontab is populated; Hermes application jobs run through the internal Docker scheduler, not Linux cron
- Hermes cron jobs must be explicitly pinned after a global provider/model change or drift protection skips them to prevent unintended spend
- Hermes cron model policy: Luna for lightweight checks/reminders, Terra for multi-tool business workflows, and Sol only for the meeting-intelligence pipeline; do not use Astra for scheduled jobs

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
