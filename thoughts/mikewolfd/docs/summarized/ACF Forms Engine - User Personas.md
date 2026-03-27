# ACF Forms Engine - User Personas (Synthesized)

Six personas spanning three role tiers -- tribal grantee staff (Approver, Contributor, Viewer), OCS federal program officers, and system administrators (ACF + contractor) -- define the user base. The personas surface concrete workflow constraints (intermittent connectivity, multi-system data re-entry, batch review of 15-25 grantees) that directly shape architecture and UX priorities.

---

## Additions & Nuances Beyond Core Context

- **Viewer role** exists alongside Contributor and Approver; core context mentions collaboration but not a read-only access tier. The Viewer persona (Council Liaison) needs dashboard status, PDF export, and attachment tracking -- no edit capability.
- **SF-424M cross-referencing** is a recurring pain point: tribal users must ensure CSFEER data is consistent with data entered separately in OLDC/SF-424M (award amount, UEI, project period). In-context guidance tying fields to their SF-424M counterparts is called out.
- **Short Form** is mentioned as a distinct tribal submission type alongside Tribal Plan & Application and Annual Report. Core context lists only Plan + Annual Report (Modules 1-3).
- **Transmittal letter / attestation** is a distinct artifact requiring signatures, upload tracking, and status visibility -- not just a form field.
- **Portfolio size**: a single OCS Program Specialist manages 15-25 tribal grantees across multiple time zones.

## Contradictions / Gaps

| Item                    | Core Context                                     | Personas Doc                                                       |
| ----------------------- | ------------------------------------------------ | ------------------------------------------------------------------ |
| Tribal submission types | Tribal Plan + Tribal Annual Report (Modules 1-3) | Also mentions **Short Form** as a distinct submission              |
| User roles              | Implies multi-person collaboration generically   | Defines three explicit access tiers: Approver, Contributor, Viewer |

---

## Grantee Workflow Constraints (Engineering Impact)

### Connectivity & Resilience
- Rural tribal users have spotty broadband; shared devices are common.
- **Requirement**: resilient auto-save + local/client-side caching to prevent data loss on connection drop. Forms must not feel "brittle" on save failure.

### Incremental Completion
- Contributors start early, return many times as data arrives from sub-programs. Approvers pause frequently for meetings, signatures, council approvals.
- **Requirement**: robust draft/partial-save support -- saving incomplete sections must not trigger blocking validation or corrupt form state.

### Pre-population & Year-over-Year Comparison
- Stable data (org info, contacts, some budget baselines) is manually re-entered every year across OLDC, CORE, and internal spreadsheets.
- Contributors want visual diff: "what changed from last year" indicators on fields.
- **Requirement**: pre-populate from prior submissions with clear editable-vs-locked distinction; expose change indicators per field.

### Validation UX
- Contributors use validation errors as a workflow cue, not just a gate. Unclear required-vs-optional-vs-rejection-causing field status is a major pain point.
- **Requirement**: inline validation with explanatory messages (e.g., "Total of Sections A-C must equal your CSBG award amount"). Clearly distinguish hard errors, warnings, and optional fields throughout the form -- not just at submission time.

### Export & Sharing
- All three grantee tiers need PDF export: Approver for leadership sign-off, Viewer for council/audit archives, Contributor for internal review.
- Leadership wants a simplified summary view (funding amount, major goals, key outcomes) separate from the full dense form.

---

## Federal Staff Workflow Constraints (Engineering Impact)

### Portfolio Dashboard
- OCS staff need a grantee-level status view: Not Started / In Progress / Submitted / Needs Correction per form per grantee.
- Current OLDC has no portfolio-level view; status tracking is done via email and spreadsheets.

### Batch Review & Export
- Program Specialists review submissions in batches, export to CSV/Excel for comparison and performance management.
- They identify outliers (major year-over-year changes) and follow up -- data comparison tooling or at minimum structured export is critical.

### Submission History
- Federal staff need access to full submission history per grantee to answer questions and prepare technical assistance.

### Validation as Workload Reducer
- A major federal staff pain point is email back-and-forth over simple data issues. Pre-submission validation directly reduces federal workload.

---

## Admin & Operations Constraints (Engineering Impact)

### User & Role Management
- Admin manages both grantee and internal staff accounts; clear separation required for ACF security compliance.
- Current process spans multiple systems (OLDC admin, email, spreadsheets). Need unified admin console with search by org/person/email/UEI, few-click role changes, and audit logging.
- Manual provisioning/deprovisioning is error-prone -- signals need for streamlined or partially automated onboarding flow.

### Observability
- Admin wants high-level analytics: failed logins, common validation errors, feature-correlated support tickets.
- Contractor/DevOps needs clear error codes and structured logs for saves, submissions, and auth events.
- Hard to reproduce issues under real-world low-connectivity conditions -- test environments should simulate degraded networks.

### Operational Resilience
- Peak load around reporting deadlines (Tribal Plan due dates, Annual Report due March 31). System stability during these windows is non-negotiable.
- Feature flags / runtime configuration to handle policy or OMB form changes without full redeploys.
- ATO artifact generation: system logs, change documentation, incident records must be extractable for security audits.

---

## Role-Permission Matrix (Derived)

| Capability          | Approver | Contributor | Viewer | OCS Staff       | Admin |
| ------------------- | -------- | ----------- | ------ | --------------- | ----- |
| Edit form sections  | Yes      | Yes         | No     | No              | No    |
| Submit / attest     | Yes      | No          | No     | No              | No    |
| View form data      | Yes      | Yes         | Yes    | Yes (read-only) | Yes   |
| Export PDF/CSV      | Yes      | Yes         | Yes    | Yes             | Yes   |
| Portfolio dashboard | No       | No          | No     | Yes             | Yes   |
| Manage users/roles  | No       | No          | No     | No              | Yes   |
| View audit logs     | No       | No          | No     | Limited         | Yes   |
