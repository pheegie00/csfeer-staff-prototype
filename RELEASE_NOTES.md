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
| CORE-41, 42, 70, 157 (Email notifications) | Deferred | Batch D. Needs SMTP infrastructure spike (will use `thebusinessofdelivery@gmail.com` for test sends per memory rule). |
| CORE-28 (Document new form template pattern) | Pending | Doc-only, needs to be written after Form Builder feedback. |
| Phase II form schemas | Placeholders | The 16 newly seeded Phase II + OFA form templates have `{}` schemas. Schema editor UI is a Phase 6 deliverable. |

---

## Technical reference

**Test suite:** 170 tests, all passing on the deployed branch.

**Deployment architecture:**
- `acf-core` (Fly.io, iad region): Django 6.0.4 + gunicorn, 2 shared-cpu-1x machines, auto-stop on idle, Postgres attached.
- `acf-core-keycloak` (Fly.io, iad region): Keycloak 26.4 + H2 (in-memory; realm re-imports on every boot from baked-in JSON), 2GB shared-cpu-1x always-on. ~$4/mo.
- Postgres: Fly Managed Postgres, 1GB volume.

**Why some pages may take a moment on first hit:** Both Django machines auto-stop when idle to save resources; the first request after idle takes 1-2 seconds while Fly wakes the machine. Keycloak stays always-on so login is instant.
