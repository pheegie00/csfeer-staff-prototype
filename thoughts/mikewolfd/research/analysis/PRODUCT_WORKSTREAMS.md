# Product Workstreams

> Eight workstreams for the CSFEER/CORE forms engine, organized by the core question each answers.
> Derived from UNDERSTANDING.md, Confluence export analysis (INFO_MAP.md), and framework requirements analysis.
>
> Priority scale: **P0** Critical — blocks launch | **P1** Core — required for functional MVP | **P2** Expected — stakeholders assume this for production | **P3** Valuable — significant improvement, not essential | **P4** Phase II+ | **P5** Vision

---

## Dependency Graph

```
                    ┌─→ 2. Grantee Experience
                    │
1. Form Schema ─────┼─→ 3. Form Data Architecture
   & Rules          │
                    ├─→ 4. Federal Staff Experience
                    │
                    └─→ 5. Data Requirements & Integration

6. Identity & Access ──────→ gates deployment of all above

7. Compliance & Infra ─────→ gates production launch

8. Form Administration ────→ operational from day one; authoring evolves over time
```

Schema is the spine. Everything else branches off it. Once the schema stabilizes, the other streams can proceed in parallel.

---

## 1. Form Schema & Rules

**Core question:** What IS a form?

This is the critical path. Everything else consumes it. Schema must be **program-agnostic from day one** — not CSBG-specific, to support future LIHEAP, Diaper Program, Rural Development, and all ACF offices.

| P | Capability |
|---|---|
| 0 | Field types: open text, numeric, date, select/dropdown, free-text narrative, financial detail (formatted/validated) |
| 0 | Conditional fields / branching questions |
| 0 | Long form vs short form variants from same base definition (e.g., $50K funding threshold determines tribal form type) |
| 0 | Validation rule definitions: hard errors (block submission) and warnings (inform only) |
| 0 | Validation scope levels: field-level, field-group-level (related fields together), and form-level (cross-section checks) |
| 1 | Repeatable sections |
| 1 | File attachment fields (stored with submission) |
| 1 | Auto-calculated fields (formulas referencing other field values) |
| 1 | Pre-populated field definitions (from prior submissions + cross-form data) |
| 1 | Screener flow routing (routing users to correct form based on answers) |
| 1 | Prior-year comparison rules (validation against previous submission values) |
| 2 | Cross-form field dependencies (shared field identifiers across form definitions) |
| 2 | One-to-many response types (multiple responses per question) |
| 3 | Schema-driven form definitions decoupled from hardcoded UI (current MVP: Pydantic classes are the schema) |
| 4 | Form complexity spectrum: support for multi-document packages (CB Title IV-E: 26-page instrument + 62-page instructions + 150-page guide) |
| 5 | Schema supports visual/no-code authoring |

**Blocks:** everything. **Blocked by:** product decisions on scope.

---

## 2. Grantee Experience

**Core question:** How do grantees fill out forms?

Has its own design cycle (Figma V1 → V1.3 → usability testing April-May 2026), its own user research track (moderated usability testing with 5+8 tribal grant recipients), and its own frontend engineering. Consumes the schema but never touches federal review screens.

| P | Capability |
|---|---|
| 0 | Interview-style page-by-page flow with server-driven navigation |
| 0 | Save-and-resume (partial completion) |
| 0 | WCAG 2.0 AA / Section 508 compliant |
| 0 | USWDS as design foundation |
| 1 | Auto-save every 30-60s (debounced, conflict handling) |
| 1 | Responsive for tablets/laptops (not phones) |
| 1 | Screener flow UX (form selection based on user answers) |
| 1 | Inline explanatory validation messages (e.g., "Total of Sections A-C must equal your CSBG award amount") — contributors use validation errors as a workflow cue |
| 1 | Clear visual distinction between hard errors vs. warnings vs. optional throughout |
| 2 | Pre-populated fields with editable vs locked distinction |
| 2 | Visual change indicators per field ("what changed from last year") |
| 2 | Client-side caching (IndexedDB/localStorage) for connection drops |
| 2 | Sync on reconnect with status indicators |
| 2 | Contextual guidance system: field-level help, section-level instructions, form-level guidance (some forms have 62-150 page companion instruction documents) |
| 3 | Multi-person collaboration on a single form |
| 4 | Fully offline field administration (ANA does live in-person assessments in Alaska with no internet; CB does collaborative case-file review on-site). MVP only targets connection-drop resilience but framework should not preclude offline-first. |

**Blocks:** usability testing, beta. **Blocked by:** schema stability.

---

## 3. Form Data Architecture

**Core question:** How do we store and process form data internally?

The Ryan Bagwell Form Manager tech spec territory. Engineering decisions about how the system works under the hood.

| P | Capability |
|---|---|
| 0 | FormEntry model with JSON field storage for form data |
| 0 | Server-driven page determination (POST request → server decides next page → HTML response) |
| 0 | Save/draft mechanics (arbitrary data accepted, no blocking validation on partial save) |
| 0 | Pydantic schema → Django form field rendering pipeline |
| 0 | Form status state machine: draft → submitted → archived |
| 1 | FormAuditTrail model (log of user actions per form entry — user-facing, not just admin; standalone requirement per Product Spec) |
| 1 | FormAuditDetail model (field-level change tracking) |
| 1 | PDF generation from review page data (WeasyPrint) |
| 1 | FormDefinition import from schema classes (`load_initial_forms`) |
| 1 | Read API for forms, submissions, and bulk data extraction (DA-01) |
| 1 | Write API for importing pre-populated data (DA-02) |
| 2 | Auto-save conflict handling for concurrent edits |
| 2 | Submission history preserved against the definition version it was created with |
| 2 | Form definition evolution without breaking existing submissions |
| 3 | Side-by-side past submission comparison |

**Design tension:** Form Manager tech spec implements review-page-only validation ("any arbitrary data can be entered") to support partial saves. UNDERSTANDING.md VE-07 requires real-time validation during data entry (Must priority). Resolution needed — this is a data architecture decision that affects grantee UX.

**Blocks:** grantee experience (rendering depends on data architecture), federal review (needs submissions to exist). **Blocked by:** schema (storage shape follows definition shape).

---

## 4. Federal Staff Experience

**Core question:** How do federal staff review, approve, and use form data?

Completely different users with completely different UX needs from grantees. The User Research Plan uses a separate research methodology for this group (semi-structured process-mapping interviews with OCS staff: Jane, Issac, Roneika, Feb-March 2026).

Key users: Melanie Durley (Congressional reporting, PRA approval), Monique Alcantara (OLDC testing, SmartForms cooperative agreement, Performance Management website), Kayla Lennon (CQI sprints, disaster relief collections), Lena Kotanchyan (data calls, Python/R/ArcGIS analysis).

| P | Capability |
|---|---|
| 0 | Submit / unsubmit / revise cycle |
| 1 | Multi-step, multi-person federal review and approval (WF-07) |
| 1 | Status dashboard (submissions by state, completion rates, outstanding reviews) |
| 2 | Transmittal letter / attestation as distinct artifact (signatures, upload tracking) |
| 2 | Deadline-aware notifications (NF-01) — email + dashboard + system alerts |
| 2 | Workflow-triggered notifications (NF-02) — submission received, review complete, revision requested |
| 2 | Data analysis export for federal staff (CSV, Excel, filtered views) |
| 3 | Congressional reporting tools (formatted output for Melanie's reporting workflow) |
| 3 | CQI workflow integration (Kayla's continuous quality improvement sprints) |
| 4 | Help desk / customer support tooling |

**Blocks:** production launch (no review = no submission pipeline). **Blocked by:** schema, identity (who can review what), data architecture (submissions must exist).

---

## 5. Data Requirements & Integration

**Core question:** What do downstream consumers need the data to look like?

Research-oriented and externally-focused. Bidirectional. The Thomas Oldfield territory — data structure liaison for upstream systems.

| P | Capability |
|---|---|
| 1 | PDF export (generated from review page data) |
| 1 | CSV/Excel export (current OLDC exports use RVW/RPT prefix convention; Module 3 patterns may differ) |
| 1 | Pre-population from OLDC exports (year-over-year) |
| 2 | Conditional-logic-aware PDF rendering (omit non-applicable sections — known pain point: printed forms currently show ALL questions including non-applicable ones, making them "hard to read") |
| 2 | Bulk data extraction API for federal staff analytics |
| 2 | SmartForms XML/XSD import (NASCSP distributes specs to vendors; current tribal reporting uses XML-based validation) |
| 2 | Prior-year submission data reconciliation from legacy systems |
| 2 | Congressional reporting format compliance |
| 2 | Integration validation against external data (e.g., UEI mismatch detection from SAM.gov) |
| 3 | Performance Management website feed (Monique is COR/PO — this is where exports go for Congressional reporting) |
| 3 | Tableau analytics pipeline integration (PII approval dependency) |
| 3 | OLDC Excel export parsing for migration (FY24 exports use RVW/RPT prefix convention; Module 3 patterns may differ) |
| 4 | State/third-party vendor system accommodation: PA uses COPOS, VA has custom system, NJ uses "empower" — existing state-to-OLDC integration patterns must be understood before Phase II |

**Blocks:** Congressional reporting, state integration (Phase II), pre-population accuracy. **Blocked by:** schema (export shape), submissions existing (for testing).

---

## 6. Identity & Access

**Core question:** Who can do what?

Has its own tech spec (Okta Authentication DRAFT, Feb 18, 2026), its own personnel (Mohammad Taleb, Katherine Chase, Matt Ding, Jim Cooper), and its own critical open questions. Four different descriptions of the auth architecture exist across Confluence docs — canonical resolution needed.

| P | Capability |
|---|---|
| 0 | Government user auth via login.acf.gov (Okta) with OIDC Authorization Code Flow + PKCE |
| 0 | Role mapping from JWT `realm_access.roles` claims (csfeer_admin, csfeer_staff, superuser) |
| 0 | Keycloak local development mock (realm: csfeer, client: csfeer-auth) |
| 1 | Non-government user auth via Login.gov (path still unconfirmed — could delay development or require rework) |
| 1 | Flexible role-based permissions model (PM-01) |
| 1 | User provisioning workflow (ServiceNow ticket vs self-service — TBD) |
| 2 | Self-service user management by organization admins (PM-02) |
| 2 | Hierarchical administration — federal > state/territory > tribal organization (PM-03) |
| 2 | Minimum permission levels per role (PM-04) |
| 2 | Federal staff roles: reviewer, approver, analyst, admin (PM-05) |
| 3 | Client secret rotation schedule and process in AWS Secrets Manager |
| 3 | RP-initiated logout with Okta session termination and post-logout redirect |

**Blocks:** deployment of all feature work, federal review (role-based access). **Blocked by:** Okta configuration decisions (6 critical open questions), non-government auth path resolution.

---

## 7. Compliance & Infrastructure

**Core question:** What gates production?

Not a "feature" workstream but has its own deliverables, owners (Oyindasola Akisanmi as ISSO, Beatrice Adenigbagbe as SCA, Tharun Chada for NGSC), and timeline. Product decisions feed into it and it constrains product.

| P | Capability |
|---|---|
| 0 | ATO documentation: 9 artifacts tracked, May 29, 2026 target |
| 0 | FISMA classification resolution (ATO hub says Low baseline; UNDERSTANDING.md says Moderate — contradictory) |
| 0 | NGSC AWS provisioning and ECS deployment |
| 0 | PIA classification resolution (whether "electronic information collection" vs "application") |
| 1 | GitLab repository setup and GitHub-to-GitLab mirroring |
| 1 | Appendix X completion (effort = "as much as all other ATO docs combined") |
| 1 | System Security Plan (SSP), BIA, IRP, Contingency Plan, Configuration Management Plan |
| 2 | E-Authentication Agreement (formal artifact for dual auth paths) |
| 2 | Government shutdown continuity plan (contact matrix exists; already impacted Feb 3 ITB) |

**Blocks:** production launch (hard gate). **Blocked by:** external review timelines, security team availability.

---

## 8. Form Administration

**Core question:** How are forms and their lifecycle managed operationally?

Active from day one. The authoring portion evolves: MVP = developer-authored Pydantic schemas; Year 2+ = visual/no-code form builder.

| P | Capability |
|---|---|
| 0 | Form definition deployment via `load_initial_forms` management command |
| 1 | Form status management — which forms are active, closed for cycle, or archived |
| 1 | Version management — current definition version, retiring old versions, submission pinning |
| 1 | Submission cycle operations — opening/closing reporting periods, deadline management (March 31 Annual Report) |
| 2 | Form inventory visibility — what forms exist, who uses them, submission state counts |
| 2 | PRA tracking — OMB approval status per form (Melanie manages ~half, Monique ~half) |
| 2 | Auto-create/initialize form instances on schedule |
| 2 | Email notifications for form status changes (cycle opening, deadlines approaching, submission received) |
| 3 | Multiple simultaneous form definition versions coexisting in production |
| 5 | Visual/no-code form builder for non-technical form authors |

---

## Cross-Cutting: Observability & Telemetry

A core but underappreciated goal is creating the **first measurable baseline** for tribal reporting performance. OCS currently has zero telemetry on workflow efficiency, error patterns, or user burden. This cuts across workstreams:

| Telemetry Category | Owner Workstream | Examples |
|---|---|---|
| User interaction | WS2 Grantee Experience | Sessions per submission, time per section, autosave frequency/success, sync patterns |
| Submission quality | WS3 Data Architecture | Validation error types/frequency, resolution rates, submit-unsubmit cycles |
| Performance | WS7 Compliance & Infra | Load times, save/sync times, export performance, p95/p98 latency |
| Operational | WS4 Federal Staff | Ticket volume, time-to-resolution, OCS review time |

Requires instrumentation from day one — event tracking for autosave, section timing, validation error categorization, connectivity state transitions. First 90 days post-launch establish measurement baselines across all four dimensions.

---

## Key Stress Points

The heaviest lifts — areas where complexity concentrates:

1. **Auto-calculated fields** with cross-field formulas
2. **Real-time validation with prior-year comparison** — compounded by the design tension between "allow arbitrary data for partial saves" and "validate in real-time during entry"
3. **Multi-version form definitions** with submission pinning
4. **Dual hard-error/warning system** that doesn't block partial saves
5. **Contextual guidance at scale** — some forms have 150-page companion documents; guidance must be embedded/accessible without overwhelming the data entry experience
6. **Conditional-logic-aware PDF export** — printed output must omit non-applicable sections (not just hide them in the UI)
7. **Offline-first extensibility** — MVP needs connection-drop resilience, but the framework must not preclude fully-offline field administration for future ACF programs (ANA, CB use cases)
8. **Legacy system integration** — SmartForms XML/XSD import, OLDC Excel export parsing, state vendor API accommodation (COPOS, CSG, custom systems)

