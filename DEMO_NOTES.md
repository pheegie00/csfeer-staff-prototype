# CORE Prototype: Customer Demo Notes

Recording reference + Jira ticket coverage. Last updated 2026-05-21.

---

## Part 1: Feature inventory by Jira ticket

### CORE tickets (shipped against the original backlog)

| Ticket | What it does | Status |
|---|---|---|
| CORE-21 | Audit log captures every state change with actor, action, target, timestamp | Shipped |
| CORE-22 | SubmissionWindow model + editor (Opens / Closes dates per form version, blocks recipient start outside window) | Shipped |
| CORE-23 | Publish-new-version flow for FormDefinition templates | Shipped |
| CORE-24 | Version history view on Form Builder detail | Shipped |
| CORE-25 | FormScoping by org type and state (controls which recipients see a form) | Shipped |
| CORE-29 | Reviewer role can return / determine but not edit form templates | Shipped |
| CORE-35 | Audit log filters (actor, target, action type, date range) | Shipped |
| CORE-36 | Audit log export for FISMA / NIST 800-53 evidence | Shipped |
| CORE-46 | CSV export of resolved submissions | Shipped |
| CORE-47 | System audit log viewer page | Shipped |
| CORE-132 | Program Admin role gates Form Builder edit / publish actions | Shipped |
| CORE-167 | Return-for-revision rationale flow (reviewer writes rationale, recipient sees it on next open) | Shipped |
| CORE-192 | Auditor role is read-only across submissions and audit log | Shipped |

### STAFF-MP tickets (multi-program scaling)

| Ticket | What it does | Status |
|---|---|---|
| STAFF-MP-01 | ACFOffice + Program models, FormDefinition.program FK, seed for OCS/OFA programs | Shipped |
| STAFF-MP-02 | OrganizationProfile.org_type (Tribe/State/Territory/CBO/etc.) with backfill | Shipped |
| STAFF-MP-03 | FormDefinition.cycle_type (annual / quarterly / monthly / ad-hoc) | Shipped |
| STAFF-MP-04 | UserProgramAssignment scoping (OCS staff cannot see OFA submissions) | Shipped |
| STAFF-MP-05 | Program-scoped Form Builder permissions | Shipped |
| STAFF-MP-06 | Shared forms (SF-424) governance, is_shared flag on FormDefinition | Partial (model + flag exist, dedicated Platform Admin edit UI deferred) |
| STAFF-MP-07 | Form Builder UI per-program views (chip filters, scoped list) | Shipped |

### Additional features built beyond Jira

| Feature | What it does |
|---|---|
| Feature flag system | 9 registered flags, superuser-only `/staff/features/` admin, friendly 503 disabled page, nav-level gating, auto-seed on first read |
| Help section | Quick start guides for 5 roles, 20 KB articles, audience-tagged filtering, 404 (not 403) on out-of-audience to keep articles non-enumerable |
| KB-grounded chatbot | Keyword + synonym scoring against article titles / keywords / body (not an LLM, no hallucination surface), top-2 results, 20-turn session history |
| View-as persona toggle | Superuser clicks their avatar and impersonates any seeded demo persona; session flag keeps the toggle visible after switching to a non-superuser |
| Demo personas | 7 staff + 3 recipient personas seeded idempotently |
| Single-program admins | Jordan (CSBG-only) and Casey (LIHEAP-only) so demo can show narrower scopes than whole-office |
| Program chip filters | Clickable program chips on Form Builder list, gated by `form_builder_chip_filters` flag |
| Avatar-as-toggle | Persona switcher lives on the avatar (no separate UI element) |
| Recipient window + scope enforcement | Form list hides out-of-scope forms, blocks start outside window, gated by `recipient_window_enforcement` flag for demo flexibility |
| Kanban + Card inbox views | Three view modes for Submissions inbox (Table, Kanban, Card) |
| Phase II + OFA seed data | 21 form templates across 11 programs (CSBG state/territory, LIHEAP, LIHWAP, AFI, CED, RCD, SSBG, TANF, Tribal TANF, HMRF, HPOG) so OFA personas have realistic templates to open |
| Feature-disabled page | 503 page with the flag's label + description so users know why a link went dark |

---

## Part 2: Demo recording script (~8 minutes)

> Style note: confident, plain English, second person. Aim for one breath per step.

### Pre-recording checklist

- [ ] Local dev server running at `http://ui.core:8000` (already up as of this writing)
- [ ] Signed in as `root@acf.hhs.gov` (Platform Superuser) so View-as toggle works
- [ ] Browser zoom at 100%, no zoom level distractions
- [ ] Clear browser console / hide bookmark bar for a clean shot
- [ ] Have this script open on a second monitor or printed

### Step 1 (0:00 to 1:00). Open as Maya, the reviewer

**Persona**: Maya Rodriguez (OCS Reviewer)
**URL**: `/staff/`

Switch to Maya via the avatar dropdown. Say:

> "This is what a federal reviewer sees the moment they sign in. Maya is on the OCS team, so her inbox is already scoped to just OCS submissions, nothing from OFA leaks in."

Click between **Table**, **Kanban**, and **Card** views.

> "Three layouts so reviewers can work the queue how they think about it."

Why it matters: zero setup, zero filtering, the right work shows up.

### Step 2 (1:00 to 2:30). Open a submission, return it, then determine it

Click the top submission card. Walk through the form fields on the left, the rationale panel on the right. Click **Return for revision**, write a one-line rationale, submit.

> "Every rationale is captured, timestamped, and shown to the recipient the next time they open the form."

Hit back, open a second submission, click **Record determination**, pick **Accepted**, save.

Why it matters: the two actions reviewers do all day are one click and one sentence each, and both are fully audited.

### Step 3 (2:30 to 3:30). Switch to Dana, then Jordan, via View-as

> "I'm signed in as a superuser for this demo, so I can switch personas without logging out."

Click your avatar in the top right, pick **Dana Chen (OCS Program Admin)**. Land back on the inbox.

> "Same data, but notice the nav now has Form templates available. Reviewers don't see that link at all."

Switch again to **Jordan Lee (CSBG Program Admin)**.

> "Jordan only manages CSBG, so her Form Builder list is narrower than Dana's. Same UI, different scope, all driven by program assignments."

Why it matters: role gating is invisible until it matters, then it's exactly right.

### Step 4 (3:30 to 5:00). Form Builder: window, scope, publish

**URL**: `/staff/form-builder/` (as Dana, since she has more programs to demo with)

Click into a CSBG form (e.g. **CSBG Model Tribal Plan**). On the detail page:

Click **Edit submission window**, set Opens and Closes dates, save.

> "That's CORE-25. Anything outside the window is blocked for recipients."

Click **Edit scope**, change the org-type checkboxes (e.g. Tribe only), save.

> "That's CORE-22. Only tribes will see this form on their side."

Hit **Publish new version**, confirm.

> "Versioning is automatic, the previous version stays available for in-flight submissions."

Why it matters: program admins self-serve everything, no platform team in the loop.

### Step 5 (5:00 to 6:00). Switch to Tasha, a tribe Authorized Official

Avatar, **Tasha Whitehorse (Tribe AO)**. Land on the recipient form list.

> "Tasha sees only forms her org is in scope for. The form Dana just narrowed to tribes? Right there. The state-only forms? Gone."

If a form is outside the window, point at the **Opens MM/DD** or **Closed** chip and try to start it.

> "Hard block, friendly message. The same enforcement Dana set up two minutes ago is live for the recipient with no deploy."

Why it matters: the policies admins write are the policies recipients experience, end to end.

### Step 6 (6:00 to 7:00). Help section and chatbot

**URL**: `/staff/help/` (switch back to Maya for this so audience filtering is visible)

Avatar, **Maya Rodriguez**, then click **Help** in the nav.

> "Help is audience-tagged. Maya only sees reviewer-facing articles. If I were Tasha, I'd see the recipient guides instead, none of the admin ones."

Open **How to return a submission for revision**. Back out, scroll to the chatbot, type *"how do I export"*. Show the top-2 article results.

> "It's a keyword search against the knowledge base, not an LLM. No hallucination risk, every answer is a real article."

Why it matters: support load goes down, and we never invent answers.

### Step 7 (7:00 to 8:00). Superuser Features admin

Avatar, **Platform Superuser (root)**. Click **Features** in the nav (only superusers see it).

> "Every demo-sensitive feature is a flag. If we're showing a customer and the chatbot isn't ready, I flip it off here."

Toggle **Help chatbot** to off, navigate back to **Help**, point at the missing chat widget.

> "Gone, instantly, no deploy."

Toggle **CSV exports** off, watch the **Exports** nav item disappear. Toggle them back on.

Why it matters: the team controls what each customer sees in real time, on a per-feature basis, with a single click.

### Close (8:00)

> "Everything you saw is one Django app, one database, one deploy. Multi-program scoping, role gating, window and scope enforcement, audit, exports, help, and feature flags are all wired together. Happy to dig into any of these."

---

## Persona quick reference

| Persona | Email | Role |
|---|---|---|
| Maya Rodriguez | `maya.rodriguez@acf.hhs.gov` | OCS Reviewer (all OCS programs) |
| Dana Chen | `dana.chen@acf.hhs.gov` | OCS Program Admin (all OCS programs) |
| Sam Patel | `sam.patel@acf.hhs.gov` | OFA Program Admin (all OFA programs) |
| Riley Brooks | `riley.brooks@acf.hhs.gov` | OCS Auditor (read-only) |
| Jordan Lee | `jordan.lee@acf.hhs.gov` | CSBG Program Admin (CSBG only) |
| Casey Wu | `casey.wu@acf.hhs.gov` | LIHEAP Program Admin (LIHEAP only) |
| Platform Admin | `root@acf.hhs.gov` | Cross-office superuser |
| Tasha Whitehorse | `tribe-ao@example.com` | Choctaw Nation Authorized Official |
| Jordan Miller | `state-editor@example.com` | OK Dept of Commerce Form Editor |
| Alex Nguyen | `cbo-approver@example.com` | Tulsa Community Action Agency Form Approver |
