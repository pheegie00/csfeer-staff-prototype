# Product Workstreams V2

> Eleven deliverables for the CSFEER/CORE forms platform, organized by the four-layer architecture from the Value Stream Analysis.
>
> Derived from PWS ADMIN/OCS/CSBG/CSFEER v2 (Rev 2, August 25, 2025), PRODUCT_WORKSTREAMS V1, VALUE_STREAM_ANALYSIS, UNDERSTANDING.md, and Confluence export analysis.
>
> Priority scale: **P0** Critical — blocks launch | **P1** Core — required for functional MVP | **P2** Expected — stakeholders assume this for production | **P3** Valuable — significant improvement, not essential | **P4** Phase II+ | **P5** Vision
>
> Requirement IDs use mnemonic prefixes per deliverable (e.g., `SCH-01` for Schema, `ENG-01` for Engine). IDs are stable — new requirements append; retired requirements are marked, not renumbered.
>
> Provenance:
> - **PWS** — directly traceable to the Performance Work Statement
> - **PWS+** — derived from or extends PWS requirements
> - **VSA** — from Value Stream Analysis (first-principles decomposition)
> - **Discovery** — from stakeholder interviews, user research, or real-world events
> - **Engineering** — architectural or implementation decisions by the team

---

## Architecture Layers & Dependency Graph

```
                    ┌─────────────────────┐
                    │  Form Schema        │  ← Specification
                    │  Convention         │
                    └────────┬────────────┘
                             │
        ┌────────────────────┼────────────────────┬──────────────────┐
        ▼                    ▼                    ▼                  ▼
  Form Engine          Workflow Rules       System & User       Inbound
  Backend              Engine              Administration      Integration
        │                    │                    │                  │
        ├────────────────────┼────────────────────┼──────────────────┤
        ▼                    ▼                    ▼                  ▼
  Recipient            Internal              Form              Support
  Application          Workflows UI          Administration    Tooling
        │                    │                    │                  │
        └────────┬───────────┘────────────────────┘──────────────────┘
                 │
        ┌────────┴─────────┐    ┌──────────────────┐
        │    Reporting     │◄───│     Outbound      │
        │    Platform      │    │   Integration     │
        └──────────────────┘    └──────────────────┘
```

**Specification.** The Form Schema Convention. Everything implements or consumes it.

**Foundation.** Form Engine Backend, Workflow Rules Engine, System & User Administration, Inbound Integration. Independent of each other. Collectively required before the application layer functions.

**Application.** Recipient Application, Form Administration, Internal Workflows UI, Support Tooling. Consumers of the foundation. Each independently deployable.

**Terminal.** Reporting Platform, Outbound Integration. Need data flowing through the system before they deliver value.

---

## Specification Layer

### 1. Form Schema Convention

**Core question:** What IS a form?

A specification, not code. The shared grammar that everything else implements or consumes. Must be **program-agnostic from day one** — not CSBG-specific, to support future LIHEAP, Diaper Program, Rural Development, and all ACF program offices.

| ID | P | Capability | Provenance |
|---|---|---|---|
| SCH-01 | 0 | Field primitives: open text, numeric, date, select/dropdown, free-text narrative, financial detail (formatted/validated) | PWS |
| SCH-02 | 0 | Conditional fields / branching questions | PWS |
| SCH-03 | 0 | Long form vs short form variants from same base definition (e.g., $50K funding threshold determines tribal form type) | PWS+ |
| SCH-04 | 0 | Validation rule definitions: hard errors (block submission) and warnings (inform only) | PWS |
| SCH-05 | 0 | Validation scope levels: field-level, field-group-level (related fields together), and form-level (cross-section checks) | PWS |
| SCH-06 | 1 | Repeatable sections | PWS+ |
| SCH-07 | 1 | File attachment fields (stored with submission) | PWS |
| SCH-08 | 1 | Auto-calculated field definitions (formulas referencing other field values) | PWS |
| SCH-09 | 1 | Pre-populated field definitions (from prior submissions + cross-form data) | PWS |
| SCH-10 | 1 | Screener flow routing definitions (routing users to correct form based on answers) | PWS+ |
| SCH-11 | 1 | Prior-year comparison rules (validation against previous submission values) | PWS |
| SCH-12 | 2 | Cross-form field dependencies (shared field identifiers across form definitions) | PWS+ |
| SCH-13 | 2 | One-to-many response types (multiple responses per question) | PWS |
| SCH-14 | 2 | Data sensitivity classification per field (public / internal / sensitive / restricted) | VSA |
| SCH-15 | 2 | PRA metadata per form (OMB control number, expiration, burden estimate) | Discovery |
| SCH-16 | 2 | Versioning rules as part of the specification (how definitions evolve, compatibility constraints) | VSA |
| SCH-17 | 3 | Schema-driven form definitions decoupled from hardcoded UI (current MVP: Pydantic classes are the schema) | Engineering |
| SCH-18 | 4 | Form complexity spectrum: support for multi-document packages (CB Title IV-E: 26-page instrument + 62-page instructions + 150-page guide) | Discovery |
| SCH-19 | 5 | Schema supports visual/no-code authoring | VSA |

**Stress points:** Auto-calculated fields with cross-field formulas (SCH-08). Multi-version form definitions with submission pinning (SCH-16). Dual hard-error/warning semantics that don't block partial saves (SCH-04).

**Blocks:** everything. **Blocked by:** product decisions on scope; multi-tenancy isolation model (open design question).

---

## Foundation Layer

### 2. Form Engine Backend

**Core question:** How do we store and process form data?

Persistence for form definitions and submissions. APIs for form lifecycle operations. Validation execution. Versioning and submission history. The stable core that outlives any frontend.

| ID | P | Capability | Provenance |
|---|---|---|---|
| ENG-01 | 0 | FormEntry model with JSON field storage for form data | PWS+ |
| ENG-02 | 0 | Server-driven page determination (POST request → server decides next page → HTML response) | PWS+ |
| ENG-03 | 0 | Save/draft mechanics (arbitrary data accepted, no blocking validation on partial save) | PWS+ |
| ENG-04 | 0 | Pydantic schema → Django form field rendering pipeline | PWS+ |
| ENG-05 | 0 | Form status state machine: draft → submitted → archived | PWS+ |
| ENG-06 | 0 | Submit / unsubmit / revise state transitions (state machine, not UI) | PWS |
| ENG-07 | 1 | FormAuditTrail model (log of user actions per form entry — user-facing, not just admin; standalone requirement per Product Spec) | PWS |
| ENG-08 | 1 | FormAuditDetail model (field-level change tracking) | PWS+ |
| ENG-09 | 1 | FormDefinition import from schema classes (`load_initial_forms`) | PWS+ |
| ENG-10 | 1 | Read API for forms, submissions, and bulk data extraction | PWS |
| ENG-11 | 1 | Write API for importing pre-populated data | PWS |
| ENG-12 | 2 | Auto-save conflict handling for concurrent edits | PWS+ |
| ENG-13 | 2 | Submission history preserved against the definition version it was created with | PWS |
| ENG-14 | 2 | Form definition evolution without breaking existing submissions | PWS+ |
| ENG-15 | 3 | Side-by-side past submission comparison | PWS |

**Design tension:** The tech spec implements review-page-only validation ("any arbitrary data can be entered") to support partial saves (ENG-03). The product spec requires real-time validation during data entry. Resolution needed — this is a backend architecture decision that affects the Recipient Application.

**Blocks:** Recipient Application (rendering depends on data architecture), Internal Workflows UI (needs submissions to exist), Reporting Platform and Outbound Integration (need data flowing). **Blocked by:** Form Schema Convention (storage shape follows definition shape).

---

### 3. Workflow Rules Engine

**Core question:** What are the rules for moving submissions through their lifecycle?

Submission lifecycle state machine. Routing rules, approval logic, delegation, escalation, conditional routing. The frontends render workflow state; this deliverable owns the rules. **This was previously embedded across multiple workstreams; the VSA correctly separates it as an independent foundation deliverable.**

| ID | P | Capability | Provenance |
|---|---|---|---|
| WFL-01 | 1 | Multi-step, multi-person federal review and approval pipeline | PWS |
| WFL-02 | 1 | Submission cycle operations — opening/closing reporting periods, deadline management (March 31 Annual Report) | PWS |
| WFL-03 | 2 | Deadline-aware notification rules — email + dashboard + system alerts | PWS |
| WFL-04 | 2 | Workflow-triggered notification rules — submission received, review complete, revision requested | PWS |
| WFL-05 | 2 | Auto-create/initialize form instances on schedule | PWS |
| WFL-06 | 2 | Email notification rules for form status changes (cycle opening, deadlines approaching) | PWS+ |
| WFL-07 | 2 | Configurable notification channels and recipients | PWS |
| WFL-08 | 3 | Multi-person collaboration workflow logic (locking, conflict resolution, role-based edit scoping) | PWS+ |
| WFL-09 | 3 | Conditional routing based on submission attributes | VSA |
| WFL-10 | 3 | Multiple simultaneous form definition versions coexisting in production | PWS+ |
| WFL-11 | 4 | Parallel approval branches with join logic | VSA |
| WFL-12 | 4 | Delegation and escalation rules | VSA |
| WFL-13 | 5 | Visual/no-code workflow builder for federal approval workflows | PWS |

**Open design question:** The Workflow Rules Engine covers a wide spectrum — a linear pipeline with approve/revise at one end (WFL-01), conditional routing with parallel branches and delegation at the other (WFL-09, WFL-11, WFL-12). Which capabilities are foundational (must ship) and which are extensions? This distinction determines scope significantly.

**Blocks:** Internal Workflows UI (renders workflow state). **Blocked by:** Form Schema Convention (workflow rules reference form structure).

---

### 4. System & User Administration

**Core question:** Who can do what?

Users, organizations, roles, permissions, authentication. Understands the schema vocabulary for scoping permissions to forms, sections, and fields. Enforces field-level access control. Self-service at every organizational level.

Has its own tech spec (Okta Authentication DRAFT, Feb 18, 2026), its own personnel (Mohammad Taleb, Katherine Chase, Matt Ding, Jim Cooper), and critical open questions. Four different descriptions of the auth architecture exist across Confluence docs — canonical resolution needed.

| ID | P | Capability | Provenance |
|---|---|---|---|
| AUTH-01 | 0 | Government user auth via login.acf.gov (Okta) with OIDC Authorization Code Flow + PKCE | PWS+ |
| AUTH-02 | 0 | Role mapping from JWT `realm_access.roles` claims (csfeer_admin, csfeer_staff, superuser) | PWS+ |
| AUTH-03 | 0 | Keycloak local development mock (realm: csfeer, client: csfeer-auth) | Engineering |
| AUTH-04 | 1 | Non-government user auth via Login.gov (path still unconfirmed — could delay development or require rework) | PWS |
| AUTH-05 | 1 | Flexible role-based permissions model | PWS |
| AUTH-06 | 1 | User provisioning workflow (ServiceNow ticket vs self-service — TBD) | PWS+ |
| AUTH-07 | 2 | Self-service user management by organization admins | PWS |
| AUTH-08 | 2 | Hierarchical administration — federal > state/territory > tribal organization | PWS |
| AUTH-09 | 2 | Minimum permission levels per role | PWS |
| AUTH-10 | 2 | Federal staff roles: reviewer, approver, analyst, admin | PWS |
| AUTH-11 | 2 | Field-level access control scoped to data sensitivity tiers (schema-driven) | VSA |
| AUTH-12 | 2 | Permission scoping to forms, sections, and fields (not just roles) | VSA |
| AUTH-13 | 3 | Client secret rotation schedule and process in AWS Secrets Manager | Engineering |
| AUTH-14 | 3 | RP-initiated logout with Okta session termination and post-logout redirect | Engineering |

**Open design question:** Authentication (AUTH-01, AUTH-04 — Okta/Login.gov plumbing) and authorization (AUTH-05 through AUTH-12 — role-permission model, organizational hierarchy) are bundled here but have different risk profiles and different external dependencies. Authentication is a blocking external dependency with open questions (non-government auth path unresolved). Authorization is an internal design problem. The two may warrant separate treatment.

**Blocks:** deployment of all feature work (authentication gates everything), Internal Workflows UI (role-based access), Recipient Application (grantee auth). **Blocked by:** Okta configuration decisions (6 critical open questions), non-government auth path resolution.

---

### 5. Inbound Integration

**Core question:** How does external data flow into the platform?

Pre-population pipelines: grant management records, entity validation (SAM.gov UEI), prior-year submissions. Maps external data into the schema convention. Designed to onboard new sources as programs adopt the platform.

| ID | P | Capability | Provenance |
|---|---|---|---|
| INB-01 | 1 | Pre-population from OLDC exports (year-over-year) | PWS |
| INB-02 | 2 | SmartForms XML/XSD import (NASCSP distributes specs to vendors; current tribal reporting uses XML-based validation) | Discovery |
| INB-03 | 2 | Prior-year submission data reconciliation from legacy systems | PWS+ |
| INB-04 | 2 | Integration validation against external data (e.g., UEI mismatch detection from SAM.gov) | PWS |
| INB-05 | 3 | OLDC Excel export parsing for migration (FY24 exports use RVW/RPT prefix convention; Module 3 patterns may differ) | Discovery |
| INB-06 | 4 | State/third-party vendor system accommodation: PA uses COPOS, VA has custom system, NJ uses "empower" — existing state-to-OLDC integration patterns must be understood before Phase II | Discovery |

**Open design question:** Data migration is a precondition for pre-population (INB-01). The current system has operated since 2015. OLDC exports, SmartForms XML/XSD, FY24 data with RVW/RPT conventions, and a parallel OLDC modernization effort all exist. Is migration a component of this deliverable or a separate concern? Currently unscoped.

**Stress point:** Legacy system integration — INB-02, INB-05, INB-06.

**Blocks:** Recipient Application (pre-population requires inbound data). **Blocked by:** Form Schema Convention (mapping external data requires the schema grammar).

---

## Application Layer

### 6. Recipient Application

**Core question:** How do grantees fill out forms?

Grantee-facing interface. Form rendering, save/resume, collaboration, low-connectivity resilience, real-time validation with explanatory messages, submit/revise lifecycle. Consumes the Form Engine Backend via APIs.

Has its own design cycle (Figma V1 → V1.3 → usability testing April-May 2026), its own user research track (moderated usability testing with 5+8 tribal grant recipients), and its own frontend engineering. Consumes the schema but never touches federal review screens.

| ID | P | Capability | Provenance |
|---|---|---|---|
| APP-01 | 0 | Interview-style page-by-page flow with server-driven navigation | PWS+ |
| APP-02 | 0 | Save-and-resume (partial completion) | PWS |
| APP-03 | 0 | WCAG 2.0 AA / Section 508 compliant | PWS |
| APP-04 | 0 | USWDS as design foundation | PWS |
| APP-05 | 1 | Auto-save every 30-60s (debounced, conflict handling) | PWS+ |
| APP-06 | 1 | Responsive for tablets/laptops (not phones) | PWS+ |
| APP-07 | 1 | Screener flow UX (form selection based on user answers) | PWS+ |
| APP-08 | 1 | Inline explanatory validation messages (e.g., "Total of Sections A-C must equal your CSBG award amount") — contributors use validation errors as a workflow cue | PWS+ |
| APP-09 | 1 | Clear visual distinction between hard errors vs. warnings vs. optional throughout | PWS+ |
| APP-10 | 2 | Pre-populated fields with editable vs locked distinction | PWS |
| APP-11 | 2 | Visual change indicators per field ("what changed from last year") | PWS+ |
| APP-12 | 2 | Client-side caching (IndexedDB/localStorage) for connection drops | Engineering |
| APP-13 | 2 | Sync on reconnect with status indicators | Engineering |
| APP-14 | 2 | Contextual guidance system: field-level help, section-level instructions, form-level guidance (some forms have 62-150 page companion instruction documents) | Discovery |
| APP-15 | 2 | Accessibility incident management process | PWS |
| APP-16 | 3 | Multi-person collaboration on a single form (UI surface; workflow logic in WFL-08) | PWS |
| APP-17 | 4 | Fully offline field administration (ANA does live in-person assessments in Alaska with no internet; CB does collaborative case-file review on-site). MVP only targets connection-drop resilience but framework should not preclude offline-first. | Discovery |

**Stress points:** Real-time validation with prior-year comparison (APP-08 + SCH-11, compounded by the partial-save design tension in ENG-03). Contextual guidance at scale (APP-14). Offline-first extensibility (APP-17).

**Blocks:** usability testing, beta. **Blocked by:** Form Schema Convention (rendering follows schema), Form Engine Backend (data operations), System & User Administration (grantee auth), Inbound Integration (pre-population).

---

### 7. Form Administration

**Core question:** How are forms built, tested, published, and versioned?

Build, test, publish, and version form definitions. PRA metadata management. Sandbox environment for draft forms. This deliverable transforms the platform from a bespoke build into a reusable engine. Active from day one — the authoring portion evolves: MVP = developer-authored Pydantic schemas; Year 2+ = visual/no-code form builder.

| ID | P | Capability | Provenance |
|---|---|---|---|
| ADM-01 | 0 | Form definition deployment via `load_initial_forms` management command | PWS+ |
| ADM-02 | 1 | Form status management — which forms are active, closed for cycle, or archived | PWS+ |
| ADM-03 | 1 | Version management — current definition version, retiring old versions, submission pinning | PWS |
| ADM-04 | 2 | Form inventory visibility — what forms exist, who uses them, submission state counts | PWS+ |
| ADM-05 | 2 | PRA tracking — OMB approval status per form (Melanie manages ~half, Monique ~half) | Discovery |
| ADM-06 | 2 | Sandbox environment for draft form testing distinct from production | VSA |
| ADM-07 | 5 | Visual/no-code form builder for non-technical form authors | PWS |

**Open design question:** Form definitions require developer effort until a visual builder ships (ADM-07). How program staff communicate form changes, the turnaround time for a schema update, and the testing process determine whether the platform behaves like a product or a custom build during its early life. This is an operational constraint this deliverable must address even before a visual builder exists.

**Blocks:** Recipient Application (needs published form definitions). **Blocked by:** Form Schema Convention (definitions implement the spec).

---

### 8. Internal Workflows UI

**Core question:** How do federal staff review, approve, and act on submissions?

Federal review and approval interface. Review queues, routing visualization, approval actions, revision requests with feedback. Consumes Workflow Rules Engine and Form Engine Backend.

Completely different users with completely different UX needs from grantees. Separate research methodology (semi-structured process-mapping interviews with OCS staff: Jane, Issac, Roneika, Feb-March 2026).

Key users: Melanie Durley (Congressional reporting, PRA approval), Monique Alcantara (OLDC testing, SmartForms cooperative agreement, Performance Management website), Kayla Lennon (CQI sprints, disaster relief collections), Lena Kotanchyan (data calls, Python/R/ArcGIS analysis).

| ID | P | Capability | Provenance |
|---|---|---|---|
| REV-01 | 1 | Status dashboard (submissions by state, completion rates, outstanding reviews) | PWS+ |
| REV-02 | 1 | Review actions: approve, request revision with feedback, reject | PWS |
| REV-03 | 2 | Transmittal letter / attestation as distinct artifact (signatures, upload tracking) | Discovery |
| REV-04 | 2 | Review queue management with routing visualization | VSA |
| REV-05 | 2 | Data analysis export for federal staff (CSV, Excel, filtered views) | PWS |
| REV-06 | 3 | Congressional reporting tools (formatted output for Melanie's reporting workflow) | Discovery |
| REV-07 | 3 | CQI workflow integration (Kayla's continuous quality improvement sprints) | Discovery |

**Blocks:** production launch (no review = no submission pipeline). **Blocked by:** Form Engine Backend (submissions must exist), Workflow Rules Engine (routing and approval logic), System & User Administration (who can review what).

---

### 9. Support Tooling

**Core question:** How do users get help when they're stuck?

Contextual help and guided walkthroughs in the Recipient Application. Staff-side support console with scoped access to grantee form state. Pattern tracking for systemic issues.

**Note:** This deliverable was rated P4 in V1 workstreams. The VSA elevates it to a dedicated value stream (Grantee Support) and deliverable, recognizing that the platform must work for its most constrained users. Priority reassignment is an open product decision.

| ID | P | Capability | Provenance |
|---|---|---|---|
| SUP-01 | 2 | Contextual help in Recipient Application: field-level guidance, section instructions, form-level overview (staff-facing surface complements APP-14) | PWS+ |
| SUP-02 | 3 | Staff-side support console with scoped, read-only access to grantee form state | VSA |
| SUP-03 | 3 | Trackable support interactions (issue category, resolution, time-to-resolve) | VSA |
| SUP-04 | 3 | Pattern tracking for systemic issues feeding product improvement | VSA |
| SUP-05 | 4 | Help desk / customer support tooling (full-featured) | VSA |

**Gap note:** This is the thinnest deliverable in terms of PWS coverage. The VSA identifies this as serving the Grantee Support value stream — one of seven. Whether to invest here at P2-P3 or defer to P4 is a scope decision.

**Blocks:** nothing directly. **Blocked by:** Recipient Application (contextual help is embedded), System & User Administration (scoped access for support staff).

---

## Terminal Layer

### 10. Reporting Platform

**Core question:** How does collected data become actionable insight?

Portfolio dashboards, cross-grantee comparison, year-over-year trends, outlier detection, compliance/audit trail access, export packaging.

| ID | P | Capability | Provenance |
|---|---|---|---|
| RPT-01 | 2 | Bulk data extraction API for federal staff analytics | PWS |
| RPT-02 | 2 | Congressional reporting format compliance | PWS+ |
| RPT-03 | 2 | Data analysis export for federal staff (CSV, Excel, filtered views) — shared surface with REV-05 | PWS |
| RPT-04 | 3 | Performance Management website feed (Monique is COR/PO — this is where exports go for Congressional reporting) | Discovery |
| RPT-05 | 3 | Tableau analytics pipeline integration (PII approval dependency) | Discovery |
| RPT-06 | 3 | Portfolio-level dashboards with cross-grantee comparison and year-over-year trends | VSA |
| RPT-07 | 3 | Outlier detection across submission data | VSA |

**Observability goal:** This is the natural home for the overarching telemetry objective — creating the **first measurable baseline** for tribal reporting performance. OCS currently has zero telemetry on workflow efficiency, error patterns, or user burden. The first 90 days post-launch establish measurement baselines.

**Blocks:** nothing. **Blocked by:** submissions flowing through the full submit-review cycle (data must exist).

---

### 11. Outbound Integration

**Core question:** How does structured data flow out of the platform?

APIs for external consumers, CSV and PDF export, public access links with field-level visibility controls.

| ID | P | Capability | Provenance |
|---|---|---|---|
| OUT-01 | 1 | PDF export (generated from review page data via WeasyPrint) | PWS |
| OUT-02 | 1 | CSV/Excel export (current OLDC exports use RVW/RPT prefix convention; Module 3 patterns may differ) | PWS |
| OUT-03 | 2 | Conditional-logic-aware PDF rendering (omit non-applicable sections — known pain point: printed forms currently show ALL questions including non-applicable ones, making them "hard to read") | Discovery |
| OUT-04 | 2 | Public access links with field-level visibility controls | PWS |
| OUT-05 | 2 | Comprehensive, developer-friendly API documentation | PWS |
| OUT-06 | 3 | APIs for external consumers (structured data for downstream systems) | VSA |

**Stress point:** Conditional-logic-aware PDF export (OUT-03) — printed output must omit non-applicable sections, not just hide them in the UI.

**Blocks:** nothing. **Blocked by:** Form Engine Backend (submissions must exist), Form Schema Convention (export shape follows definition shape).

---

## Cross-Cutting Concerns

Four concerns span the entire deliverable map. They live in no single deliverable; every deliverable must account for them.

### Data Sensitivity

Federal grant programs handle data about vulnerable populations: tribal nations, families in poverty, children, domestic violence survivors. Sensitivity varies by program and field. Field-level access control must be part of the schema convention (SCH-14) and enforced by System & User Administration (AUTH-11). Every deliverable that touches submission data respects sensitivity tiers.

### Audit Trail

Every deliverable emits audit events: form creation, field edits, permission changes, submission state transitions, review actions, export operations. The Compliance & Audit value stream consumes these events. Audit is an obligation every deliverable fulfills, not a separate application. FormAuditTrail (ENG-07) and FormAuditDetail (ENG-08) models are the persistence layer; every deliverable contributes events.

### Multi-Tenancy

The platform serves multiple program offices, each with their own forms, recipients, review workflows, and data. Program-level isolation touches the schema convention, the authorization model, and every query surface. The isolation model (tenant, permission, data partitioning, or hybrid) is an **unresolved design decision** that constrains all foundation-layer deliverables.

### Observability & Telemetry

Creating the **first measurable baseline** for tribal reporting performance. OCS currently has zero telemetry on workflow efficiency, error patterns, or user burden. Requires instrumentation from day one. Performance monitoring must track median, p95, and p98 latency, concurrent users, and error rates in real time.

| Telemetry Category | Primary Deliverable | Examples |
|---|---|---|
| User interaction | Recipient Application | Sessions per submission, time per section, autosave frequency/success (APP-05), sync patterns (APP-13) |
| Submission quality | Form Engine Backend | Validation error types/frequency, resolution rates, submit-unsubmit cycles (ENG-06) |
| Performance | Infrastructure & Deployment | Load times, save/sync times, export performance, p95/p98 latency |
| Operational | Reporting Platform | Ticket volume, time-to-resolution, OCS review time |

First 90 days post-launch establish measurement baselines across all four dimensions.

---

## Security & Compliance Artifacts

**Core question:** Can we prove the system is authorized to operate?

Documentation and classification work that gates production launch. Different lifecycle from engineering deliverables — driven by external review timelines, security team availability, and agency processes. Produces artifacts, not features.

**Key personnel:** Oyindasola Akisanmi (ISSO), Beatrice Adenigbagbe (SCA).

| ID | P | Capability | Provenance |
|---|---|---|---|
| SEC-01 | 0 | ATO documentation: 9 artifacts tracked, May 29, 2026 target | PWS |
| SEC-02 | 0 | FISMA classification resolution (ATO hub says Low baseline; UNDERSTANDING.md says Moderate — contradictory) | PWS |
| SEC-03 | 0 | PIA classification resolution (whether "electronic information collection" vs "application") | PWS+ |
| SEC-04 | 0 | System of Records Notice (SORN) | PWS |
| SEC-05 | 1 | Appendix X completion (effort = "as much as all other ATO docs combined") | PWS+ |
| SEC-06 | 1 | System Security Plan (SSP), BIA, IRP, Contingency Plan, Configuration Management Plan | PWS+ |
| SEC-07 | 2 | E-Authentication Agreement (formal artifact for dual auth paths — feeds into AUTH-01, AUTH-04) | PWS+ |
| SEC-08 | 2 | Government shutdown continuity plan (contact matrix exists; already impacted Feb 3 ITB) | Discovery |

**Interaction with deliverables:** Every deliverable that handles data (ENG, AUTH, INB, APP, REV, RPT, OUT) must produce security documentation inputs — data flow diagrams, access control descriptions, encryption-at-rest/in-transit details. The ATO is not just a compliance team deliverable; engineering produces the technical evidence that the compliance artifacts describe.

**Blocks:** production launch (hard gate). **Blocked by:** FISMA/PIA classification decisions (SEC-02, SEC-03), external review timelines, security team availability.

---

## Infrastructure & Deployment

**Core question:** Where does the system run and how does code get there?

Engineering work for provisioning, CI/CD, and operational readiness. Different owners and cadence from security artifacts — this is engineering infrastructure, not compliance documentation.

**Key personnel:** Tharun Chada (NGSC).

| ID | P | Capability | Provenance |
|---|---|---|---|
| INF-01 | 0 | NGSC AWS provisioning and ECS deployment | PWS+ |
| INF-02 | 1 | GitLab repository setup and GitHub-to-GitLab mirroring | Engineering |
| INF-03 | 1 | CI/CD pipeline from GitLab to NGSC environments | PWS |
| INF-04 | 1 | 24/7 operational availability | PWS |
| INF-05 | 2 | Environment parity: dev, staging, production with consistent configuration | Engineering |

**Interaction with deliverables:** Every deliverable deploys through this pipeline. System & User Administration has the tightest coupling — Okta/Login.gov integration requires environment-specific configuration in NGSC. Form Administration needs the sandbox environment concept (ADM-06) to be reflected in deployment topology.

**Blocks:** production launch (nothing deploys without infrastructure). **Blocked by:** NGSC provisioning approval, GitLab access.

---

## Value Stream Traceability

Which deliverables serve which value streams. If a deliverable changes, this shows which user journeys are affected.

|                           | SCH | ENG | WFL | AUTH | INB | APP | ADM | REV | SUP | RPT | OUT |
| ------------------------- | :-: | :-: | :-: | :--: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| **Grantee Submission**    |     |  ●  |     |  ●   |  ●  |  ●  |     |     |     |     |     |
| **Federal Review**        |     |  ●  |  ●  |  ●   |     |     |     |  ●  |     |     |     |
| **Reporting & Analytics** |     |  ●  |     |      |     |     |     |     |     |  ●  |  ●  |
| **System Administration** |  ●  |     |     |  ●   |     |     |  ●  |     |     |     |     |
| **Data Integration**      |  ●  |  ●  |     |      |  ●  |     |     |     |     |     |  ●  |
| **Compliance & Audit**    |     |  ●  |     |  ●   |     |     |  ●  |     |     |  ●  |     |
| **Grantee Support**       |     |  ●  |     |  ●   |     |  ●  |     |     |  ●  |  ●  |     |

---

## Open Design Questions

Unresolved decisions that constrain scope.

1. **Multi-tenancy isolation model.** Tenant partitioning vs permission scoping vs data partitioning vs hybrid. Constrains every foundation-layer deliverable. Must be resolved before foundation layer stabilizes.

2. **Data migration scope.** OLDC exports, SmartForms XML/XSD, FY24 data, parallel OLDC modernization. Is this Inbound Integration or a separate concern? Currently unscoped.

3. **Authentication vs authorization split.** AUTH-01/AUTH-04 (authentication) vs AUTH-05 through AUTH-12 (authorization). Different risk profiles, different external dependencies. May warrant separate treatment.

4. **Workflow rules complexity spectrum.** Linear approve/revise (WFL-01) → conditional routing (WFL-09) → parallel branches (WFL-11) → delegation (WFL-12). Which capabilities are foundational, which are extensions?

5. **Form authoring pipeline before visual builder.** How do program staff communicate form changes, and what's the turnaround time? Determines whether the platform feels like a product or a custom build. See ADM-01 through ADM-06.

6. **Real-time validation vs partial save.** ENG-03 says review-page-only validation; product spec says real-time (APP-08). Architecture decision that crosses Engine and Recipient App.

7. **Support Tooling priority.** VSA elevates this to a full value stream; V1 workstreams rated SUP-05 as P4. Product decision needed on investment level for SUP-02 through SUP-04.

---

## Key Stress Points

The heaviest lifts, mapped to their requirement IDs:

| Stress Point | Requirements |
|---|---|
| Auto-calculated fields with cross-field formulas | SCH-08 (schema) + ENG (execution) |
| Real-time validation with prior-year comparison | ENG-03 vs APP-08 (design tension) + SCH-11 |
| Multi-version form definitions with submission pinning | SCH-16 (versioning rules) + ENG-13, ENG-14 (enforcement) |
| Dual hard-error/warning system that doesn't block partial saves | SCH-04 (semantics) + APP-09 (rendering) |
| Contextual guidance at scale (150-page companion docs) | APP-14 (UX) + SUP-01 (support) |
| Conditional-logic-aware PDF export | OUT-03 |
| Offline-first extensibility | APP-17 (architecture constraint) |
| Legacy system integration (SmartForms, OLDC, state vendors) | INB-02, INB-05, INB-06 (inbound) + OUT-02 (outbound) |

---

## Provenance Summary

| Source | Count | What it covers |
|---|---|---|
| **PWS** | 51 | Directly traceable to the Performance Work Statement |
| **PWS+** | 37 | Derived from or extends PWS requirements |
| **VSA** | 17 | From Value Stream Analysis — scope expansion beyond contract |
| **Discovery** | 15 | From stakeholder interviews, user research, real-world events |
| **Engineering** | 9 | Architectural or implementation decisions by the team |
| **Total** | 129 | |

---

*Product workstreams aligned to VALUE_STREAM_ANALYSIS deliverable architecture. 129 capabilities across 13 sections, each with a stable mnemonic requirement ID. Provenance traces to the PWS (contract authority), VSA (first-principles analysis), Discovery (user research), and Engineering (team decisions).*
