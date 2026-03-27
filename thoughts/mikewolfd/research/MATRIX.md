# CSFEER Requirements Matrix

> **Scope:** Requirements extracted exclusively from Confluence export documents.
> **System Requirements Sources:** S01-S11, S13-S15, S23, S26, S29 (contractual, program, and regulatory). Internal team sources moved to Project Context § Internally-Sourced Requirements.
> **Lineage:** Every requirement traces to one or more source documents (see [Appendix A](#appendix-a-source-document-registry)) with specific details.
> **Status:** REVIEWED — source-verified via 12 parallel agent reviews against all 30 source documents. S31-S39 (internal team docs) incorporated into Project Context. WS lineage analysis applied (DA-15, FE-47, AD-13, UP-12 added; 4 note expansions).
> **Date:** 2026-03-03 (reviewed 2026-03-02, source-restricted 2026-03-02, S31-S39 incorporated 2026-03-02, WS lineage 2026-03-03)

## Glossary

| Abbreviation | Meaning |
|---|---|
| ACF | Administration for Children and Families (HHS division) |
| ATO | Authority to Operate — federal security certification required before launch |
| CSBG | Community Services Block Grant — the federal grant program |
| CUI | Controlled Unclassified Information — sensitive but not classified data |
| FedRAMP | Federal Risk and Authorization Management Program — cloud security standard |
| FIPS | Federal Information Processing Standards — encryption requirements |
| FISMA | Federal Information Security Modernization Act — security compliance framework |
| NGSC | Next Generation Security Cloud — ACF's AWS hosting environment |
| NIST | National Institute of Standards and Technology — sets security standards |
| OCS | Office of Community Services — the ACF office that runs CSBG |
| OLDC | Online Data Collection system — the legacy system CORE replaces |
| PIA | Privacy Impact Assessment |
| SF-424M | Standard federal grant application form; tribes cross-reference fields against it |
| SORN | System of Records Notice — required Privacy Act documentation |
| UEI | Unique Entity Identifier — the key that links an organization across federal systems |
| USWDS | United States Web Design System — federal UI component library |
| VPAT | Voluntary Product Accessibility Template — accessibility conformance report |
| WCAG | Web Content Accessibility Guidelines — the accessibility standard (target: AA level) |

## Legend

| Field | Meaning |
|-------|---------|
| **ID** | Category prefix + sequence number |
| **Priority** | M=Must, S=Should, C=Could, W=Won't (for MVP) — where inferrable from sources |
| **Source** | Source document ID(s) from [Appendix A](#appendix-a-source-document-registry), with section references where applicable. `L###` = PWS line number (PWS ADMIN/OCS/CSBG/CSFEER v2, Rev 2, August 25, 2025). |
| **Conflict** | Cross-document disagreements flagged for resolution |

Priority is assigned based on language in source documents (e.g., "must," "required by law," "out of scope for MVP"). Where no priority language exists, priority is marked `?`.

---

## System Requirements

### 1. Form Engine Core (FE)

#### 1.1 Form Field Types & Data Entry

| ID | Requirement | Priority | Source | Notes |
|----|-------------|----------|--------|-------|
| FE-01 | Manual data entry: open fields for user-entered values | M | [S29] §2.0 Form Field Types L129 |  |
| FE-02 | Auto-calculated fields using formulas based on other inputs | M | [S29] §2.0 Form Field Types L130 |  |
| FE-03 | Pre-population: data that connects forms from pre-award to post-award | M | [S29] §2.0 Form Field Types L131 |  |
| FE-04 | Conditional fields and branching questions | M | [S29] §2.0 Form Field Types L137 |  |
| FE-05 | One-to-many response types (multiple responses per question) | M | [S29] §2.0 Form Field Types L138 |  |
| FE-06 | File attachment fields stored with submission | M | [S29] §2.0 Form Field Types L136 |  |
| FE-12 | Reduce compatibility issues and variability from custom State/Tribal plans and third-party-enabled State annual reports | M | [S29] Top Problems to Solve |  |

#### 1.2 Validation

| ID | Requirement | Priority | Source | Conflict |
|----|-------------|----------|--------|----------|
| FE-20 | Flexible validation rules engine for calculations or comparisons to prior form submissions | M | [S29] §2.0 Validation L133 |  |
| FE-21 | Hard errors (blocking) and warning/notification validations | M | [S29] §2.0 Validation L134 |  |
| FE-22 | Field-level, field-group-level, and form-level validation | M | [S29] §2.0 Validation L135 |  |
| FE-23 | Automated data validation using business logic during form completion | M | [S29] Top Problems to Solve |  |
| FE-24 | Automated comparison to integration data (e.g., UEI mismatches via SAM.gov) | ? | [S29] Top Problems to Solve; [S37] | Same list as FE-23; no basis in [S29] to differentiate priority; [S37] specifies SAM.gov as external registry |
| FE-25 | **CONFLICT — Validation timing:** During data entry vs. review-page-only | M | [S29] §2.0 Validation — "while a grant-recipient fills out a form" | **Resolution needed.** [S29] implies inline feedback during entry. Implementation spec [S21] proposes review-page-only validation with partial saves of invalid data. |

#### 1.3 Version Control & Data Integrity

| ID | Requirement | Priority | Source | Notes |
|----|-------------|----------|--------|-------|
| FE-30 | Multiple simultaneous form versions maintaining existing submission data | M | [S29] §2.0 Version Control L113 |  |
| FE-31 | Robust version history: federal staff can view submission state at various workflow points | M | [S29] §2.0 Version Control L115 |  |
| FE-32 | Historical comparison: recipients view past submissions comparatively | M | [S29] §2.0 Version Control L116 |  |

#### 1.4 Form Builder

| ID | Requirement | Priority | Source | Notes |
|----|-------------|----------|--------|-------|
| FE-40 | Low-code/no-code form builder for non-technical staff | C | [S29] §2.0 Accessibility & Design L162 — "after year 1" | Explicitly out of MVP scope per [S21] |
| FE-41 | Sandbox/testing space for form builder | C | [S29] §2.0 Accessibility & Design L162 | Post-year-1 |
| FE-42 | Enable new forms to be designed, updated, and tested more quickly by program staff | M | [S29] Top Problems to Solve | Long-term goal; MVP uses hard-coded Python schemas |

### 2. Form Submission Workflow (WF)

| ID | Requirement | Priority | Source | Conflict |
|----|-------------|----------|--------|----------|
| WF-01 | Auto-create and initialize forms for recipients with pre-populated data based on reporting schedules | M | [S29] §2.0 Workflow L120 |  |
| WF-02 | Show trends over time using previous year data | M | [S29] §2.0 Workflow L120 |  |
| WF-04 | Recipients can "unsubmit" forms | M | [S29] §2.0 Workflow L122 |  |
| WF-05 | Recipients can submit revisions to submitted forms | M | [S29] §2.0 Workflow L122; [S24] Req #8 | Absorbs WF-08 |
| WF-09 | Customizable multi-step, multi-person federal review and approval | M | [S29] §2.0 Workflow L123 | **Out of MVP scope** per [S21] |
| WF-10 | Visual/no-code workflow builder for review processes | C | [S29] §2.0 Workflow L123 — "ideally managed through a visual/no-code workflow builder" | Post-MVP; "ideally" = aspirational, not a Should |
| WF-11 | Save progress and return later to make revisions | M | [S29] §2.0 User Experience L172; [S29] Task Area 2 | Absorbs AD-07; [S21] confirms partial saves with invalid data allowed |
| WF-12 | Previously submitted data available in forms to limit repeat data requests | M | [S29] §2.0 User Experience |  |
| WF-13 | Customizable real-time alerts and notifications linked to workflow events | M | [S29] §2.0 Workflow L124 | **Out of MVP scope** per [S21] |
| WF-14 | Deadline-aware notifications | M | [S29] §2.0 Collaboration & Workflow Mgmt L124 — "deadlines and notifications"; [S29] §2.0 Workflow — "form past due" in notification examples |  |
| WF-15 | Workflow for multiple users entering data into one form, routing, updating/returning for re-submission | M | [S29] §2.0 Workflow L121; §2.0 Collaboration | Absorbs WF-03; **Out of MVP scope** per [S21] |
| WF-17 | Tracking and collaboration visibility on forms between program staff, lead agencies, and sub-recipients across submission, review, and revision lifecycle | M | [S29] Top Problems to Solve | CQI (Continuous Quality Improvement) sprints are a specific collaboration workflow consuming this visibility ([S03], [S05]) |
| WF-18 | March 31 statutory submission deadline for CSBG Annual Reports per CSBG Act §678(b) | M | [S15] — "ensures grant recipient compliance as outlined in Section 678(b) of the CSBG Act" | Recurring annual deadline; system should enforce/notify per WF-14 |

### 3. Authentication & Security (AS)

| ID | Requirement | Priority | Source | Conflict |
|----|-------------|----------|--------|----------|
| AS-01 | Authentication with Login.gov | M | [S29] §2.0 Security L142 |  |
| AS-03 | Government users authenticate via `login.acf.gov` (Okta), NOT Login.gov directly | M | [S10] | Nuance missing from [S29]; gov vs non-gov distinction |
| AS-04 | Non-government users have separate authentication path (TBD) | ? | [S10] | **Risk documented** — could delay development or require rework |
| AS-14 | ATO within 18 months | M | [S29] §2.0 Security L143 |  |
| AS-16 | SORN (Systems of Records Notice) required | M | [S29] §2.0 Security L144 |  |

#### 3.1 ATO Artifacts

| ID | Artifact | Status (as of Feb 2026) | Owner | Source |
|----|----------|------------------------|-------|--------|
| AS-A4 | System Security Plan (SSP) | In Progress (2026-02-23) | — | [S08] |
| AS-A11 | Security Assessment Plan | In Progress | — | [S08] |
| AS-A12 | Appendix X (controls implementation) | In Progress | — | [S08] — "as much effort as all other ATO docs combined" |
| AS-A13 | Interconnection Security Agreement (ISA) | In Progress (ACF template sent) | — | [S08] |
| AS-A14 | Plan of Action and Milestones (POAM) | In Progress (ACF template sent) | — | [S08] |

> See Project Context § Internally-Sourced Requirements for full ATO artifact inventory from [S12] compliance tracker, including FISMA baseline conflict.

### 4. Integration & Data (DA)

| ID | Requirement | Priority | Source | Conflict |
|----|-------------|----------|--------|----------|
| DA-01 | Flexible read API for forms, submissions, and bulk data extraction | M | [S29] §2.0 Integration L148 | **Out of MVP scope** per [S21] |
| DA-02 | Write API to import pre-populated data | M | [S29] §2.0 Integration L149 | **Out of MVP scope** per [S21] |
| DA-03 | Data exports via API, CSV, and human-readable formats | M | [S29] §2.0 Integration L150 |  |
| DA-04 | Export individual form submissions as PDFs | M | [S29] §2.0 Integration L151 |  |
| DA-05 | Generate public-access links to specific portions of a submission | ? | [S29] §2.0 Integration L152 | No [S29] language differentiates priority from adjacent items; was S without basis |
| DA-06 | Comprehensive, easy-to-understand API documentation | M | [S29] §2.0 Integration L153 |  |
| DA-07 | Real-time data access that doesn't hinder application performance | M | [S29] Top Problems to Solve |  |
| DA-09 | Data exports feed Performance Management website (Monique Alcantara is COR) | ? | [S05]; [S03] | Downstream consumer not in [S29]; congressional reporting is primary downstream workflow — Melanie manages all congressional reporting ([S03]); data flows: exports → PM website → Congress ([S01], [S29]) |
| DA-10 | OLDC DataConnect or Excel exports as data migration source | ? | [S13] — "Ideal: OLDC DataConnect from GS; Alternative: Excel exports" |  |
| DA-12 | Existing XML/XSD validation artifacts from SmartForms available as reference | ? | [S13] | "Migration input" was an inference; source only lists the artifact attachment |
| DA-13 | FY24 raw data exports exist (State Plan, Modules 1/2/4) for schema reference | ? | [S14] — RVW/RPT prefix naming convention |  |
| DA-14 | Enable program staff to easily export, review, and correct data errors (missing data, data conflicts, new elements) | M | [S29] Top Problems to Solve |  |
| DA-15 | Conditional-logic-aware PDF/print export: omit non-applicable sections from output | ? | [S03] — "business logic built in, but when they print it, it shows everything (even questions that weren't applicable) - hard to read" |  |

### 5. Accessibility & Design (AD)

| ID | Requirement | Priority | Source | Notes |
|----|-------------|----------|--------|-------|
| AD-01 | Section 508 WCAG AA-compliant front end | M | [S29] §2.0 Accessibility & Design L162 |  |
| AD-02 | USWDS (United States Web Design System) as design system | M | [S29] §2.0 Accessibility & Design L162 — "ideally using" USWDS | [S29] uses "ideally" for USWDS specifically; 508 AA is the hard requirement |
| AD-05 | Clear information about user's location in multi-step process | M | [S29] Task Area 2 — "Give users clear information about where they are" |  |
| AD-06 | Plain, familiar language throughout the service | M | [S29] Task Area 2 |  |
| AD-08 | Consistent visual identity with agency branding | S | [S29] Task Area 2 |  |
| AD-09 | Low-bandwidth/rural environment support | ? | [S06] — Alaska named explicitly | Priority was M per [S24]; needs re-evaluation with allowed sources only. Note: [S06] also documents zero-connectivity on-site assessment scenarios (ANA), which exceeds "low-bandwidth" — gap between AD-09 and full offline capability |
| AD-13 | In-context field guidance and companion document integration (extends UP-02) | ? | [S06] — "Form itself does not include the substantial context that comes with very lengthy instruction and guide documents"; [S32] | Broader than SF-424M cross-ref (UP-02): field-level help, section instructions, 62–150 page companion docs |

### 6. Permissions & User Management (PM)

| ID | Requirement | Priority | Source | Conflict |
|----|-------------|----------|--------|----------|
| PM-01 | Flexible permissions: read, write, and export controls | M | [S29] §2.0 Permissions L177 |  |
| PM-02 | Self-service user management: recipients manage their own users and permissions | M | [S29] §2.0 Permissions L178 |  |
| PM-03 | Hierarchical administration: sub-recipient, state, and federal levels | M | [S29] §2.0 Permissions L178 |  |
| PM-04 | Minimum permission levels: read-only, write-only, approve at each level | M | [S29] §2.0 Permissions L179 |  |
| PM-05 | Varying permission levels: view-only, view+edit, view+submit | M | [S29] Objective — "varying permission levels" |  |
| PM-06 | 75 federal staff with review, route, approve, analyze, compare, export capabilities | M | [S29] Objective — scale assumption |  |
| PM-07 | Roles and permissions managed through Okta groups syncing with application | ? | [S10] | Implementation approach |
| PM-08 | Authorization and access control | M | [S29] §2.0 Permissions | **Out of MVP scope** per [S21] — **CONFLICT** |

### 7. Performance & Reliability (PR)

| ID | Requirement | Priority | Source | Notes |
|----|-------------|----------|--------|-------|
| PR-02 | Scalable to 1,100 grant recipients + sub-recipients + 75 federal staff | M | [S29] Objective |  |
| PR-04 | Real-time system resource utilization monitoring | M | [S29] Task Area 2 — "Use data to drive decisions" |  |
| PR-05 | Real-time performance monitoring: response time, latency, throughput, error rates | M | [S29] Task Area 2 |  |
| PR-06 | Median, 95th percentile, and 98th percentile performance measurement | M | [S29] Task Area 2 |  |
| PR-07 | Track concurrent users in real-time | M | [S29] Task Area 2 |  |
| PR-08 | Monitor user behaviors in aggregate | S | [S29] Task Area 2 |  |
| PR-09 | Multivariate/A/B testing support in production | C | [S29] Task Area 2 — "as needed" |  |
| PR-10 | 24/7 operational availability | M | [S29] Task Area 3 L349 — "operational 7 days per week, 24 hours per day" |  |

---

## MVP Definition

### 8. Success Criteria (SC)

| ID | Criterion | Source | Conflict |
|----|-----------|--------|----------|
| SC-01 | 20+ Tribal grant recipients submit via CORE without reverting to PDFs | [S24] Obj 1 KR; [S21] Goal 1 | **Conflicts with other sources suggesting 10-12 pilot cohort** |
| SC-02 | ≥80% of users report digital experience is easier than PDFs | [S24] Obj 3 KR; [S21] Goal 3 (item 3.i) |  |
| SC-03 | 100% Section 508 compliance | [S24] Obj 3 KR; [S39] | VPAT verification required per AD-11; also AC criterion |
| SC-04 | Zero ACF OCIO security or compliance findings | [S24] Obj 3 KR |  |
| SC-05 | Architecture documentation complete for Phase II | [S24] Obj 2 KR |  |
| SC-06 | Platform supports both simple and complex forms | [S24] Obj 2 |  |
| SC-07 | Establish first measurable baseline for Tribal reporting performance | [S24] — "CORE provides the first measurable baseline" |  |

### 9. Form Inventory (FI)

| ID | Form Name | Phase | Users | Source |
|----|-----------|-------|-------|--------|
| FI-01 | CSBG Tribal Plan and Application | Phase I | ~66 | [S29] Phase I; [S13] |
| FI-02 | CSBG Tribal Annual Report | Phase I | ~30 (up to 66) | [S29] Phase I; [S13] | [S29] uses "CSBG Tribal Annual Report (OMB Approved Form)"; "(Long Form)" is informal shorthand. Tribal reports have 3 modules (not 4): M1=Tribal Admin, M2=Tribal Expenditures, M3=Individual/Family. |
| FI-03 | CSBG Tribal Annual Report [Short Form] | Phase I | ~30 (up to 66) | [S29] Phase I; [S13] — $50k funding threshold determines which form | [S29] uses bracket notation [Short Form] |
| FI-04 | CSBG Eligible Entity List | Phase II | — | [S29] Phase II — OMB Approved **Doc** (not Form) |
| FI-05 | CSBG State and Territory Plan | Phase II | 53+ | [S29] Phase II |
| FI-06 | CSBG Annual Report 3.0 (Modules 1-4) | Phase II | 53+ | [S29] Phase II; [S15] — Modules: M1=State Administration, M2=Agency Expenditures/Capacity/Resources, M3=Community Level, M4=Individual and Family Level | M3 and M4 were previously swapped; corrected per [S15] (IM #152). M1 completed by state lead agencies; M2-M4 by eligible entities. |

> **Note:** $50,000 funding threshold determines whether tribes submit FI-02 (Long) or FI-03 (Short) — this is **mandatory based on allocation**, not a choice. Source: [S15]

> **Note:** PRA approval status is an operational dependency for form publishing. Melanie Durley manages PRA for approximately half the forms; Monique Alcantara for the other half ([S03], [S05]). CSBG Annual Report PRA was "in progress" as of export date ([S13]). System implication: form administration needs PRA status visibility.

---

## Project Context

### Implementation Decisions

Technical design decisions from [S21] (Form Manager Tech Spec), [S27] (Okta Auth Tech Spec), [S18] (Tech Stack), and [S31] (Q1 2026 Plan). These describe HOW the system implements the requirements above, not WHAT it must do. Items retain their original IDs for traceability.

#### Form Engine

| ID | Decision | Source | Notes |
|----|----------|--------|-------|
| FE-08 | Interview-style page-by-page data entry flow via POST | [S21] | Implements FE-01 through FE-07 |
| FE-09 | JSON field storage for form entry data in FormEntry model | [S21] |  |
| FE-10 | Python/Pydantic schemas as single source of truth for UI structure, validation rules, and UX definition | [S21] | Schema has 3 parts: metadata, Django Form class, UX definition |
| FE-11 | FormDefinition records contain schema class name linking to Python schema | [S21] |  |
| FE-33 | Form status lifecycle: draft → submitted → amended → archived | [S21] | "amended" = revision after submission; "archived" = available but hidden from user view |
| FE-35 | Detailed field-level change logging via FormAuditDetail model | [S21] | Extends FE-34 (audit trail requirement) |
| FE-36 | Short form variant derived from long form base with simplified field set | [S31] | Clarifies FI-02/FI-03 relationship; UI must differentiate variants |
| FE-37 | Cross-form pre-population: Tribal Plan pre-populates from Tribal AR data | [S31] | Extends FE-03; requires shared field identifiers across form schemas |
| FE-38 | Periodic auto-save every 30-60 seconds with success/failure messaging | [S31] | Implements WF-11; implies debounced persistence and conflict handling |
| FE-39 | PDF generation uses review page data, not raw form data | [S31] | Clarifies DA-08; review page aggregation is a dependency for PDF export |
| FE-43 | Screener flow: routing UI after login that determines which form a user fills out | [S36] | Form-selection component; not in prior context |
| FE-44 | Client-side caching via IndexedDB/localStorage for connection resilience; sync on reconnect | [S36] | Prescribed browser storage APIs; requires service worker or connection-monitoring layer |
| FE-45 | Three connection state indicators: "Saved", "Connection lost — work stored locally", "Reconnected — sync successful" | [S36] | Implements AD-09/PR-14 low-connectivity UX |
| FE-46 | UEI (Unique Entity Identifier) as cross-form pre-population key | [S36] | Extends FE-03/FE-37; Authorized Official inputs UEI-keyed data |
| FE-47 | Concurrent edit conflict handling for periodic auto-save (extends FE-38) | [S21] — "Simultaneous multi-user editing" listed as known concern |  |

#### Authentication

| ID | Decision | Source | Notes |
|----|----------|--------|-------|
| AS-05 | Authorization Code Flow with PKCE + client secret; all token handling server-side (browser receives only Django session cookie) | [S27] | Implements AS-01/AS-02 auth requirements |
| AS-06 | Keycloak (`oauth.csfeer:8081`) for local development mock | [S27] | Realm: `csfeer`, client: `csfeer-auth` |
| AS-07 | Role-to-group mapping from JWT `realm_access.roles` claims | [S27] | **Critical open question** — will Okta/Login.gov token emit roles in `realm_access.roles` structure (Keycloak convention), or will backend need updating for different claim structure? |
| AS-08 | Role mappings: `csfeer_admin` → staff+superuser; `csfeer_staff` → staff; `superuser` → superuser; **any other role** → Django group created/assigned by name | [S27] | Fourth mapping carries security implications — unexpected roles auto-create groups |
| AS-09 | Token lifetimes: access 5min, session idle 30min, session max 10hr | [S27] | **Keycloak dev config values** — production Okta settings not yet confirmed |
| AS-10 | Auto-provision user (by `email` claim), OrganizationProfile, and UserOrganizationMembership (role: `admin`) on first login; store `sub` claim in `UserProfile.oidc_user_id` | [S27] |  |
| AS-11 | Group memberships cleared and re-synced from token on every login | [S27] |  |
| AS-12 | RP-initiated logout with Okta session termination | [S27] |  |
| AS-18 | MVP uses basic session management without Login.gov; Login.gov integration deferred | [S31] | Story 1.3; clarifies AS-01 is not in MVP scope |

#### Data

| ID | Decision | Source | Notes |
|----|----------|--------|-------|
| DA-08 | PDF generation via WeasyPrint (HTML/CSS to PDF) | [S18] | Implements DA-04; **conflicts** with any "headless Chrome" references |

### Internally-Sourced Requirements

Requirements identified from internal team documents, implementation specs, and project management artifacts (S12, S16-S22, S24, S27). These represent team consensus or internal specifications not yet traced to contractual or program authority. Items retain their original IDs for traceability.

#### Form Engine

| ID | Requirement | Priority | Source | Notes |
|----|-------------|----------|--------|-------|
| FE-07 | Support both simple and complex forms (complexity spectrum) | M | [S24] Obj 2 |  |
| FE-34 | Audit trail for all form actions by user | M | [S24] Req #19; [S21] — FormAuditTrail model |  |
| [WS-01] | Data sensitivity classification per field | ? | Derived: AS-20 (CUI) + PM-01 (access controls) imply per-field tiers | Stretch |
| [WS-02] | PRA metadata per form (OMB number, expiration, burden) | ? | Derived: FI-01–FI-06 + [S03], [S05], [S13] PRA notes | Operational dependency; stretch |
| [WS-03] | Schema-driven definitions decoupled from hardcoded UI | ? | Derived: FE-10 + FE-42 + FE-40 | Direction for post-MVP form builder |

#### Workflow

| ID | Requirement | Priority | Source | Notes |
|----|-------------|----------|--------|-------|
| WF-06 | Submit a form (distinct action) | M | [S24] Req #5 |  |
| WF-07 | Submit a report (distinct from form?) | ? | [S24] Req #7 | May be duplicate of WF-06; early conceptual distinction |
| WF-16 | Four-stage deliverable approval: draft → gov't comments → final → GTM/COR acceptance | ? | [S16]; [S17] | **Misplaced** — contract deliverable workflow, not form submission; belongs in § 12 governance |
| [WS-07] | Conditional routing based on submission attributes (e.g., budget threshold triggers CFO step) | ? | Derived: [S37] open question | Post-MVP; depends on WF-09 |
| [WS-08] | Parallel approval branches with join logic | ? | Derived: [S37] open question | Post-MVP; depends on WF-09 |
| [WS-09] | Delegation and escalation rules for review workflows | ? | Derived: [S37] open question | Post-MVP; depends on WF-09 |

> **Review Workflow Open Questions** (from [S37], PWS analysis — unresolved design decisions for WF-09/WF-10):
> Sequential vs. parallel review steps? | Conditional routing (e.g., budget threshold triggers CFO step)? | Unanimous vs. any-one-approves per step? | Who configures workflows — IT, program managers, or end users? | Delegation and override rules? | Reviewer permission tiers (view-only / comment / final approve)?

#### Authentication & Security

| ID | Requirement | Priority | Source | Notes |
|----|-------------|----------|--------|-------|
| AS-02 | OIDC via Okta (`acf.okta.com`) as identity broker | M | [S27] |  |
| AS-13 | Client secret must be stored in secrets manager (e.g., AWS Secrets Manager); rotation schedule TBD | M | [S27] | Storage is M ("must never be hardcoded"); rotation schedule is S |
| AS-15 | ATO target date: May 29, 2026 | M | [S12] | Specific milestone from compliance tracker |
| AS-17 | PIA (Privacy Impact Assessment) required | M | [S12] — status "UNDER REVIEW" as of 2026-02-09 | [S29] §2.0 Security does NOT mention PIA; sourced from ATO process only |
| AS-19 | Zero Trust strategy required per EO 14028 | M | [S33] | Contractor must provide ZT strategy |
| AS-20 | CUI handling per NIST standards for Controlled Unclassified Information | M | [S33] |  |
| AS-21 | AI policy: federal data cannot train commercial AI models without approval | M | [S33] | Must comply with US law + ACF policy |
| AS-22 | Personnel security: background investigations, NDAs, annual security/privacy/records training | M | [S33] |  |
| AS-23 | High-risk Public Trust clearance required for contractor staff | M | [S34] | PWS page 40/67; affects onboarding timelines for new team members |
| AS-24 | Incident response SLAs: Critical <1hr, High <4hrs, Medium <24hrs, Low <72hrs | M | [S35] |  |

#### ATO Artifacts (from [S12] compliance tracker)

| ID | Artifact | Status (as of Feb 2026) | Owner | Source |
|----|----------|------------------------|-------|--------|
| AS-A1 | ACF System Registration Form | COMPLETED (2026-01-27) | Diana Rosner (CTR) | [S12] |
| AS-A2 | Privacy Impact Assessment Form | UNDER REVIEW (2026-02-09) | Ablavi Zolome (CTR) | [S12] |
| AS-A3 | System-Categorization | UNDER REVIEW (2026-02-20) | Oyindasola Akisanmi (CTR) | [S12] |
| AS-A5 | Business Impact Analysis (BIA) | Unknown (blank in tracker) | — | [S12] |
| AS-A6 | Incident Response Plan (IRP) | Unknown (blank in tracker) | — | [S12] |
| AS-A7 | Contingency Plan | Unknown (blank in tracker) | — | [S12] |
| AS-A8 | Configuration Management Plan | Unknown (blank in tracker) | — | [S12] |
| AS-A9 | E-Authentication Agreement | Unknown (blank in tracker) | — | [S12] |
| AS-A10 | Selected Controls Rev5-Low_System | Unknown (blank in tracker) | — | [S12] |

> **CONFLICT (AS-A10):** [S12] references **Rev5-Low** baseline controls. [S29] and other docs imply **FISMA Moderate**. Resolution needed. See also C-3 in Open Conflicts.

#### Integration & Data

| ID | Requirement | Priority | Source | Notes |
|----|-------------|----------|--------|-------|
| DA-11 | Pre-population limited to "high-confidence data only" for MVP | ? | [S16]; [S17] — risk mitigation strategy |  |

#### Accessibility & Design

| ID | Requirement | Priority | Source | Notes |
|----|-------------|----------|--------|-------|
| AD-04 | Optimized for tablets and laptops | M | [S24] NFR6 |  |
| AD-10 | Prototype designs may vary from implementation based on USWDS component feasibility | ? | [S20] | Implementation variance caveat |
| AD-11 | Accessibility Conformance Report (ACR) via VPAT required for any commercial ICT | M | [S33] | Gov't reserves right to independently test; remediation at contractor expense |
| AD-12 | WCAG 2.0 AA is contractual obligation; building to WCAG 2.1/2.2 AA is advisable | ? | [S33] | 2.0 is outdated; 2.1/2.2 is current standard |
| [WS-11] | Offline-first field administration (ANA, CB on-site assessment) | ? | Derived: AD-09 + FE-44 + [S06] — "ANA — offline/in-person administration needed" | Post-MVP; exceeds low-bandwidth (AD-09) into full offline |

#### Performance & Reliability NFRs

| ID | Requirement | Priority | Source | Notes |
|----|-------------|----------|--------|-------|
| PR-01 | Form load/save ≤ 3 seconds on typical 4G connection | M | [S24] NFR1 |  |
| PR-03 | ≥ 99.5% uptime excluding scheduled maintenance | M | [S24] NFR3 |  |
| PR-11 | ≥ 200 concurrent users | M | [S24] NFR2 |  |
| PR-12 | FISMA Moderate, FedRAMP hosting, FIPS 140-2 encryption | M | [S24] NFR4 | Relevant to conflict C-3: [S24] explicitly says **Moderate** |
| PR-13 | Modern browser support: Chrome, Firefox, Edge, Safari | M | [S24] NFR5 |  |
| PR-14 | Operate reliably despite poor connectivity (auto-save + local caching) | M | [S24] Req #13 | Connects to AD-09 low-bandwidth constraint |
| PR-15 | Test coverage: >80% | M | [S35] |  |
| PR-16 | 3G network testing required in addition to 4G | M | [S35] | Extends PR-01 |
| PR-17 | Form completion time target: <25 minutes | S | [S35] | UX performance metric |
| PR-19 | Support volume: <60 tickets/month | S | [S35] |  |
| PR-20 | Processing cost: <$50/form | S | [S35] |  |
| PR-21 | 75% tribal digital adoption within Year 1 | S | [S35] | Also appears as success metric |

#### Internally-Sourced Success Metrics

Detailed success metrics from [S36] (Product Spec v2.0). These extend the contractual success criteria (SC-01 through SC-07) with implementation-level targets.

| ID | Metric | Target | Source | Notes |
|----|--------|--------|--------|-------|
| SC-08 | Pilot orgs with successful submission | 100% | [S36] |  |
| SC-09 | Submissions passing validation without OCS help | ≥90% | [S35]; [S36] | Absorbs PR-18 |
| SC-10 | Errors resolved without OCS intervention | ≥85% | [S36] |  |
| SC-11 | Reduction in OCS follow-up emails | ≥30% | [S36] |  |
| SC-12 | Autosave success rate | ≥98% | [S36] |  |
| SC-13 | Data loss | 0% | [S36] |  |
| SC-14 | User satisfaction | ≥4/5 | [S36] | Relevant to C-9 — different metric than SC-02's "≥80% easier than PDFs" |
| SC-15 | Help desk tickets per org | ≤1 | [S36] |  |
| SC-16 | Submission time reduction | 12-20 days → 3-7 days | [S36] | Aspirational: <1 hour; 1,800 hrs/yr current tribal burden |
| SC-17 | Component reuse across forms | ≥70% | [S36] | Architecture metric |
| SC-18 | New form onboarding time | ≤6 weeks | [S36] | Phase II readiness metric |
| SC-19 | OCS review time reduction | ≥25% (long-term ≥50%) | [S36] |  |
| SC-20 | API uptime | ≥99.9% | [S36] | Stricter than system uptime (PR-03: 99.5%) |
| SC-21 | Form completion time reduction vs legacy PDF | ≥25% | [S39] | Different framing than SC-16 (days-based) |

**Observability by category** (day-one instrumentation required per DL-15):

| Category | Key Metrics |
|----------|-------------|
| User interaction | Sessions per submission, autosave success ≥98% (SC-12) |
| Submission quality | Validation passes without help ≥90% (SC-09), errors self-resolved ≥85% (SC-10) |
| Performance | Load/save ≤3s on 4G (PR-01), p95/p98 latency (PR-06), ≥200 concurrent users (PR-11) |
| Operational | Tickets <60/mo (PR-19), OCS review time ≥25% reduction (SC-19) |

#### MVP Acceptance Criteria (from [S39])

Concrete "done" criteria for MVP sign-off:

| ID | Criterion | Source | Notes |
|----|-----------|--------|-------|
| AC-01 | All three tribal forms available digitally with validation + save/submit | [S39] |  |
| AC-02 | Login.gov working for all pilot users | [S39] | Note: contradicts AS-18 (Login.gov deferred per [S31]); may reflect earlier planning |
| AC-03 | CSV + PDF export functional | [S39] |  |
| AC-04 | At least 10 tribal orgs successfully submit during pilot | [S39] | Lower bar than SC-01 (20+ per [S24]); connects to C-2 (pilot size) |

### 10. Infrastructure & Technology (IT)

| ID | Decision | Source | Notes |
|----|----------|--------|-------|
| IT-01 | Python 3.12, Django 6.0+ | [S18]; [S07] — "Tech stack approved" |  |
| IT-02 | PostgreSQL (NGSC AWS) | [S18]; [S09] — "proceeding with ECS and Postgres" |  |
| IT-03 | AWS ECS (not Kubernetes) | [S09] — resolves PMP vs Helm chart discrepancy |  |
| IT-04 | Alpine.js 3.15+ for frontend reactivity | [S18] |  |
| IT-05 | USWDS 3.13+ for UI components | [S18] |  |
| IT-06 | Django Ninja 1.4+ for REST APIs | [S18] | [S35] PMP says DRF — outdated; Django Ninja is actual framework |
| IT-07 | WeasyPrint 62.3+ for PDF generation | [S18] |  |
| IT-08 | Django Cotton 2.1+ for reusable template components | [S18] |  |
| IT-09 | Keycloak for local dev auth mock | [S27] — realm: `csfeer`, client: `csfeer-auth`; [S38] | [S38] notes Keycloak is being replaced (low impact); may affect mock-oauth setup |
| IT-10 | NGSC AWS as production environment | [S07]; [S09]; [S38] | ATO strategy: **inherit existing NGSC controls** (confirmed at IPT kickoff); environments: Dev/Test, Stage, Prod (lower + upper) |
| IT-11 | GitLab repository (~Feb 18, 2026) with GitHub mirroring | [S10] | Date inferred from "next Wednesday" relative to Feb 10 meeting |
| IT-12 | Jira for sprint tracking (project key "FE", RapidView 404) | [S16]; [S17] |  |
| IT-13 | Confluence for documentation | [S25] |  |
| IT-14 | Figma for design/prototyping — two boards: "ACF-Exploration" (strategy/service blueprint) and "Tribal-Forms" (clickable prototypes V1, V1.3) | [S20]; [S19] |  |
| IT-15 | Mural for process maps and research workshops | [S22]; [S03] |  |
| IT-16 | Open-source codebase preferred, using standard sustainable open-source libraries | S | [S29] §2.0 Open Source & Scalability — "preferred" | Entire [S29] subsection had no MATRIX entries |
| IT-17 | Affordable scaling of user licenses (if applicable) | ? | [S29] §2.0 Open Source & Scalability — "if applicable" |  |
| IT-18 | PIV cards + GFE required for NGSC access; Zscaler for network access management | M | [S38] | Operationally significant for CI/CD pipeline design |
| IT-19 | Parallel development: Focus builds in own environment while NGSC provisioning proceeds | — | [S38] | Timeline risk mitigation |
| IT-20 | ServiceNow ticket process for Okta/Login.gov user provisioning | — | [S38] | Operational integration path |

### 11. Risks

> R-01 through R-16. See [open-items.md § Risks](open-items.md#risks-r-01-through-r-14) for full risk register with probability, impact, mitigation, and sources.

### Delivery & Sprint Planning

| ID | Item | Target | Source | Notes |
|----|------|--------|--------|-------|
| DL-01 | Landing page deployed | 2026-03-01 | [S31] |  |
| DL-02 | Tribal Annual Report (long form) complete | 2026-03-15 | [S31] |  |
| DL-03 | Tribal Plan and Application complete | 2026-03-31 | [S31] |  |
| DL-04 | ATO documentation package submitted | 2026-03-31 | [S31] |  |
| DL-05 | Build sequence: rendering → saving → review page → auto-save → PDF export | — | [S31] | **Critical path for March 15** — no flexibility in sequence; each step depends on the previous |
| DL-06 | 192 story points across 6 epics for Q1 (~11-12 weeks, ~4.75 FTE) | Q1 2026 | [S31] | Aggressive velocity; no benchmarks stated |
| DL-07 | Shutdown-safe sequencing: ACF-independent work prioritized first | — | [S31] | Government shutdown risk mitigation |
| DL-09 | API data export endpoints designated as stretch goal | — | [S31] | May be deprioritized if forms slip; relevant to C-4 |
| DL-10 | Rural connection performance optimization as acceptance criterion for data persistence | — | [S31] | Connects to AD-09 |
| DL-11 | Soft launch to 10-12 tribal orgs with white-glove support | Month 9 | [S35] | Weekly check-ins tapering to bi-weekly; connects to C-2 (pilot size) |
| DL-12 | Wave-based full rollout of remaining orgs | Month 12 | [S35] | After ATO authorization |
| DL-13 | Stage Gates: Discovery (M2), MVP (M8), Pilot (M9), Continuous Dev (M15) | Various | [S35] | Go/No-Go decision points |
| DL-14 | ATO timeline: Planning (M1-2), Implementation (M3-8), Assessment (M9-12), Authorization (M12-13); weekly sprint stories | M1-13 | [S31]; [S35] | ATO certification is #1 risk (p×i = 0.45) |
| DL-15 | 90-day post-launch baseline telemetry: user interaction, submission quality, performance, operational metrics | Post-launch | [S36] | Requires day-one instrumentation; not post-MVP |

### User Personas & Role Model

Six personas across three tiers from [S32]. Surfaces workflow constraints that shape architecture and UX priorities. Role-permission matrix is derived, not contractual.

#### Persona-Derived Requirements

| ID | Item | Source | Notes |
|----|------|--------|-------|
| UP-01 | Three grantee role tiers: Approver (edit + submit/attest), Contributor (edit only), Viewer (read-only + PDF export) | [S32] | More specific than PM-01–PM-05; Viewer role not in prior context |
| UP-02 | SF-424M cross-referencing: in-context guidance linking CSFEER fields to their SF-424M/OLDC counterparts | [S32] | Recurring tribal pain point; data consistency across systems |
| UP-03 | Transmittal letter/attestation: distinct artifact requiring signatures, upload tracking, and status visibility | [S32] | Not just a form field; separate workflow artifact |
| UP-04 | Portfolio dashboard: grantee-level status view (Not Started / In Progress / Submitted / Needs Correction) per form per grantee | [S32] | OCS staff manage 15-25 grantees; current OLDC has no portfolio view |
| UP-05 | Batch review & structured export: CSV/Excel for cross-grantee comparison and outlier identification | [S32] | Extends DA-03; federal staff compare submissions in batches |
| UP-06 | Visual diff: per-field "what changed from last year" indicators | [S32] | Extends FE-32; contributors want change indicators on fields |
| UP-07 | Simplified summary view for leadership (funding amount, major goals, key outcomes) | [S32] | Separate from full dense form; used for council/leadership briefings |
| UP-08 | Unified admin console: search by org/person/email/UEI, few-click role changes, audit logging | [S32] | Extends PM-02; current process spans OLDC admin, email, spreadsheets |
| UP-09 | Peak load resilience around reporting deadlines (Tribal Plan dues, March 31 Annual Report) | [S32] | Extends PR-10; system stability during these windows is "non-negotiable" |
| UP-10 | Feature flags / runtime configuration for policy or OMB form changes without full redeploys | [S32] | Operational resilience; avoids redeploy for policy changes |
| UP-11 | Degraded network test environments for reproducing real-world low-connectivity issues | [S32] | Testing infrastructure; hard to reproduce issues otherwise |
| UP-12 | 4-tier support model: in-app help → help desk (email/phone) → tech escalation → on-site | [S35]; [S32] | "In-app help" tier is closest to system feature; connects to AD-13 |
| [WS-12] | Form inventory visibility (what exists, who uses it, submission counts) | Derived: FI-01–FI-06 + FE-42 | Stretch |
| [WS-13] | PRA tracking per form (Melanie ~half, Monique ~half) | Derived: [S03], [S05], [S13] PRA notes | Operational dependency; stretch |
| [WS-16] | Congressional reporting tools (Melanie's workflow) | Derived: DA-09 + [S01], [S03], [S29] — exports → PM website → Congress | Post-MVP |
| [WS-17] | CQI workflow integration (Kayla's sprints) | Derived: WF-17 + [S03], [S05] — CQI consumes collaboration visibility | Post-MVP |
| [WS-19] | Staff support console with scoped read-only access | Derived: UP-12 + UP-04 | Post-MVP |
| [WS-20] | Trackable support interactions (category, resolution, time) | Derived: SC-15 (≤1 ticket/org) implies tracking | Post-MVP |

#### Role-Permission Matrix (from [S32])

| Capability | Approver | Contributor | Viewer | OCS Staff | Admin |
|------------|----------|-------------|--------|-----------|-------|
| Edit form sections | Yes | Yes | No | No | No |
| Submit / attest | Yes | No | No | No | No |
| View form data | Yes | Yes | Yes | Yes (read-only) | Yes |
| Export PDF/CSV | Yes | Yes | Yes | Yes | Yes |
| Portfolio dashboard | No | No | No | Yes | Yes |
| Manage users/roles | No | No | No | No | Yes |
| View audit logs | No | No | No | Limited | Yes |

### Contract & Governance

From [S33] (ACF Project Brief). Contract structure and governance obligations.

| ID | Item | Source | Notes |
|----|------|--------|-------|
| CG-01 | Contract: 24-month (12+12); Core: PM, Tech Lead, Product Manager, UX Lead, 2 Sr Full-Stack Devs (6 FTE); Surge: +2 Devs, +0.5 Security, +0.25 A11y (M4-9, M13-15) | [S33]; [S35] | Relevant to C-8; [S33] says ~4.75 FTE, [S35] details 6 FTE + surge |
| CG-02 | Key personnel: Product Manager requires government approval for replacement | [S33] |  |
| CG-03 | Bi-weekly release cadence | [S33] | Aligns with agile methodology |
| CG-04 | Governance: Project Intake Form within 5 days of award; CFT meetings; Stage Gate Reviews | [S33] | ACF OCIO governance framework |
| CG-05 | Reporting: bi-weekly dashboard, monthly CSR, semi-annual Mid-Year Performance Summary | [S33] |  |
| CG-06 | Transition plan: 4 weeks per [S33], 90 days per [S35] — see C-12 | [S33]; [S35] | Conflict: 4 weeks (2 sprints) vs 90 days (doc audit → training → parallel ops) |
| CG-07 | Incident response: comply with ACF IRT policy; report all suspected/confirmed incidents | [S33] |  |
| CG-09 | Tribal Advisory Group: 6-8 geographically diverse representatives (formed M1-6); 8-10 site visits during discovery | [S35] |  |
| CG-11 | Repo and all infrastructure assets transfer to HHS/ACF post-development | [S35] |  |
| CG-12 | Open-source contributions planned: USWDS Crispy Forms for Django, USWDS Cotton component framework | [S35] | Aspirational; Crispy Forms not observed in codebase |
| CG-13 | All IP (research, designs, code, documentation) is property of ACF | [S37] | From PWS |
| CG-14 | Requirements are non-exhaustive and mutable; agile discovery drives changes; Government is Product Owner | [S37] | From PWS |

### Phased Rollout

From [S33] (ACF Project Brief). Long-term deployment phases beyond MVP.

| ID | Phase | Scope | Source | Notes |
|----|-------|-------|--------|-------|
| PH-01 | Phase I (MVP) | CSBG Tribal forms (~66 orgs, 3 forms) | [S33]; [S29] | Current scope |
| PH-02 | Phase II | States/territories opt in; legacy OLDC runs in parallel | [S33] | Dual-track operation required — some users on CORE, some on legacy |
| PH-03 | Phase III | Full migration of all users; legacy system sunset | [S33] | Requires data migration and feature parity with PDF workflows |
| PH-04 | Long-term vision | 25,000+ recipients, 100+ forms across all ACF program offices | [S33] | CSBG is first program; multi-program platform |

---

## Open Conflicts

### 12. Conflicts Requiring Resolution

> C-1 through C-13. See [open-items.md § Conflicts](open-items.md#conflicts-c-1-through-c-13) for full conflict table with source citations, MVP-blocking flags, and resolution status.
>
> Inline flags throughout this document (e.g., "**CONFLICT**", references to C-xx) mark specific requirements affected by these conflicts.

---

## Background Intelligence

> Cross-program expansion interest and legacy system details moved to [UNDERSTANDING.md](UNDERSTANDING.md):
> - [Legacy Systems & Data Sources](UNDERSTANDING.md#legacy-systems--data-sources) (OLDC, SmartForms, GrantSolutions, etc.)
> - [Cross-Program Expansion Interest](UNDERSTANDING.md#cross-program-expansion-interest) (ANA, CB, LIHEAP, Diaper, Rural Dev)

---

## Appendix A: Source Document Registry

All source references in this matrix use bracketed IDs (e.g., `[S29]`) that map to the documents below. Section references (e.g., `§2.0 Workflow`) follow the document ID where applicable.

| ID | Document | Date | Key Detail |
|----|----------|------|------------|
| S01 | 2024-06 Initial Conversation | 2024-06 | Conversation with Minette Galindo — OLDC history, SmartForms issues |
| S02 | 2025-09-17 Kickoff Prep | 2025-09-17 | Pre-kickoff preparation notes |
| S03 | 2025-09-25 Kickoff with CSBG Staff | 2025-09-25 | Kickoff meeting with CSBG program staff |
| S04 | 2025-09-29 Kickoff | 2025-09-29 | Project kickoff meeting |
| S05 | 2025-11-20 CSBG Check-in | 2025-11-20 | CSBG program check-in; staff roles and regional assignments |
| S06 | 2025-11-26 Forms Digitization Meeting | 2025-11-26 | Cross-program forms digitization discussion (ANA, CB, LIHEAP) |
| S07 | 2026-01-13 ITB Meeting | 2026-01-13 | Integrated Technical Board — tech stack approved |
| S08 | 2026-01-27 ITB Meeting | 2026-01-27 | ITB — ATO artifacts, Security Assessment Plan, Appendix X |
| S09 | 2026-02-03 ITB Meeting | 2026-02-03 | ITB — ECS and Postgres confirmed |
| S10 | 2026-02-10 ITB Meeting Minutes | 2026-02-10 | ITB — GitLab, auth paths, Okta groups |
| S11 | 2026-02-13 Meeting | 2026-02-13 | Sprint demo / working meeting |
| S12 | ATO Documentation & Compliance Hub | Ongoing | ATO artifact tracker and compliance status dashboard |
| S13 | CSBG Annual Report.md | — | CSBG Annual Report form analysis, data migration notes, XML/XSD artifacts |
| S14 | CSBG Data Files.md | — | FY24 raw data exports (State Plan, Modules 1/2/4); RVW/RPT naming convention |
| S15 | CSBG Reporting Process.md | — | Reporting workflow, IM #152, module definitions, $50k funding threshold |
| S16 | CSR Dec 2025 | 2025-12 | Contractor Status Report — December 2025 |
| S17 | CSR Jan 2026 | 2026-01 | Contractor Status Report — January 2026 |
| S18 | CSFEER Tech Stack | — | Approved technology choices (Python, Django, Alpine.js, USWDS, WeasyPrint, etc.) |
| S19 | Demo 1 | 2025-12-05 | First sprint demo — conditional narrative display |
| S20 | Design & Research.md | — | Design & Research index (Figma boards, prototype versions V1/V1.3) |
| S21 | Form Manager Tech Spec (WIP) | 2026-02-13 | Ryan Bagwell — form manager implementation specification |
| S22 | Forms Engine Discovery | — | Discovery phase process maps and research workshops |
| S23 | Forms Engine Onboarding Documents | — | Onboarding materials; GrantSolutions and legacy system context |
| S24 | Initial Product Spec - MVP | — | MVP objectives, key results, requirements (#1–#19), NFRs (#1–#6) |
| S25 | IPT Meetings Index | — | Integrated Project Team meeting notes index |
| S26 | OCS and CSBG Overview | — | Program overview, form inventory (60 forms across 8 offices + 4 cross-office) |
| S27 | Okta Auth Tech Spec DRAFT | 2026-02-18 | Mohammad Taleb — OIDC auth via Okta, Keycloak dev mock, token lifecycle |
| S28 | Product_ Forms Engine | — | Product team roster and role assignments |
| S29 | PWS (Performance Work Statement) | — | Contract PWS — §2.0 subsections, Task Areas, Phases, Objectives, Top Problems |
| S30 | Risk Management | — | Risk management documentation and team assignments |
| S31 | Q1 2026 Forms Engine Plan | 2026-01 | Sprint-level delivery plan — Tribal AR by Mar 15, Tribal Plan by Mar 31; shutdown risk sequencing |
| S32 | ACF Forms Engine User Personas | — | Six personas across three tiers (tribal grantee, OCS federal, system admin); connectivity and batch-review constraints |
| S33 | ACF Project Brief | — | Contract structure, governance, compliance mandates, phased rollout; CORE as public-facing name |
| S34 | ACF CSFEER Intro Client Meeting | 2025-09 | Pre-kickoff intro between OCS and Focus; legacy system dates to 2015; 9-12 month validation cycles; LIHEAP/Diaper/Rural as future targets |
| S35 | PMP V2 | 2025-10 | Project Management Plan — 12-month delivery, soft launch to 10-12 tribes at Month 9, ECS (not EKS), read-only API for ACF staff |
| S36 | Product Spec — CORE Tribal MVP v2.0 | 2025-11-17 | Tribal MVP spec v2.0 — 75% digital adoption target, 3-7 day submission target (from 12-20), 90-day baseline telemetry plan |
| S37 | Specific Requirements and Tasks (synthesized) | — | Synthesized analysis of PWS §2.0; surfaces no-code form builder, public link sharing, ATO timeline, SORN, federal review workflow open questions |
| S38 | ITB - CSFEER (synthesized) | 2026-01-13 | Synthesized IPT kickoff analysis; NGSC AWS deployment, inherited ATO strategy, Okta-mediated Login.gov, OLDC integration dependencies |
| S39 | Product Specification - MVP for CSFEER/CORE (synthesized) | — | Synthesized MVP spec analysis; Phase I targeting 66 tribal orgs, 3 forms, SLA specifics, governance, acceptance criteria, CORE naming |

---

## Next Steps

> Open research tasks moved to [UNDERSTANDING.md § Research Next Steps](UNDERSTANDING.md#research-next-steps).
>
> **Completed:**
> - [x] Source-verify all requirements against 30 source documents (2026-03-02)
> - [x] Restrict System Requirements sources to contractual/program authority (2026-03-02)
> - [x] Add missing [S29] "Top Problems to Solve" items — FE-12, WF-17, DA-14 (2026-03-03)
> - [x] Incorporate March 31 statutory deadline — WF-18 (2026-03-03)
> - [x] WS lineage analysis — DA-15, FE-47, AD-13, UP-12 added (2026-03-03)
