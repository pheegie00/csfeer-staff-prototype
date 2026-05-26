# CORE Prototype — Release Notes (Phase 4 + Phase 5)

**Release date:** 2026-05-21
**Branch:** `staff-prototype`
**Deployed URL:** https://acf-core.fly.dev/
**Auth provider:** https://acf-core-keycloak.fly.dev/ (Keycloak)

---

## Access for the PM

| Field | Value |
|---|---|
| URL | https://acf-core.fly.dev/ |
| Login (any persona, demo password) | `core-demo` |
| Recommended persona for general walk-through | `root@acf.hhs.gov` (Platform Superuser; can View-as any other persona) |
| Source repo | `pheegie00/csfeer-staff-prototype` branch `staff-prototype` |

Demo personas (each uses password `core-demo`):

| Email | Role |
|---|---|
| `root@acf.hhs.gov` | Platform Superuser |
| `maya.rodriguez@acf.hhs.gov` | OCS Reviewer (all OCS programs) |
| `dana.chen@acf.hhs.gov` | OCS Program Admin (all OCS programs) |
| `sam.patel@acf.hhs.gov` | OFA Program Admin (all OFA programs) |
| `riley.brooks@acf.hhs.gov` | OCS Auditor (read-only) |
| `jordan.lee@acf.hhs.gov` | CSBG Program Admin (CSBG only) |
| `casey.wu@acf.hhs.gov` | LIHEAP Program Admin (LIHEAP only) |
| `tribe-ao@example.com` | Recipient: Choctaw Nation Authorized Official |
| `state-editor@example.com` | Recipient: OK Dept of Commerce Form Editor |
| `cbo-approver@example.com` | Recipient: Tulsa CBO Form Approver |

---

## What's new in this release

### Major new capabilities

1. **Multi-program scaling foundation.** The app now models ACFOffice → Program → FormDefinition explicitly, and per-program staff assignments determine who sees what. OCS and OFA are both modeled, with 11 programs and 21 form templates seeded across them.

2. **Form Builder UI.** A program-scoped admin layer at `/staff/form-builder/` where Program Admins manage their templates: edit submission windows per fiscal year, adjust org-type scoping, and publish new versions with automatic auto-close of in-progress drafts.

3. **Recipient-side enforcement.** Out-of-scope forms are hidden from a recipient's home page. Forms with a closed window are visible but un-startable, with a clear "Closed MM/DD" badge. Existing drafts remain editable when a window closes (per CORE-25 acceptance).

4. **Per-role help section.** `/staff/help/` ships 20 knowledge base articles plus role-specific quick start guides. Each user only sees articles relevant to their role. A KB-grounded chatbot answers questions by surfacing matching articles (deterministic search; not an LLM).

5. **Feature flag admin.** Superusers can toggle 9 features on or off live at `/staff/features/` without a redeploy. Used to hide work-in-progress before a customer demo. Toggling a feature off hides the nav item and blocks the URL with a friendly disabled page.

6. **View-as persona toggle.** Platform Admins can click their avatar in the header and switch into any seeded persona with one click. Keeps the demo flow fluid (no logout / login per role switch). Allow-listed so a leaked URL can't impersonate real accounts.

7. **Deployed to Fly.io.** The whole stack (Django app + Postgres + Keycloak) runs on Fly's free / near-free tiers. Two separate apps: `acf-core` (Django) and `acf-core-keycloak` (Keycloak 26.4 with a pre-seeded `csfeer` realm).

### Smaller improvements

- 13 CORE tickets and 7 STAFF-MP tickets shipped (see verification checklist below).
- Three inbox view modes (Table / Kanban / Card).
- CSV exports + tamper-evident audit log for compliance.
- Sample data: 11 programs, 21 form templates, 9 demo submissions across multiple statuses.
- Single-program admins (CSBG-only, LIHEAP-only) demonstrate that role scoping is finer than office-wide.
- Program filter chips on Form Builder list.
- Root URL `/` now redirects straight to `/staff/` so reviewers land on the inbox.
- No em dashes in any user-facing string (per content style rule).

---

## Verification checklist for the PM

Each ticket below has a one-paragraph "how to verify" the PM can run against the deployed URL. Order matches the suggested testing flow.

### Foundation tickets (STAFF-MP series)

> **Note for the PM:** STAFF-MP-* tickets are NOT in Jira. They were created in the project's internal backlog at [`docs/backlog.md`](https://github.com/pheegie00/csfeer-staff-prototype/blob/staff-prototype/docs/backlog.md) when we identified multi-program scaling work that was prerequisite to extending the prototype beyond CSBG-only. You may want to file these 7 as new Jira tickets (titles + acceptance criteria are all in `docs/backlog.md`).

#### STAFF-MP-01 — Multi-program data model + seed
**Verify:** Sign in as Platform Admin (`root@acf.hhs.gov`). Open https://acf-core.fly.dev/staff/form-builder/. Click any program chip in the "Your programs" strip. The list should narrow to that program's forms only. Switch to Sam Patel (OFA Program Admin) via the avatar dropdown; you should see OFA programs (TANF, Tribal TANF, HMRF, HPOG), not OCS ones.

#### STAFF-MP-02 — OrganizationProfile.org_type
**Verify:** Switch to Jordan Lee (CSBG Program Admin). Open the CSBG Model Tribal Plan template. The "Org scoping" card should show org types like "Federally Recognized Tribe" and an in-scope count > 0. Edit the scope to add "State Government" and save; the count should change.

#### STAFF-MP-03 — Cycle types (annual / quarterly / ad-hoc)
**Verify:** On the Form Builder list, the Cycle column should show a mix of values (Annual, Quarterly, Ad-hoc). Not every form is annual.

#### STAFF-MP-04 — Program-scoped queries
**Verify:** Switch to Maya Rodriguez (OCS Reviewer). The Submissions inbox should show only OCS submissions. Switch to Sam Patel. The inbox should be different content (OFA submissions, currently zero seeded but the empty state confirms scoping is wired).

#### STAFF-MP-05 — Program-scoped Form Builder permissions
**Verify:** As Maya (Reviewer), the "Form templates" nav item should be visible but the Detail page should show "View only" instead of "Edit" controls. As Dana (Admin), the same template shows "Edit window", "Edit scope", "Publish new version" buttons.

#### STAFF-MP-07 — Program chip filters
**Verify:** As Dana, on Form Builder list, click the "OCS · CSBG" chip. URL becomes `?program=CSBG`, list filters to CSBG only. Click "All" to clear.

#### STAFF-MP-06 — Shared forms governance
**Status:** **PARTIAL.** Model + `is_shared` flag exist; the dedicated Platform Admin edit UI for SF-424 style shared forms is deferred to a follow-up ticket.

### Submissions workflow (CORE series)

#### CORE-29 / CORE-132 / CORE-192 — Role-based access
**Verify:** Open the Submissions inbox as Maya (Reviewer): you can return + record determination. As Riley Brooks (Auditor): the action buttons are hidden, but the same submission opens read-only. As Dana (Admin): both Submission and Form Builder are visible and editable.

#### CORE-167 — Return for revision rationale
**Verify:** As Maya, open any "Submitted" status card. Click "Return for revision". The return builder lets you add one or more review items, each with a section reference, a field reference, and your comment. Submit and the entry moves to "Returned".

#### CORE-21 / CORE-35 / CORE-36 / CORE-47 — Audit log
**Verify:** Click "Audit log" in the nav (visible to Platform Admin and Auditor roles). Filter by user, action, or date range. Each row shows actor, action, target, timestamp, IP, user-agent. Try editing a row directly via the admin (you won't be able to; it's append-only).

#### CORE-46 — CSV exports
**Verify:** Click "Exports". The page lists every (form template, fiscal year) combination with at least one resolved (Accepted / Closed) submission. Click "Export CSV" on any row. A CSV downloads with one column per form field. Open the Audit log: a new "export_csv" event should appear with your actor + the file name.

### Form Builder workflow (CORE series)

#### CORE-22 — FormScoping
**Verify:** As Dana, open CSBG Model Tribal Plan. Click "Edit scope". Uncheck Federally Recognized Tribe and check State Government. Save. Open in a new tab as Tasha Whitehorse (Tribe AO recipient): the Tribal Plan should no longer appear on her form list (she's a Tribe, but the form now wants States).

#### CORE-25 — SubmissionWindow
**Verify:** As Dana, open any form. Edit the FY26 window: set Opens to a future date, set Closes 30 days after. Save. Open as Tasha: the form shows "Opens MM/DD/YYYY" badge with a disabled Start button.

#### CORE-23 — Publish new version
**Verify:** As Dana, open a template. Click "Publish new version". The form auto-suggests the next semver (e.g. 1.1.0). Submit. The template list now shows the new version as Published with the old one deprecated.

#### CORE-24 — Auto-close in-progress drafts on publish
**Verify:** Same as CORE-23. After publishing, the impact summary should say "N in-progress submissions auto-closed". Open the audit log; you'll see one auto-close event per affected entry.

### Help section (no Jira ticket, new feature)

**Verify:**
1. As Maya, click "Help". You should see ~10 articles tagged for the reviewer role. The "How to publish a new version" admin-only article should NOT appear.
2. As Dana, the same Help page shows the publish article.
3. As Tasha (recipient), the Help page shows recipient-only articles (e.g. "How to start a new form draft"), and no admin articles.
4. Try the chatbot on the right rail. Type "how do I send a submission back". The assistant should return the "How to return a submission for revision" article.
5. Type "asdfghjkl". The assistant returns a polite fallback message with no article suggestions.

### Platform / demo plumbing (no Jira ticket, new feature)

#### Feature flags
**Verify:** As Platform Admin, click "⚙ Features" in the nav. Toggle "Help chatbot" off. Navigate to "Help"; the chat widget should be gone but the articles remain. Toggle "CSV exports" off; the "Exports" nav item should disappear. Toggle them both back on.

#### View-as toggle
**Verify:** As Platform Admin, click the avatar in the top right. Switch to Dana. The avatar now shows Dana's name. Switch to Jordan. Try switching to a NON-allow-listed user via URL fiddling: e.g. POST to `/staff/demo-users/view-as/` with `user_id` of a non-demo account. Should return 403.

#### Recipient enforcement (CORE-22 + CORE-25 wired end-to-end)
**Verify:** As Tasha (tribe AO), open `/forms/`. Forms scoped to Tribe only should appear. State-only forms (LIHEAP Household Report, CSBG State Plan) should NOT. Forms with a closed window show a "Closed" badge. Forms with an upcoming window show "Opens MM/DD" with the Start button hidden.

---

## Known gaps / deferred work

| Item | Status | Notes |
|---|---|---|
| STAFF-MP-06 (Shared forms admin UI) | Deferred | Model + `is_shared` flag exist. Dedicated Platform Admin edit UI for SF-424 is a follow-up. |
| STAFF-MP-12 (Submission Detail Figma redesign) | Not started | Chrome + Submissions inbox have been redesigned per the new Figma. Submission Detail (Tribal Plan accordion + Accept/Close modals) is the natural next deliverable. Figma assets are in hand. |
| CORE-41, 42, 70, 157 (Email notifications) | Deferred | Batch D. Needs SMTP infrastructure spike (will use `thebusinessofdelivery@gmail.com` for test sends per memory rule). |
| CORE-28 (Document new form template pattern) | Pending | Doc-only, needs to be written after Form Builder feedback. |
| Phase II form schemas | Placeholders | The 16 newly seeded Phase II + OFA form templates have `{}` schemas. Schema editor UI is a Phase 6 deliverable. |

---

## Appendix: STAFF-MP ticket drafts for Jira

The 7 STAFF-MP tickets shipped in this release were created in the project's internal backlog (`docs/backlog.md`) rather than in Jira. Below is a copy-paste-ready draft for each one so the product team can file them. Format mirrors what the CORE tickets use (Story / Acceptance / Priority).

### STAFF-MP-01: Add Program + ACFOffice models

- **Story:** As a platform owner, I want every form and submission attributable to a specific ACF program and office so that staff permissions, queues, and reporting can be scoped per program.
- **Acceptance criteria:**
  - `programs` Django app exists with `ACFOffice` and `Program` models
  - `FormDefinition.program` FK added
  - Seed data for OCS->CSBG and OFA->TANF / Tribal_TANF / HMRF / HPOG (HPOG marked inactive)
  - Existing FormDefinitions backfilled to CSBG
- **Priority:** HIGH (blocks every multi-program scenario)
- **Status in this release:** SHIPPED
- **Dependencies:** none

### STAFF-MP-02: Add org_type to OrganizationProfile

- **Story:** As a federal staff member, I want to filter and group recipients by organization type (Tribe / State / Territory / Higher Ed / CBO / Faith-Based / Workforce Agency) so that program-specific queues match program-specific recipient mixes.
- **Acceptance criteria:**
  - `OrganizationProfile.org_type` field added with 8 choices: Tribe, Tribal_Org, State, Territory, Higher_Ed, Workforce_Agency, CBO, Faith_Based
  - Existing orgs backfilled to "Tribe"
  - Staff Inbox supports filtering by org_type
- **Priority:** MEDIUM (needed before HMRF or TANF programs go live)
- **Status in this release:** SHIPPED
- **Dependencies:** none

### STAFF-MP-03: Add cycle_type to FormDefinition

- **Story:** As a federal staff member, I want each form to declare whether it's annual / quarterly / monthly / ad-hoc so that submission windows and reporting reflect the real cycle.
- **Acceptance criteria:**
  - `FormDefinition.cycle_type` choices field added (annual / quarterly / monthly / ad_hoc)
  - SubmissionWindow (CORE-25) honors the cycle when computing per-cycle deadlines
- **Priority:** MEDIUM (ACF-196R is quarterly; misclassifying as annual surfaces bad data)
- **Status in this release:** SHIPPED
- **Dependencies:** none

### STAFF-MP-04: Scope staff permissions to assigned programs

- **Story:** As an OCS staff member, I should not see OFA submissions, and vice versa.
- **Acceptance criteria:**
  - `UserProgramAssignment(user, program, role)` model added
  - `staff_review.views.InboxView.get_queryset()` filters by the user's assigned programs
  - Permissions reusable across programs (not hardcoded per program)
  - Verified end-to-end: an OCS-only reviewer never sees a TANF submission in their inbox
- **Priority:** HIGH (required as soon as program #2 lands)
- **Status in this release:** SHIPPED
- **Dependencies:** STAFF-MP-01

### STAFF-MP-05: Program-scoped Form Builder permissions

- **Story:** As an OCS form admin, I want to see and manage only CSBG forms. As an OFA TANF form admin, I want to see and manage only TANF forms. Each program self-manages without bleeding into others.
- **Acceptance criteria:**
  - 7 new FormDefinition permissions added (form_builder_view, form_builder_create, form_builder_edit_draft, form_builder_publish, form_builder_archive, form_builder_window_edit, form_builder_scope_edit)
  - Form Templates Manager UI filters templates by the user's assigned programs
  - Cross-program leakage tested (an OCS admin POSTing to an OFA template ID returns 403)
- **Priority:** HIGH (blocks program self-service)
- **Status in this release:** SHIPPED
- **Dependencies:** STAFF-MP-01, STAFF-MP-04

### STAFF-MP-06: Shared forms (SF-424 etc.) governance

- **Story:** As a platform admin, I want to manage cross-program shared forms like SF-424 from one place, while program admins reference but cannot edit them.
- **Acceptance criteria:**
  - `FormDefinition.is_shared` boolean added
  - Shared forms surface in their own section in the Form Builder UI
  - Only users with `form_builder_manage_shared` permission can edit shared forms
  - Program admins see shared forms as read-only references
- **Priority:** MEDIUM (needed when first non-CSBG program lands)
- **Status in this release:** PARTIAL
  - Model + `is_shared` flag exist and work
  - Shared-forms section renders in Form Builder list
  - Dedicated Platform Admin edit UI for shared forms is still TODO
- **Dependencies:** STAFF-MP-05

### STAFF-MP-07: Form Builder UI per-program views

- **Story:** As a form admin, when I open Form Builder I see a list scoped to my program(s). I never see other programs' forms unless I'm explicitly assigned.
- **Acceptance criteria:**
  - Form Templates Manager screen filters by the user's assigned programs
  - Shared-forms section shown separately from the user's own program forms
  - Publish + Edit actions only render on forms the user has permission for
  - Clickable program filter chips at the top of the list (one per assigned program, plus "All")
- **Priority:** HIGH (shipping Form Builder without this would teach users a global-admin pattern we'd have to retrain)
- **Status in this release:** SHIPPED
- **Dependencies:** STAFF-MP-05

### STAFF-MP-08: Pre-sign-in landing page

- **Story:** As an unauthenticated visitor, when I open the root URL I want a branded landing page that explains what CORE does and gives me a clear Sign In CTA, instead of being dumped into the auth flow without context.
- **Acceptance criteria:**
  - Public marketing page at `/` (no auth required)
  - Navy CORE header with "Sign in" button top-right
  - Hero with product description + primary "Sign in to continue" CTA
  - Feature grid (6 cards) summarizing the major capabilities (program scoping, return/determine, Form Builder, audit + exports, help, window enforcement)
  - "Programs onboarded" chip strip listing all 11 seeded programs
  - ACF "Children & Families" navy footer
  - Signed-in users still redirect straight to `/staff/` on `/` so logged-in flow isn't slowed down
- **Priority:** MEDIUM (customer-facing first impression)
- **Status in this release:** SHIPPED
- **Dependencies:** none

### STAFF-MP-09: Apply Figma "Staff Experience 05" chrome to all staff pages

- **Story:** As a federal staff member, when I sign in I want the new branded look (navy header, user-chip dropdown, ACF footer) across every staff page so the UI feels cohesive and intentional.
- **Acceptance criteria:**
  - New `_base_staff.html` chrome: navy CORE header with subtitle
  - User-chip dropdown ("First Last v") on the right of the header that contains all previously-horizontal-nav items:
    - "Go to" group: Submissions, Form templates, Exports, Audit log, Help
    - "View as (testing)" group: persona switcher (demo-admin only)
    - "Platform" group: Features admin (superuser only)
    - Sign out
  - ACF "Children & Families" navy footer on every staff page
  - Page-level secondary nav slot (subnav block) so individual pages can add their own tabs without touching base
  - No regressions: every Phase 4 + Phase 5 feature remains reachable and functional via the new dropdown
- **Priority:** MEDIUM (visual cohesion)
- **Status in this release:** SHIPPED
- **Dependencies:** none

### STAFF-MP-10: Redesign Submissions inbox per Figma

- **Story:** As a federal staff member, I want a clean Active/Completed tab split on the Submissions inbox with a focused filter row and a simple table, matching the new Figma design.
- **Acceptance criteria:**
  - Tab subnav under the header: "Active submissions" and "Completed submissions"
    - Active bucket = anything not yet resolved (Submitted / In Progress / Returned)
    - Completed bucket = Accepted or Closed
  - Filter row: regions, organizations, forms, fiscal years dropdowns + primary "Apply filter" button
  - Pale-blue section header band on the table ("Needs review" on Active, "Completed" on Completed)
  - Table columns per Figma: Organization, Forms (with OMB no. subtitle), Period, Status, Last action by, Last updated, Action
  - Distinct status pills per status (Submitted, In Progress, Returned, Accepted, Closed)
  - "Export CSV" button visible on the Completed tab (gated by the `csv_exports` feature flag)
  - Pagination footer
  - **Preserved from prior release:** Table / Kanban / Card view toggle still works (see STAFF-MP-11)
- **Priority:** MEDIUM
- **Status in this release:** SHIPPED
- **Dependencies:** STAFF-MP-09

### STAFF-MP-11: Preserve Table / Kanban / Card view toggle in redesigned inbox

- **Story:** As a federal staff member, even after the visual redesign I want to keep being able to switch between Table, Kanban, and Card views of the inbox so I can work the queue the way I think about it.
- **Acceptance criteria:**
  - View toggle control (Table / Kanban / Card) on the inbox filter row
  - Toggling view preserves the current bucket + all active filters
  - Table view matches the new Figma design (see STAFF-MP-10)
  - Kanban view renders one column per status bucket, restyled with the navy + pale-blue palette to feel native to the new design
  - Kanban columns are filtered to the active bucket (Active tab shows Submitted/In Progress/Returned lanes; Completed tab shows Accepted/Closed lanes)
  - Card view: responsive grid of detail cards, each linking to the submission detail
  - All three views link to the same submission detail page
- **Priority:** MEDIUM (existing functionality the team values)
- **Status in this release:** SHIPPED
- **Dependencies:** STAFF-MP-10

### STAFF-MP-12: Apply Figma look to Submission Detail (Tribal Plan) page

- **Story:** As a federal staff member reviewing a submission, I want the detail page to match the new Figma design: clean breadcrumb, big "Review and Submit" heading, collapsible section accordions, "Add review item" buttons per section, and confirmation modals on Accept / Close.
- **Acceptance criteria:**
  - Breadcrumb at top: "All submissions / [Organization name]"
  - Form title + status pills (Submitted / Accepted / Closed) in left column
  - Right column: "Close without acceptance" and primary blue "Accept" buttons
  - "Review and Submit" H1 with "Expand all" toggle on the right
  - Each form section renders as a collapsible accordion ("Section 1: Tribal Administrative Information", etc.) with an "Add review item" button inline
  - Banner treatments for accepted ("Submission accepted, accepted on MM/DD/YYYY at HH:MM PM by [reviewer]") and closed ("Submission closed without acceptance...") states
  - Confirmation modals on both Accept and Close actions explaining the consequences before commit
- **Priority:** MEDIUM
- **Status in this release:** NOT YET STARTED
  - Figma assets exist (Tribal Plan, Tribal Plan-1 through -4 from the Staff Experience 05 export)
  - Chrome + inbox have been redesigned; this is the natural next deliverable
- **Dependencies:** STAFF-MP-09

---

## Technical reference

**Test suite:** 170 tests, all passing on the deployed branch.

**Deployment architecture:**
- `acf-core` (Fly.io, iad region): Django 6.0.4 + gunicorn, 2 shared-cpu-1x machines, auto-stop on idle, Postgres attached.
- `acf-core-keycloak` (Fly.io, iad region): Keycloak 26.4 + H2 (in-memory; realm re-imports on every boot from baked-in JSON), 2GB shared-cpu-1x always-on. ~$4/mo.
- Postgres: Fly Managed Postgres, 1GB volume.

**Why some pages may take a moment on first hit:** Both Django machines auto-stop when idle to save resources; the first request after idle takes 1-2 seconds while Fly wakes the machine. Keycloak stays always-on so login is instant.
