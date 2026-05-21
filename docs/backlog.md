# Backlog (proposed Jira tickets)

Items below are scoped-but-not-yet-filed. File in Jira when prioritized.
Each gets a CORE-xxx ticket number on file.

## Multi-program scaling (research output -- see `multi_program_architecture.md`)

### Architectural foundation (cheap now, expensive later)

- **STAFF-MP-01: Add `Program` + `ACFOffice` models**
  - Story: As a platform owner, I want every form and submission attributable
    to a specific ACF program and office so that staff permissions, queues,
    and reporting can be scoped per program.
  - Acceptance: `programs` app exists with `ACFOffice` and `Program` models;
    `FormDefinition.program` FK added; seed data for OCS->CSBG and OFA->TANF /
    Tribal_TANF / HMRF / HPOG (HPOG marked inactive); existing FormDefinitions
    backfilled to CSBG.
  - Priority: HIGH -- blocks every multi-program scenario.

- **STAFF-MP-02: Add `org_type` to `OrganizationProfile`**
  - Story: As a federal staff member, I want to filter and group recipients
    by organization type (Tribe / State / Territory / Higher Ed / CBO /
    Faith-Based / Workforce Agency) so that program-specific queues match
    program-specific recipient mixes.
  - Acceptance: `OrganizationProfile.org_type` field with 8 choices added;
    existing orgs backfilled to "Tribe"; staff_review Inbox supports filtering
    by org_type.
  - Priority: MEDIUM -- needed before HMRF (mixed org types) or TANF (state-
    dominant).

- **STAFF-MP-03: Add `cycle_type` to `FormDefinition`**
  - Story: As a federal staff member, I want each form to declare whether
    it's annual / quarterly / monthly / ad-hoc so that submission windows
    and reporting reflect the real cycle.
  - Acceptance: `FormDefinition.cycle_type` choices field; submission window
    (CORE-25 follow-up) calculates per-cycle.
  - Priority: MEDIUM -- ACF-196R is quarterly; misclassifying as annual will
    surface bad data.

- **STAFF-MP-04: Scope staff permissions to assigned programs**
  - Story: As an OCS staff member, I should not see OFA submissions, and
    vice versa.
  - Acceptance: `UserProgramAssignment(user, program, role)` model added;
    `staff_review.views.InboxView.get_queryset()` filters by user's assigned
    programs; permissions reusable across programs.
  - Priority: HIGH -- required as soon as program #2 (TANF) lands.

### TANF-specific forms (per OFA grant program research)

- **STAFF-MP-10: Add TANF Form Family enums**
  - Add `TANFFinancialForms`, `TANFDataForms`, `TANFMOEForms` to
    `form_manager/constants.py`. Wire ACF-196R, ACF-199, ACF-209, ACF-204,
    ACF-202.
  - Depends on: STAFF-MP-01.

- **STAFF-MP-11: Add SF-424 shared form template**
  - SF-424 is used across all programs as the standard federal application.
    Should be a shared FormDefinition reusable by any program (not duplicated).
  - Depends on: STAFF-MP-01.

- **STAFF-MP-12: Implement ACF-196R schema (Tribal TANF Financial Report)**
  - Quarterly financial reporting from Tribal TANF grantees. Schema in
    `form_manager/schema/forms/tanf_196t/`.
  - Depends on: STAFF-MP-03 (quarterly cycle), STAFF-MP-10 (form family).

### HMRF + HPOG + Coordination (deferred until OFA strategy clear)

- **STAFF-MP-20: Decision -- replace, mirror, or aggregate nFORM 2.0?**
  - HMRF grantees currently use nFORM 2.0 for performance measure data. CORE
    needs a strategic decision before building HMRF screens.
  - Output: ADR-002.

- **STAFF-MP-21: Decision -- replace, mirror, or aggregate TANF Data Portal + OLDC?**
  - TANF financial + data reports go through OLDC (GrantSolutions) and TANF
    Data Portal today.
  - Output: ADR-003.

## Phase 3 (in-flight) -- not multi-program

These are sequenced from current Phase 3 plan:

- **Step 1: Wire CORE-167 rationale flow to FormAuditTrail writes.**
  Currently saves to session + toasts. Should write
  `FormAuditTrail(action='edit_on_behalf', rationale=...)` + child
  `FormAuditDetail` rows per changed field.

- **Step 2a: Build CORE-46 CSV export of resolved submissions.**
  Scoped by form_type + fiscal year. Resolved-only.

- **Step 2b: Build CORE-47 system-wide tamper-evident audit log viewer.**
  FISMA / NIST 800-53 compliance.

- **Step 3: Add Kanban + Card Inbox views.**
  Parity with prototype's 3 view modes.

- **Step 4: Deploy `staff_review` Django app to Render.**
  Demo URL alongside the React prototype.

## Other tickets surfaced during this work

- **STAFF-MISC-01: Activity log full drawer**
  Currently inline expandable in the rail. Prototype has a full right-side
  drawer with filter chips. Translate that.

- **STAFF-MISC-02: Bulk operations on Inbox rows**
  Prototype doesn't show this. Real federal staff workflow likely needs
  bulk-return, bulk-assign-reviewer, bulk-export.

- **STAFF-MISC-03: Federal Staff archive flow (CORE-132)**
  Permission added (`staff_archive_submission`) but no UI yet.
