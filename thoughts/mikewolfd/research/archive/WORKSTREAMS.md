# Product Workstreams

> Eleven deliverables for the CSFEER/CORE forms platform, organized by the four-layer architecture from the Value Stream Analysis.
>
> **Derived from:** [MATRIX.md](MATRIX.md) (authoritative requirements registry, source-verified 2026-03-02, WS lineage applied 2026-03-03) + [VALUE_STREAM_ANALYSIS.md](VALUE_STREAM_ANALYSIS.md) (architectural framework).
>
> **Relationship to MATRIX.md:** MATRIX is the authoritative requirements registry — the single source of truth for WHAT the system must do, traced to 39 source documents. This document provides the product architecture view — HOW those requirements organize into deliverable workstreams with dependency analysis, design tensions, and product-level prioritization.
>
> **Priority scale:** **P0** Critical — blocks launch | **P1** Core — required for functional MVP | **P2** Expected — stakeholders assume for production | **P3** Valuable — not essential | **P4** Phase II+ | **P5** Vision
>
> Product priorities (P0–P5) are informed by MATRIX source priorities (M/S/C/W/?) and MVP scope flags.
>
> **MVP scope markers:** ✓ confirmed | ✗ out | ⚡ contested (see [Open Conflicts](#open-conflicts)) | ○ stretch
>
> **Requirement IDs:** MATRIX IDs (FE-xx, WF-xx, etc.) are primary. Items from V2's first-principles analysis not in MATRIX are marked **[WS-xx]**. Implementation decisions from MATRIX tech specs are marked **[D]**.

---

## Changes from V2

1. **MATRIX traceability** — All requirements reference source-verified MATRIX IDs with lineage to S01–S39
2. **MVP scope resolution** — Seven contested scope items explicitly flagged (not assumed)
3. **Priority rebalancing** — Several V2 P1 items now P3+ per MATRIX's "Out of MVP scope per [S21]" flags (APIs, authorization, notifications, federal review)
4. **Persona integration** — UP-01 through UP-11 from MATRIX user personas placed into workstreams
5. **Delivery timeline** — DL-01 through DL-15 milestones integrated
6. **Contract constraints** — CG-01 through CG-14 acknowledged
7. **ID system** — V2 mnemonic IDs (SCH-xx, ENG-xx) replaced by MATRIX IDs; supplementary items marked [WS-xx]

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

**Foundation.** Form Engine Backend, Workflow Rules Engine, System & User Administration, Inbound Integration. Independent of each other; collectively required before the application layer functions.

**Application.** Recipient Application, Form Administration, Internal Workflows UI, Support Tooling. Consumers of the foundation; each independently deployable.

**Terminal.** Reporting Platform, Outbound Integration. Need data flowing through the system before they deliver value.

---

## MVP Scope

### Acceptance & Success Criteria

Full definitions in [MATRIX.md §8–9](MATRIX.md#mvp-definition). Workstream mapping:

| ID | Workstreams | Notes |
|----|-------------|-------|
| AC-01 | 1, 2, 6 | Drives core scope |
| AC-02 | 4 | ⚡ C-13 |
| AC-03 | 11 | |
| AC-04 | All | ⚡ C-2 |
| SC-01–SC-07 | All | SC-07 requires day-one instrumentation (DL-15) |

### Contested MVP Scope

Seven conflicts affect what ships in MVP: C-1 (1, 2, 6), C-4 (10, 11), C-5 (4), C-6 (3), C-7 (3, 8), C-10 (11), C-13 (4).

---

## Specification Layer

### 1. Form Schema Convention

**Core question:** What IS a form?

A specification, not code. The shared grammar that everything else implements or consumes. Must be **program-agnostic from day one** — not CSBG-specific — to support Phase II expansion (LIHEAP, Diaper Program, Rural Development, 60 forms across 8 ACF offices per [S26]).

| MATRIX ID | P | Capability | MVP |
|-----------|---|-----------|-----|
| FE-01 | 0 | Manual data entry: open text, numeric, date, select, narrative | ✓ |
| FE-02 | 0 | Auto-calculated fields using formulas based on other inputs | ✓ |
| FE-04 | 0 | Conditional fields and branching questions | ✓ |
| FE-21 | 0 | Hard errors (blocking) and warning/notification validations | ✓ |
| FE-22 | 0 | Validation scope: field-level, field-group, form-level | ✓ |
| FE-20 | 0 | Flexible validation rules engine (calculations, cross-submission) | ✓ |
| FE-23 | 0 | Automated business logic validation during completion | ✓ |
| FE-05 | 1 | One-to-many response types (multiple responses per question) | ✓ |
| FE-06 | 1 | File attachment fields stored with submission | ✓ |
| FE-07 | 1 | Simple-to-complex form spectrum (internal, [S24]) | ✓ |
| FE-12 | 1 | Reduce variability from custom State/Tribal implementations | ✓ |
| FE-36 | 1 | Short form variant from long form base ($50K threshold) [D] | ✓ |
| FE-10 | — | Pydantic/Python schemas as single source of truth [D] | ✓ |
| FE-30 | 2 | Multiple simultaneous form versions | ✓ |
| [WS-01] | 2 | Data sensitivity classification per field — *trace: AS-20 (CUI) + PM-01 (access controls) imply per-field tiers* | ○ |
| [WS-02] | 2 | PRA metadata per form (OMB number, expiration, burden) — *operational dependency; see MATRIX FI section PRA note ([S03], [S05], [S13])* | ○ |
| [WS-03] | 3 | Schema-driven definitions decoupled from hardcoded UI — *trace: FE-10 + FE-42 + FE-40 imply this direction* | ○ |

**Conflict:** C-1 (FE-25) — Validation timing. [S29] implies inline during entry; [S21] implements review-page-only. Resolution determines whether validation is a schema-level or rendering-level concern.

**Stress points:** Auto-calculated fields with cross-field formulas (FE-02). Multi-version definitions with submission pinning (FE-30). Dual hard-error/warning semantics that don't block partial saves (FE-21).

**Blocks:** everything. **Blocked by:** product decisions on scope; multi-tenancy isolation model.

---

## Foundation Layer

### 2. Form Engine Backend

**Core question:** How do we store and process form data?

Persistence, APIs, validation execution, versioning, submission history. The stable core that outlives any frontend. Build sequence per DL-05: rendering → saving → review page → auto-save → PDF export.

| MATRIX ID | P | Capability | MVP |
|-----------|---|-----------|-----|
| FE-09 | 0 | JSON field storage in FormEntry model [D] | ✓ |
| FE-08 | 0 | Interview-style page-by-page via POST [D] | ✓ |
| FE-33 | 0 | Form status lifecycle: draft → submitted → amended → archived [D] | ✓ |
| WF-11 | 0 | Save progress and return later (partial saves with invalid data) | ✓ |
| WF-04 | 1 | Recipients can unsubmit forms | ✓ |
| WF-05 | 1 | Recipients submit revisions to submitted forms | ✓ |
| WF-06 | 1 | Submit action (distinct from save) (internal, [S24]) | ✓ |
| FE-11 | 1 | FormDefinition records linking to Python schema [D] | ✓ |
| FE-34 | 1 | Audit trail for all form actions (internal, [S24]/[S21]) | ✓ |
| FE-35 | 1 | Field-level change logging via FormAuditDetail [D] | ✓ |
| FE-31 | 2 | Version history: view submission at various workflow points | ✓ |
| FE-32 | 2 | Historical comparison: recipients view past submissions | ✓ |
| FE-38 | 2 | Auto-save every 30–60s with success/failure messaging [D] | ✓ |
| FE-47 | 2 | Concurrent edit conflict handling for periodic auto-save (extends FE-38) | ○ |

**Design tension:** WF-11 allows partial saves with invalid data. FE-23/FE-25 (C-1) demand validation during entry. Proposed resolution: validation fires but doesn't block saves — warnings inform, only submission is gated by hard errors.

**Blocks:** Recipient Application, Internal Workflows UI, Reporting, Outbound Integration. **Blocked by:** Form Schema Convention.

---

### 3. Workflow Rules Engine

**Core question:** What are the rules for moving submissions through their lifecycle?

State machine, routing rules, approval logic, notification triggers. Frontends render workflow state; this workstream owns the rules. **Heavily affected by contested scope — 3 of 7 conflicts (C-5, C-6, C-7) touch this workstream.**

| MATRIX ID | P | Capability | MVP |
|-----------|---|-----------|-----|
| WF-01 | 1 | Auto-create/initialize forms with pre-populated data per schedule | ✓ |
| WF-02 | 1 | Show trends over time using previous year data | ✓ |
| WF-12 | 1 | Previously submitted data available to limit repeat requests | ✓ |
| WF-14 | 1 | Deadline-aware notifications (March 31 per WF-18, CSBG Act §678(b)) | ✓ |
| WF-17 | 2 | Tracking and collaboration visibility across lifecycle | ✓ |
| WF-18 | 2 | March 31 statutory submission deadline enforcement | ✓ |
| WF-09 | 3 | Customizable multi-step, multi-person federal review | ⚡ C-7 |
| WF-13 | 3 | Customizable real-time alerts and notifications | ⚡ C-6 |
| WF-15 | 3 | Multi-user data entry, routing, re-submission | ⚡ C-7 |
| WF-10 | 4 | Visual/no-code workflow builder | ✗ |
| [WS-07] | 3 | Conditional routing based on submission attributes — *trace: [S37] open question "Conditional routing (e.g., budget threshold triggers CFO step)?"* | ○ |
| [WS-08] | 4 | Parallel approval branches with join logic — *trace: [S37] open question "Sequential vs. parallel review steps?"* | ✗ |
| [WS-09] | 4 | Delegation and escalation rules — *trace: [S37] open question "Delegation and override rules?"* | ✗ |

**Contests:** C-6 (notifications) and C-7 (approval workflows) flagged as Must in [S29] but Out of MVP in [S21]. If federal review stays post-MVP, WF-09/WF-13/WF-15 move to P4. If MVP requires any review, a minimal approve/revise pipeline (not configurable) becomes P1.

**Blocks:** Internal Workflows UI. **Blocked by:** Form Schema Convention.

---

### 4. System & User Administration

**Core question:** Who can do what?

Authentication, authorization, organization hierarchy, role-permission model. Dual external dependencies: Okta for government users, Login.gov (or alternative) for non-government users. Has its own tech spec ([S27]) and critical open questions.

#### Authentication

| MATRIX ID | P | Capability | MVP |
|-----------|---|-----------|-----|
| AS-03 | 0 | Government users via login.acf.gov (Okta) | ✓ |
| AS-05 | 0 | OIDC Authorization Code Flow + PKCE, server-side tokens [D] | ✓ |
| AS-06 | 0 | Keycloak local dev mock (realm: csfeer) [D] | ✓ |
| AS-18 | 0 | Basic session management; Login.gov deferred [D, S31] | ✓ |
| AS-01 | 1 | Login.gov for non-government users | ⚡ C-13 |
| AS-04 | 1 | Non-government auth path (TBD — risk R-08) | ⚡ C-13 |
| AS-10 | 2 | Auto-provision user + org on first login [D] | ✓ |
| AS-07 | 2 | Role mapping from JWT claims — Okta format TBD [D] | ✓ |
| AS-11 | 2 | Group memberships re-synced from token on login [D] | ✓ |
| AS-12 | 2 | RP-initiated logout with Okta session termination [D] | ✓ |

#### Authorization

| MATRIX ID | P | Capability | MVP |
|-----------|---|-----------|-----|
| PM-01 | 1 | Flexible permissions: read, write, export controls | ⚡ C-5 |
| PM-02 | 2 | Self-service user management by org admins | ⚡ C-5 |
| PM-03 | 2 | Hierarchical admin: sub-recipient, state, federal | ⚡ C-5 |
| PM-04 | 2 | Minimum permission levels per role at each level | ⚡ C-5 |
| PM-05 | 2 | Varying levels: view-only, view+edit, view+submit | ⚡ C-5 |
| PM-06 | 2 | 75 federal staff with review/route/approve/analyze/export | ✓ |
| PM-07 | 2 | Roles via Okta group syncing [D] | ✓ |
| PM-08 | 2 | Authorization and access control | ⚡ C-5 |
| UP-01 | 2 | Three grantee tiers: Approver, Contributor, Viewer ([S32]) | ⚡ C-5 |
| UP-08 | 3 | Unified admin console: search by org/person/email/UEI ([S32]) | ✗ |

**Contests:** C-5 (authorization out of MVP per [S21]) and C-13 (Login.gov deferred per [S31] but required by AC-02). If authorization stays out, UP-01 role tiers and PM-01–PM-05 move to post-MVP — but then how does the system distinguish who can submit vs who can only view?

**Open questions:** Non-gov auth path (AS-04, risk R-08) has no resolution timeline. Okta/Login.gov token claim structure mismatch (AS-07) needs verification.

**Blocks:** all feature work (authentication gates everything). **Blocked by:** Okta configuration, non-gov auth decision.

---

### 5. Inbound Integration

**Core question:** How does external data flow into the platform?

Pre-population pipelines, entity validation (SAM.gov UEI), prior-year data. Maps external data into the schema convention.

| MATRIX ID | P | Capability | MVP |
|-----------|---|-----------|-----|
| FE-03 | 1 | Pre-population connecting pre-award to post-award data | ✓ |
| FE-37 | 1 | Cross-form: Tribal Plan pre-populates from Tribal AR [D] | ✓ |
| FE-46 | 1 | UEI as cross-form pre-population key [D] | ✓ |
| DA-10 | 2 | OLDC DataConnect/Excel exports as migration source | ✓ |
| DA-11 | 2 | Pre-population limited to high-confidence data only (internal) | ✓ |
| FE-24 | 2 | SAM.gov UEI mismatch detection | ○ |
| DA-12 | 3 | SmartForms XML/XSD validation artifacts as reference | ○ |
| DA-13 | 3 | FY24 raw data exports (RVW/RPT prefix) for schema reference | ○ |

**Open question:** Data migration (DA-10, DA-12, DA-13) is a precondition for pre-population. OLDC has operated since ~2015. Is migration a component of this workstream or a separate concern? Risk R-04 (Med × Med) and R-14 (OLDC user isolation) apply.

**Blocks:** Recipient Application (pre-population). **Blocked by:** Form Schema Convention, OLDC data access (Thomas Oldfield is data liaison).

---

## Application Layer

### 6. Recipient Application

**Core question:** How do grantees fill out forms?

Grantee-facing interface. Form rendering, save/resume, low-connectivity resilience, validation feedback, submit/revise lifecycle. Design cycle: Figma V1 → V1.3 → usability testing. Consumes the schema but never touches federal review screens.

| MATRIX ID | P | Capability | MVP |
|-----------|---|-----------|-----|
| AD-01 | 0 | Section 508 WCAG AA-compliant front end | ✓ |
| AD-02 | 0 | USWDS as design system | ✓ |
| AD-05 | 0 | Clear user location in multi-step process | ✓ |
| AD-06 | 0 | Plain, familiar language throughout | ✓ |
| FE-43 | 1 | Screener flow routing to correct form [D] | ✓ |
| AD-04 | 1 | Optimized for tablets and laptops (internal, [S24]) | ✓ |
| FE-25 | 1 | Validation feedback during entry | ⚡ C-1 |
| FE-44 | 2 | Client-side caching via IndexedDB/localStorage [D] | ✓ |
| FE-45 | 2 | Connection state indicators: Saved / Lost / Synced [D] | ✓ |
| AD-08 | 2 | Consistent visual identity with agency branding | ✓ |
| AD-09 | 2 | Low-bandwidth/rural support (Alaska named explicitly) | ✓ |
| AD-11 | 2 | VPAT/ACR required for commercial ICT (internal, [S33]) | ✓ |
| UP-02 | 2 | SF-424M cross-referencing guidance ([S32]) | ○ |
| UP-03 | 2 | Transmittal letter/attestation as distinct artifact ([S32]) | ○ |
| UP-06 | 2 | Visual diff: per-field "what changed from last year" ([S32]) | ○ |
| UP-07 | 3 | Simplified summary view for leadership briefings ([S32]) | ○ |
| AD-12 | 3 | WCAG 2.1/2.2 AA advisable (2.0 is contractual) (internal, [S33]) | ○ |
| WF-15 | 3 | Multi-person collaboration on single form (app-layer UI of WF-15) | ⚡ C-7 |
| [WS-11] | 4 | Offline-first field administration (ANA, CB on-site) — *trace: AD-09 + FE-44 + [S06] "ANA — offline/in-person administration needed"* | ✗ |

**Stress points:** Validation UX (C-1 resolution determines inline vs review-page). Contextual guidance at scale — AD-13 (some forms have 62–150 page companion documents). Low-connectivity resilience with auto-save (FE-38 + FE-44 + AD-09).

**Blocks:** usability testing, beta, pilot. **Blocked by:** Schema, Engine, Auth, Inbound Integration.

---

### 7. Form Administration

**Core question:** How are forms built, tested, published, and versioned?

MVP = developer-authored Pydantic schemas via `load_initial_forms`. Year 2+ = visual builder.

| MATRIX ID | P | Capability | MVP |
|-----------|---|-----------|-----|
| FE-11 | 0 | FormDefinition deployment via management command [D] | ✓ |
| FE-42 | 1 | Enable faster form design/update/test for program staff | ✓ |
| FE-30 | 2 | Version management: current, retired, submission-pinned | ✓ |
| [WS-12] | 2 | Form inventory visibility (what exists, who uses it, counts) — *trace: FI-01–FI-06 (inventory) + FE-42 (faster design implies knowing what exists)* | ○ |
| [WS-13] | 2 | PRA tracking per form (Melanie ~half, Monique ~half) — *operational dependency; see MATRIX FI section PRA note ([S03], [S05], [S13])* | ○ |
| FE-40 | 4 | Low-code/no-code form builder (post year 1) | ✗ |
| FE-41 | 4 | Sandbox/testing space for form builder | ✗ |

**Open question:** Form definitions require developer effort until a visual builder ships. How program staff communicate form changes, turnaround time for schema updates, and the testing process determine whether the platform behaves like a product or a custom build. Risk R-13 (policy changes mid-development) applies.

**Blocks:** Recipient Application (needs published definitions). **Blocked by:** Schema.

---

### 8. Internal Workflows UI

**Core question:** How do federal staff review, approve, and act on submissions?

Federal review interface. Completely different users from grantees with different UX needs. Key users: Melanie Durley (Congressional reporting), Monique Alcantara (OLDC/PM website), Kayla Lennon (CQI), Lena Kotanchyan (data analysis). Each manages 15–25 grantees (UP-04).

| MATRIX ID | P | Capability | MVP |
|-----------|---|-----------|-----|
| UP-04 | 2 | Portfolio dashboard: status per form per grantee ([S32]) | ✓ |
| UP-05 | 2 | Batch review + structured export for cross-grantee comparison ([S32]) | ✓ |
| UP-06 | 2 | Visual diff per field, year-over-year ([S32]) | ○ |
| WF-09 | 3 | Multi-step review and approval pipeline | ⚡ C-7 |
| WF-09 | 2 | Review actions: approve, request revision, reject (UI surface of WF-09) | ⚡ C-7 |
| UP-03 | 3 | Transmittal letter tracking (federal side of UP-03 in workstream 6) | ○ |
| [WS-16] | 3 | Congressional reporting tools (Melanie's workflow) — *see MATRIX DA-09 note; data flows: exports → PM website → Congress ([S01], [S03], [S29])* | ○ |
| [WS-17] | 3 | CQI workflow integration (Kayla's sprints) — *see MATRIX WF-17 note; CQI consumes collaboration visibility ([S03], [S05])* | ○ |

**Contest:** C-7 — if federal review is post-MVP, this entire workstream shifts to P3+. But AC-01 says "save/submit" which implies someone receives submissions. Minimum viable: read-only submission view for federal staff, no formal review pipeline.

**Blocks:** production launch (no review = no submission pipeline). **Blocked by:** Engine, Workflow Rules, Auth.

---

### 9. Support Tooling

**Core question:** How do users get help when they're stuck?

| MATRIX ID | P | Capability | MVP |
|-----------|---|-----------|-----|
| AD-13 | 2 | In-context field guidance and companion document integration (extends UP-02) | ○ |
| UP-12 | 3 | 4-tier support model: in-app help → help desk → tech escalation → on-site ([S35], [S32]) | ○ |
| [WS-19] | 3 | Staff support console with scoped read-only access — *orphaned; VSA-derived* | ✗ |
| [WS-20] | 3 | Trackable support interactions (category, resolution, time) — *orphaned; VSA. SC-15 (≤1 ticket/org) implies tracking* | ✗ |
| [WS-21] | 4 | Full-featured help desk tooling — *orphaned; VSA. R-05 mitigation mentions "help desk support"* | ✗ |

Thinnest workstream. Targets: <60 tickets/month (PR-19), ≤1 ticket per org (SC-15). Soft launch (DL-11) includes white-glove support with weekly check-ins tapering to bi-weekly.

**Blocks:** nothing. **Blocked by:** Recipient Application, Auth.

---

## Terminal Layer

### 10. Reporting Platform

**Core question:** How does collected data become actionable insight?

Export packaging, data access, API documentation. Portfolio dashboards (UP-04) and cross-grantee comparison/outlier detection (UP-05) live in workstream 8 (Internal Workflows UI) as they serve federal review users. Natural home for the overarching telemetry objective — creating the **first measurable baseline** for tribal reporting (SC-07).

| MATRIX ID | P | Capability | MVP |
|-----------|---|-----------|-----|
| DA-03 | 1 | Data exports: API, CSV, human-readable formats | ✓ |
| DA-07 | 2 | Real-time data access without hindering performance | ✓ |
| DA-14 | 2 | Easy export/review/correction of data errors | ✓ |
| DA-06 | 2 | Comprehensive, easy-to-understand API documentation | ✓ |
| DA-05 | 3 | Public access links to specific submission portions | ○ |
| DA-09 | 3 | Performance Management website feed (Monique is COR) | ○ |

**Observability:** 90-day post-launch baseline telemetry (DL-15) requires instrumentation from day one — not post-MVP. OCS currently has zero telemetry on workflow efficiency, error patterns, or user burden.

**Blocks:** nothing. **Blocked by:** submissions flowing through full submit-review cycle.

---

### 11. Outbound Integration

**Core question:** How does structured data flow out of the platform?

| MATRIX ID | P | Capability | MVP |
|-----------|---|-----------|-----|
| DA-04 | 0 | Individual form submission PDF export | ✓ |
| DA-08 | 0 | WeasyPrint (HTML/CSS → PDF) [D] | ✓ |
| FE-39 | 0 | PDF generated from review page data, not raw form data [D] | ✓ |
| DA-03 | 1 | CSV/human-readable exports (AC-03) | ✓ |
| DA-01 | 2 | Flexible read API for forms, submissions, bulk | ⚡ C-4 |
| DA-02 | 3 | Write API for importing pre-populated data | ⚡ C-4 |
| DA-15 | 2 | Conditional-logic-aware PDF: omit non-applicable sections from output | ○ |

**Contests:** C-4 — APIs are Must per [S29] but out of MVP per [S21], stretch per [S31]. If included, read-only only per [S35]/[S39]. C-10 — WeasyPrint vs headless Chrome; [S18] specifies WeasyPrint.

**Blocks:** nothing. **Blocked by:** Engine, Schema.

---

## Cross-Cutting Concerns

### Data Sensitivity

Federal grant data includes vulnerable populations: tribal nations, families in poverty, children, domestic violence survivors. CUI handling per NIST required (AS-20). AI policy: federal data cannot train commercial AI models without approval (AS-21). Every workstream that touches submission data must respect sensitivity tiers.

### Audit Trail

FormAuditTrail (FE-34) and FormAuditDetail (FE-35) as persistence layer. Every workstream emits audit events: form creation, field edits, permission changes, state transitions, review actions, exports. All IP is property of ACF (CG-13).

### Multi-Tenancy

Platform serves multiple program offices in Phase II+ (PH-02 through PH-04: 25,000+ recipients, 100+ forms across all ACF offices). Program-level isolation touches the schema convention, authorization model, and every query surface. Isolation model is an **unresolved design decision**.

### Observability & Telemetry

First measurable baseline for tribal reporting (SC-07). Day-one instrumentation for 90-day post-launch baseline (DL-15).

| Category | Primary Workstream | Key Metrics |
|----------|-------------------|-------------|
| User interaction | Recipient Application | Sessions per submission, autosave success ≥98% (SC-12) |
| Submission quality | Form Engine Backend | Validation passes without help ≥90% (SC-09), errors self-resolved ≥85% (SC-10) |
| Performance | Infrastructure | Load/save ≤3s on 4G (PR-01), p95/p98 latency (PR-06), ≥200 concurrent users (PR-11) |
| Operational | Reporting Platform | Tickets <60/mo (PR-19), OCS review time ≥25% reduction (SC-19) |

---

## Security & Compliance

ATO target: **May 29, 2026** (AS-15). **#1 risk** (R-06, p×i = 0.45). Produces artifacts, not features. Every workstream that handles data must produce security documentation inputs.

| MATRIX ID | P | Item | Status (Feb 2026) |
|-----------|---|------|-------------------|
| AS-14 | 0 | ATO within 18 months | In progress |
| AS-16 | 0 | SORN (System of Records Notice) | Required |
| AS-17 | 0 | PIA (Privacy Impact Assessment) | Under review (AS-A2) |
| AS-19 | 0 | Zero Trust strategy per EO 14028 | Required |
| AS-20 | 0 | CUI handling per NIST | Required |
| AS-A4 | 0 | System Security Plan (SSP) | In progress |
| AS-A12 | 1 | Appendix X ("as much effort as all others combined") | In progress |
| AS-A11 | 1 | Security Assessment Plan | In progress |
| AS-A13 | 1 | Interconnection Security Agreement (ISA) | In progress |
| AS-22 | 2 | Personnel security: backgrounds, NDAs, training | Ongoing |
| AS-23 | 2 | High-risk Public Trust clearance | Affects onboarding |
| AS-24 | 2 | Incident response SLAs: Critical <1hr, High <4hrs | Required |

**Conflict:** C-3 — FISMA classification. [S24] says Moderate; [S12] says Rev5-Low. Resolution affects entire control baseline and audit scope.

**Blocks:** production launch (hard gate). **Blocked by:** FISMA/PIA classification (C-3), external review timelines.

---

## Infrastructure & Deployment

| MATRIX ID | P | Decision | MVP |
|-----------|---|---------|-----|
| IT-01 | 0 | Python 3.12, Django 6.0+ | ✓ |
| IT-02 | 0 | PostgreSQL on NGSC AWS | ✓ |
| IT-03 | 0 | AWS ECS (not Kubernetes) | ✓ |
| IT-10 | 0 | NGSC AWS production (inherit existing controls) | ✓ |
| IT-04 | 0 | Alpine.js 3.15+ for frontend reactivity | ✓ |
| IT-05 | 0 | USWDS 3.13+ for UI components | ✓ |
| IT-06 | 0 | Django Ninja 1.4+ for REST APIs | ✓ |
| IT-11 | 1 | GitLab with GitHub mirroring | ✓ |
| IT-18 | 1 | PIV cards + GFE for NGSC access; Zscaler for network | ✓ |
| PR-01 | 1 | Form load/save ≤3s on typical 4G connection (internal, [S24]) | ✓ |
| PR-03 | 1 | ≥99.5% uptime excluding scheduled maintenance (internal, [S24]) | ✓ |
| PR-10 | 1 | 24/7 operational availability | ✓ |
| PR-11 | 1 | ≥200 concurrent users (internal, [S24]) | ✓ |
| PR-12 | 2 | FISMA Moderate, FedRAMP hosting, FIPS 140-2 (internal, [S24]) | ✓ |
| PR-13 | 2 | Chrome, Firefox, Edge, Safari support (internal, [S24]) | ✓ |
| PR-15 | 2 | Test coverage >80% (internal, [S35]) | ✓ |
| PR-16 | 2 | 3G network testing in addition to 4G (internal, [S35]) | ✓ |

**Blocks:** everything (nothing deploys without infra). **Blocked by:** NGSC provisioning, PIV/GFE access (IT-18).

---

## Delivery Milestones

Contract: 24-month (12+12), ~4.75 FTE core + surge at M4–9 and M13–15 (CG-01). Bi-weekly release cadence (CG-03).

| MATRIX ID | Target | Milestone | Workstreams |
|-----------|--------|-----------|-------------|
| DL-01 | 2026-03-01 | Landing page deployed | 6, Infra |
| DL-02 | 2026-03-15 | Tribal Annual Report (long form) complete | 1, 2, 6 |
| DL-03 | 2026-03-31 | Tribal Plan and Application complete | 1, 2, 6 |
| DL-04 | 2026-03-31 | ATO documentation package submitted | Sec |
| DL-05 | — | Build sequence: rendering → saving → review → auto-save → PDF | 2, 6, 11 |
| DL-11 | Month 9 | Soft launch to 10–12 tribal orgs (white-glove support) | All |
| DL-12 | Month 12 | Wave-based full rollout (post-ATO) | All |
| DL-13 | Various | Stage gates: Discovery (M2), MVP (M8), Pilot (M9), Continuous (M15) | All |
| DL-15 | Post-launch | 90-day baseline telemetry across all four dimensions | 10, Cross-cutting |

**Critical path for March 15:** Schema (1) → Engine rendering (2) → data saving → review page → auto-save. No flexibility in sequence (DL-05). 192 story points across 6 epics (~11–12 weeks, ~4.75 FTE) — aggressive with no velocity benchmarks (DL-06).

---

## Risks by Workstream

R-06 → Sec | R-05 → 6, 9 | R-02 → 6 | R-08 → 4 | R-04 → 5 | R-01 → Delivery | R-14 → 4, 5 | R-12 → 3, 8 | R-13 → 1, 7

---

## Open Conflicts

Five MVP-blocking: **C-1** (1, 2, 6), **C-3** (Sec, Infra), **C-5** (4), **C-7** (3, 8), **C-13** (4). Others: C-2 (All), C-4 (10, 11), C-6 (3), C-8 (Delivery), C-9 (Observability), C-10 (11), C-11 (Context), C-12 (Delivery).

---

---

*~156 capabilities across 11 workstreams. MATRIX.md is the authoritative requirements registry; this document maps requirements to deliverable workstreams with dependency analysis and product-level prioritization.*
