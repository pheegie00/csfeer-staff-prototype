# Value Stream Analysis — CSFEER/CORE

A first-principles decomposition of the product space into value streams and deliverables. Independent of implementation sequence, team structure, and current codebase. The reference for prioritization, architecture, and scope decisions.

Program-specific behavior belongs in configuration. Everything below describes a general-purpose, cross-program-office forms platform. CSBG tribal forms are the first instantiation.

---

## Value Streams

Seven distinct flows of value to distinct stakeholder groups. Each has its own users, journey, and definition of done.

### 1. Grantee Submission

**Who:** Grant recipients at any tier (tribes, states, territories, eligible entities, sub-recipients) across any ACF program office.

**Journey:** Receive reporting obligation. Find the correct form via screener or assignment. Enter data across multiple sessions with collaborators. Run validation, resolve errors. Obtain leadership sign-off. Submit.

**Outcome:** Reporting obligation fulfilled with minimal burden. Data enters the system validated and structured.

**Requires:** Form definitions assigned. Prior-year data pre-populated. Authentication and permissions resolved. Validation rules executing in real time.

### 2. Federal Review

**Who:** Program Specialists, review leads, approvers across any program office.

**Journey:** Submission arrives. Reviewer is notified. Reviews against policy and data quality expectations. Routes through configured approval pipeline. Approves, requests revision with feedback, or rejects. Closes the review cycle.

**Outcome:** Consistent oversight, visible and auditable. No email chains. No spreadsheets.

**Requires:** Submissions in the system. Workflow routing rules configured. Reviewer permissions scoped to their program and grantee assignments.

### 3. Reporting & Analytics

**Who:** Program analysts, agency leadership, Congressional reporting staff, public accountability audiences.

**Journey:** Approved submission data becomes queryable. Staff explores portfolio-level views. Performs cross-grantee comparisons and year-over-year trend analysis. Identifies outliers. Packages findings for the appropriate audience.

**Outcome:** Collected data gets used. Raw submissions become actionable insight.

**Requires:** Submissions through the full submit-review cycle. Data queryable without degrading operational performance. Export formats serving diverse consumers.

### 4. System Administration

**Who:** Program office staff (form configuration), system administrators (user and org management), technical staff (operational health).

**Journey:** Define a reporting cycle. Configure or update form definitions. Test in sandbox. Publish. Assign forms to recipients. Set deadlines and notification rules. Manage user access. Monitor system health.

**Outcome:** The platform operates without engineering intervention for routine operations.

**Requires:** Form schema supporting non-technical authoring (long-term). Self-service user and permission management at every organizational tier.

### 5. Data Integration

**Who:** The platform itself (automated pipelines), agency technical staff (API consumers), external system operators, downstream data consumers.

**Journey:** External data flows in (grant management records, entity validation like SAM.gov UEI, prior-year submissions). Pre-populates form fields and validates against authoritative sources during entry. Collected and approved data flows out via APIs, exports, and public access links.

**Outcome:** The platform connects to the broader grants ecosystem. Context flows in to reduce burden. Structured data flows out to serve analysis, compliance, and interoperability.

**Requires:** Inbound integration operational before the Recipient Application delivers full pre-population value. Outbound integration requires data in the system. Both depend on the schema convention for mapping external data.

### 6. Compliance & Audit

**Who:** OIG, OMB, legal counsel, FOIA officers, ISSO, agency records managers.

**Journey:** Oversight body verifies data was collected lawfully, stored correctly, retained appropriately, reproducible on demand. Queries audit trails. Reviews chain-of-custody metadata. Verifies PRA clearance status. Produces compliance artifacts.

**Outcome:** The platform can prove it did the right thing to anyone authorized to ask.

**Requires:** Every deliverable emitting audit events. Schema convention including PRA metadata. Records retention policies defined and enforced. Field-level access controls for data sensitivity tiers.

### 7. Grantee Support

**Who:** Program office staff providing technical assistance, TTA providers, grant recipients who need help.

**Journey:** Grantee cannot complete a form, does not understand a rejection, cannot resolve a validation error. Initiates support interaction. Issue is diagnosed: usability, data, permissions, or policy. Guided to resolution. Issue resolved, grantee continues.

**Outcome:** The platform works for its most constrained users. Support interactions are tracked and patterns feed product improvement.

**Requires:** Recipient Application surfacing contextual help and explanatory validation. Support staff with scoped access to grantee form state. Trackable support interactions.

---

## Product Deliverables

Twelve concrete things to build, ship, and track. Organized by layer.

| #   | Deliverable                      | Layer         | What It Produces                                                                                                                                                                                                                 |
| --- | -------------------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Form Schema Convention**       | Specification | The shared grammar: field primitives, composition rules, validation semantics, versioning rules, data sensitivity classification. A specification, not code. Everything else implements or consumes it.                          |
| 2   | **Form Engine Backend**          | Foundation    | Persistence for form definitions and submissions. APIs for form lifecycle operations. Validation execution. Versioning and submission history. The stable core that outlives any frontend.                                       |
| 3   | **Workflow Rules Engine**        | Foundation    | Submission lifecycle state machine. Routing rules, approval logic, delegation, escalation, conditional routing. The frontends render workflow state; this owns the rules.                                                        |
| 4   | **System & User Administration** | Foundation    | Users, organizations, roles, permissions, authentication. Understands schema vocabulary for scoping permissions to forms, sections, and fields. Enforces field-level access control. Self-service at every organizational level. |
| 5   | **Inbound Integration**          | Foundation    | Pre-population pipelines: grant management records, entity validation (SAM.gov UEI), prior-year submissions. Maps external data into the schema convention. Designed to onboard new sources as programs adopt the platform.      |
| 6   | **Recipient Application**        | Application   | Grantee-facing interface. Form rendering, save/resume, collaboration, low-connectivity resilience, real-time validation with explanatory messages, submit/revise lifecycle. Consumes the Form Engine Backend via APIs.           |
| 7   | **Form Administration**          | Application   | Build, test, publish, and version form definitions. PRA metadata management. Sandbox environment for draft forms. This deliverable transforms the platform from a bespoke build into a reusable engine.                          |
| 8   | **Internal Workflows UI**        | Application   | Federal review and approval interface. Review queues, routing visualization, approval actions, revision requests with feedback. Consumes Workflow Rules Engine and Form Engine Backend.                                          |
| 9   | **Support Tooling**              | Application   | Contextual help and guided walkthroughs in the Recipient Application. Staff-side support console with scoped access to grantee form state. Pattern tracking for systemic issues.                                                 |
| 10  | **Reporting Platform**           | Terminal      | Portfolio dashboards, cross-grantee comparison, year-over-year trends, outlier detection, compliance/audit trail access, export packaging.                                                                                       |
| 11  | **Outbound Integration**         | Terminal      | APIs for external consumers, CSV and PDF export, public access links with field-level visibility controls.                                                                                                                       |
| 12  | **Platform Operations**          | Operations    | Security authorization artifacts, deployment infrastructure, environment management, operational monitoring. The substrate that makes all other deliverables available to users. Not a product capability — the capability to operate the product. |

### Layers

**Specification.** The Form Schema Convention. Everything implements or consumes it.

**Foundation.** Form Engine Backend, Workflow Rules Engine, System & User Administration, Inbound Integration. Independent of each other. Collectively required before the application layer functions.

**Application.** Recipient App, Form Administration, Internal Workflows UI, Support Tooling. Consumers of the foundation. Each independently deployable and replaceable.

**Terminal.** Reporting Platform, Outbound Integration. Need data flowing through the system before they deliver value.

**Operations.** Platform Operations. Security authorization, deployment infrastructure, monitoring. Orthogonal to the product capability layers — it does not consume the schema convention or produce product features. It produces the ability to deploy and run everything else. Gates when any deliverable reaches users, not what the deliverable does.

### Dependency Graph

```
           ┌─────────────────────┐
           │  Form Schema        │  ← specification
           │  Convention         │
           └────────┬────────────┘
                    │                                    ┌──────────────────┐
   ┌────────────────┼────────────────┬──────────────┐    │    Platform      │
   ▼                ▼                ▼              ▼    │    Operations    │
 Form Engine      Workflow        System &       Inbound │                  │
 Backend          Rules           User Admin     Integ.  │  Gates when any  │
   │                │                │              │    │  deliverable     │
   ├────────────────┼────────────────┼──────────────┤    │  reaches users   │
   ▼                ▼                ▼              ▼    │                  │
 Recipient       Internal         Form          Support  │  ← operations   │
 App             Workflows UI     Admin         Tooling  └──────────────────┘
   │                │                │              │
   └───────┬────────┘────────────────┘──────────────┘
           │
   ┌───────┴────────┐    ┌────────────────┐
   │   Reporting    │◄───│   Outbound     │
   │   Platform     │    │  Integration   │
   └────────────────┘    └────────────────┘
```

---

## Value Stream × Deliverable Matrix

Primary reference for tracing dependencies. If a deliverable changes, this shows which value streams are affected.

|                           | Schema Conv. | Engine Backend | Workflow Rules | Sys & User Admin | Inbound Integ. | Recipient App | Form Admin | Workflows UI | Support Tooling | Reporting Platform | Outbound Integ. | Platform Ops |
| ------------------------- | :----------: | :------------: | :------------: | :--------------: | :------------: | :-----------: | :--------: | :----------: | :-------------: | :----------------: | :-------------: | :----------: |
| **Grantee Submission**    |              |       ●        |                |        ●         |       ●        |       ●       |            |              |                 |                    |                 |              |
| **Federal Review**        |              |       ●        |       ●        |        ●         |                |               |            |      ●       |                 |                    |                 |              |
| **Reporting & Analytics** |              |       ●        |                |                  |                |               |            |              |                 |         ●          |        ●        |              |
| **System Administration** |      ●       |                |                |        ●         |                |               |     ●      |              |                 |                    |                 |      ●       |
| **Data Integration**      |      ●       |       ●        |                |                  |       ●        |               |            |              |                 |                    |        ●        |              |
| **Compliance & Audit**    |              |       ●        |                |        ●         |                |               |     ●      |              |                 |         ●          |                 |      ●       |
| **Grantee Support**       |              |       ●        |                |        ●         |                |       ●       |            |              |        ●        |         ●          |                 |              |

---

## Cross-Cutting Concerns

Three concerns span the entire deliverable map. They live in no single deliverable; every deliverable must account for them.

**Data sensitivity.** Federal grant programs handle data about vulnerable populations: tribal nations, families in poverty, children, domestic violence survivors. Sensitivity varies by program and field. Field-level access control must be part of the schema convention and enforced by System & User Administration. Every deliverable that touches submission data respects sensitivity tiers.

**Audit trail.** Every deliverable emits audit events: form creation, field edits, permission changes, submission state transitions, review actions, export operations. Compliance & Audit consumes these events. Audit is an obligation every deliverable fulfills, not a separate application.

**Multi-tenancy.** The platform serves multiple program offices, each with their own forms, recipients, review workflows, and data. Program-level isolation touches the schema convention, the authorization model, and every query surface. The isolation model (tenant, permission, data partitioning, or hybrid) is an unresolved design decision that constrains all foundation-layer deliverables.

---

*First-principles decomposition of the CSFEER/CORE product space. Independent of current codebase, team structure, or procurement framing. CSBG tribal forms are the initial instantiation; the analysis describes a platform that serves any ACF program office. Platform Operations (D12) is the one deliverable that is implementation-specific by nature — it is included because security authorization and deployment infrastructure gate when all other deliverables reach users.*
