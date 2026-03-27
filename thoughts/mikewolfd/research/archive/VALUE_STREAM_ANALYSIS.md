# Value Stream Analysis Synthesis — CSFEER/CORE

## Executive Summary

The CSFEER/CORE mandate — replacing legacy PDF-based grant reporting with a
scalable, cross-program-office digital forms platform — contains not one product
but a product ecosystem. While the initial instantiation targets CSBG tribal
forms, the platform must serve any ACF program office, any form type, and any
recipient population. This analysis decomposes that ecosystem from first
principles, independent of the current codebase, procurement structure, or
initial program scope.

**What we found:** 7 distinct value streams serving 4 stakeholder tiers
(grantees, federal operational staff, federal leadership and oversight bodies,
support providers), supported by 6 shared capability domains, realized through
11 product deliverables. Each stream has its own users, its own journey, and its
own definition of success.

**Why it matters:** Treating the platform as a monolithic build obscures
prioritization, creates hidden coupling between unrelated concerns, and
concentrates risk. The deliverables have a natural dependency order — building
them out of sequence costs significantly more than building them in the right
sequence.

**The monolith is fine.** This analysis is not an argument for microservices or
separate deployments. A 6-person team should start with a single codebase and a
single deploy. But thinking in value streams and deliverables from day one is
what preserves the ability to evolve, split, and scale the platform over its
lifetime. Just because you start as a monolith doesn't mean you can't separate
things later — but only if the conceptual boundaries were clear from the start.
Lose that clarity early and the coupling becomes structural, making future
separation expensive or impossible.

---

## The 7 Value Streams

Each stream represents a distinct flow of value to a distinct stakeholder group.
They are not features or epics — they are end-to-end journeys through the
platform that define what "done" looks like for different users.

These streams are defined program-agnostically. While the initial build targets
CSBG tribal forms, every stream must work identically for any ACF program
office — LIHEAP, Head Start, TANF, or any future program that onboards to the
platform. Program-specific behavior lives in form definitions and configuration,
not in the streams or the deliverables that support them.

### 1. Grantee Submission

- **Who:** Grant recipients at any organizational tier — tribes, states,
  territories, eligible entities, sub-recipients. The platform must serve
  recipients across all ACF program offices, not just one program.
- **Journey:** Receives a reporting obligation → finds the correct form (routed
  by screener or assignment) → enters data across multiple sessions, potentially
  with collaborators → runs validation, resolves errors → obtains leadership
  sign-off or attestation → submits to the administering program office
- **Outcome:** The reporting obligation is fulfilled with minimal burden. Data
  enters the system in a validated, structured format. The grantee's time is
  spent on substance, not on fighting the tool.
- **Depends on:** Form definitions must exist and be assigned. Prior-year data
  must be pre-populated. Authentication and permissions must resolve the user's
  identity, organization, and role. Validation rules must execute in real time
  during data entry.

### 2. Federal Review

- **Who:** Federal program staff — Program Specialists, review leads, approvers
  across any program office
- **Journey:** A submission arrives → reviewer is notified → reviews the
  submission against policy requirements and data quality expectations → routes
  through the configured approval pipeline (sequential or parallel steps,
  conditional routing based on thresholds, delegation rules) → approves, requests
  revision with explanatory feedback, or rejects → closes the review cycle
- **Outcome:** Timely, consistent oversight with reduced manual effort. The
  review process is visible, trackable, and auditable — no more email chains and
  spreadsheets.
- **Depends on:** Submissions must exist in the system. Workflow routing rules
  must be configured. Reviewers must have appropriate permissions scoped to their
  program and grantee assignments.

### 3. Reporting & Analytics

- **Who:** Program analysts, agency leadership, Congressional reporting staff,
  public accountability audiences — across any program office using the platform
- **Journey:** Approved submission data becomes queryable → staff explores
  portfolio-level views (grantee status across programs, submission completion
  rates) → performs cross-grantee comparisons and year-over-year trend
  analysis → identifies outliers and patterns → packages findings for the
  appropriate audience (internal program improvement, Congressional reports,
  public data releases)
- **Outcome:** Collected data gets used — not just stored. The platform
  transforms raw submissions into actionable insight across multiple reporting
  contexts.
- **Depends on:** Submissions must have flowed through the full Grantee
  Submission → Federal Review cycle. Data must be queryable without degrading
  operational performance. Export formats must serve diverse consumers.

### 4. System Administration

- **Who:** Program office staff (form configuration), system administrators
  (user and org management), technical staff (operational health)
- **Journey:** Program staff defines a new reporting cycle → configures or
  updates form definitions → tests the form in a sandbox → publishes to
  production → assigns forms to recipient organizations → sets deadlines and
  notification rules → manages user access across organizational tiers → monitors
  system health and operational metrics
- **Outcome:** The platform operates without engineering intervention. New
  reporting cycles, form updates, and organizational changes are handled by
  program staff through administrative tooling.
- **Depends on:** Form schema convention must support non-technical authoring.
  User and permission management must be self-service at every organizational
  tier.

### 5. Data Integration

- **Who:** The platform itself (automated pipelines), agency technical staff
  (API consumers), external system operators, downstream data consumers
- **Journey:** External data flows in — grant management system records,
  authoritative entity validation (e.g., SAM.gov UEI), prior-year submission
  data → pre-populates form fields
  and validates against authoritative sources during data entry → collected and
  approved data flows out via APIs, CSV exports, PDF generation, and public
  access links → downstream consumers integrate the data into their own systems
  and processes
- **Outcome:** The platform is not an island. It connects to the broader grants
  ecosystem — importing context that reduces grantee burden on the way in, and
  exporting structured data that serves analysis, compliance, and interoperability
  on the way out.
- **Depends on:** Inbound integration must be operational before the Recipient
  Application can deliver its full value (pre-populated forms). Outbound
  integration requires data to exist in the system. Both halves depend on the
  form schema convention for mapping external data into and out of the platform's
  vocabulary.

### 6. Compliance & Audit

- **Who:** Office of Inspector General (OIG), OMB, legal counsel, FOIA officers,
  ISSO, agency records managers
- **Journey:** An oversight body needs to verify that data was collected
  lawfully, stored correctly, retained for the appropriate duration, and is
  reproducible on demand → queries audit trails for specific submissions, users,
  or time periods → reviews chain-of-custody metadata → verifies PRA clearance
  status for active forms (OMB control numbers, expiration dates, burden
  estimates) → produces compliance artifacts (FOIA responses, audit reports,
  ATO evidence packages)
- **Outcome:** The platform can prove it did the right thing, to anyone
  authorized to ask. Compliance is demonstrable, not aspirational — backed by
  immutable logs, retention policies, and reproducible records.
- **Depends on:** Every other deliverable must emit audit events. The form
  schema convention must include PRA metadata. Records retention policies must be
  defined and enforced. Field-level access controls must exist for data
  sensitivity tiers.

### 7. Grantee Support

- **Who:** Program office staff providing technical assistance, TTA (Training
  and Technical Assistance) providers, grant recipients who need help
- **Journey:** A grantee cannot complete a form, does not understand a rejection,
  cannot resolve a validation error, or cannot navigate the system → initiates a
  support interaction (in-app help, guided walkthrough, or escalation to OCS
  staff) → issue is diagnosed — is it a usability problem, a data problem, a
  permissions problem, or a policy question? → guided to resolution through
  contextual help, staff-assisted walkthrough, or direct intervention → issue
  resolved, grantee continues or completes submission
- **Outcome:** The platform works for its most constrained users, not just its
  most capable. Support interactions are tracked, patterns are identified, and
  systemic issues feed back into product improvement.
- **Depends on:** The Recipient Application must surface contextual help and
  explanatory validation messages. Support staff need a console with scoped
  access to grantee form state. Support interactions must be trackable for
  pattern analysis. This stream requires its own user research — understanding
  recipient technical capacity (which varies dramatically across organizational
  types and geographies), common failure modes, and the TTA provider landscape.

---

## Capability Domains

When you trace all seven value streams, six shared building blocks keep
appearing. No single stream owns them — they are the platform's structural
vocabulary.

| Domain                     | Definition                                                                                                    | Streams That Depend On It                                         |
| -------------------------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| **Form Platform**          | Schema-driven form definition, rendering, validation, calculated fields, conditional logic, versioning        | Grantee Submission, Federal Review, System Admin, Grantee Support |
| **Identity & Access**      | Multi-tier organizational identity, self-service user management, role-permission governance, authentication  | All seven streams                                                 |
| **Grantee Experience**     | Recipient-facing application layer — save/resume, collaboration, low-connectivity resilience, submit/revise   | Grantee Submission, Grantee Support                               |
| **Federal Workflow**       | Configurable multi-step review/approval pipelines, routing, delegation, status tracking                       | Federal Review, System Administration                             |
| **Portfolio Intelligence** | Aggregate querying, cross-grantee views, trend analysis, export packaging                                     | Reporting & Analytics, Compliance & Audit                         |
| **Data Exchange**          | Inbound pipelines (pre-population, external validation) and outbound interfaces (APIs, exports, public links) | Data Integration                                                  |

These domains organize into three tiers:

- **Foundation:** Form Platform and Identity & Access — every stream passes
  through one or both. These are load-bearing, not deferrable.
- **Application:** Grantee Experience and Federal Workflow — where users
  actually live. Built on top of the foundation, consumed by the value streams
  that serve grantees and federal staff.
- **Terminal:** Portfolio Intelligence and Data Exchange — they consume what the
  other domains produce. Last to deliver value, but high strategic importance.

---

## Product Deliverables

The capability domains describe what the platform needs to be able to do. The
product deliverables are the concrete things you build, ship, and put on a
roadmap — things a team owns, a stakeholder can see a demo of, and a roadmap
tracks.

### The Deliverable Map

| #   | Deliverable                      | Layer         | What It Is                                                                                                                                                                                                                                                                                                                                                      |
| --- | -------------------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Form Schema Convention**       | Specification | The shared grammar — field primitives, composition rules, validation semantics, versioning rules, data sensitivity classification. A time-boxed design activity that includes an explicit adopt-vs-build evaluation against existing specifications (XForms, JSON Forms, FHIR Questionnaire, etc.). Not code — a specification that everything else implements. |
| 2   | **Form Engine Backend**          | Core          | Implements the schema convention. Persistence layer for form definitions and submissions, APIs for form lifecycle operations, validation execution, versioning and submission history. The stable core that outlives any frontend.                                                                                                                              |
| 3   | **Workflow Rules Engine**        | Core          | Submission lifecycle state machine — routing rules, approval logic, delegation, escalation, conditional routing (e.g., budget threshold triggers additional review step). A core-layer concern: the frontends render workflow state, the backend owns the rules.                                                                                                |
| 4   | **System & User Administration** | Core          | Users, organizations, roles, permissions, authentication. Understands the schema convention's vocabulary for scoping permissions to specific forms, sections, and fields. Enforces field-level access control for data sensitivity tiers. Self-service at every organizational level.                                                                           |
| 5   | **Inbound Integration**          | Core-adjacent | Pre-population pipelines — grant management system records, authoritative entity validation (e.g., SAM.gov UEI), prior-year submission data. Maps external data into the platform's schema convention. Must be operational before the Recipient Application can show pre-populated forms. Designed to onboard new external sources as additional program offices adopt the platform.                                                                                               |
| 6   | **Recipient Application**        | Frontend      | Grantee-facing interface. Form rendering, save/resume, multi-person collaboration, low-connectivity resilience (IndexedDB/localStorage caching with sync-on-reconnect), real-time validation with explanatory messages, submit/revise lifecycle. Consumes the Form Engine Backend via APIs.                                                                     |
| 7   | **Form Administration**          | Frontend      | Build, test, publish, and version form definitions. PRA metadata management (OMB control numbers, expiration dates, burden estimates). Sandbox/testing environment for draft forms. Consumes the Form Engine Backend. This deliverable is what transforms the platform from a bespoke build into a reusable engine.                                             |
| 8   | **Internal Workflows UI**        | Frontend      | Federal review and approval interface. Renders the Workflow Rules Engine for human interaction — review queues, routing visualization, approval actions, revision requests with feedback. Consumes the Workflow Rules Engine and Form Engine Backend.                                                                                                           |
| 9   | **Support Tooling**              | Frontend      | Contextual help systems and guided walkthroughs within the Recipient Application. Staff-side support console for program office personnel assisting grantees — scoped access to grantee form state, ability to diagnose issues, support ticket integration. Pattern tracking for systemic issue identification.                                                            |
| 10  | **Reporting Platform**           | Terminal      | Portfolio dashboards, cross-grantee comparison views, year-over-year trend analysis, outlier detection, compliance and audit trail access, export packaging for Congressional and public reporting.                                                                                                                                                             |
| 11  | **Outbound Integration**         | Terminal      | APIs for external consumers, CSV and PDF export, public access links with field-level visibility controls. Serves data out of the platform to downstream systems and reporting contexts.                                                                                                                                                                        |

### Dependency Graph

```
           ┌─────────────────────┐
           │  Form Schema        │  ← specification
           │  Convention         │
           └────────┬────────────┘
                    │
   ┌────────────────┼────────────────┬──────────────┐
   ▼                ▼                ▼              ▼
 Form Engine      Workflow        System &       Inbound
 Backend          Rules           User Admin     Integration
 + Data           Engine
   │                │                │              │
   ├────────────────┼────────────────┼──────────────┤
   ▼                ▼                ▼              ▼
 Recipient       Internal         Form          Support
 App             Workflows UI     Admin         Tooling
   │                │                │              │
   └───────┬────────┘────────────────┘──────────────┘
           │
   ┌───────┴────────┐    ┌────────────────┐
   │   Reporting    │◄───│   Outbound     │
   │   Platform     │    │  Integration   │
   └────────────────┘    └────────────────┘
```

### Reading the Graph

**Form Schema Convention** is the keystone — everything implements or consumes
it. It is a specification, not a running service.

**Core layer** (Form Engine Backend, Workflow Rules Engine, System & User Admin,
Inbound Integration) can be built in parallel. These four deliverables are
independent of each other but collectively required before the frontend layer
can function. They are the stable foundation that outlives any particular
frontend.

**Frontend layer** (Recipient App, Internal Workflows UI, Form Admin, Support
Tooling) are consumers of the core layer. Each can be built, rebuilt, or
replaced independently. In theory, the core backend can remain stable while
entirely new frontends are developed for new programs, new user groups, or new
interaction models.

**Terminal layer** (Reporting Platform, Outbound Integration) need data flowing
through the system before they can deliver value. They are downstream consumers
of everything above them.

### Cross-Cutting Concerns

Two concerns span the entire deliverable map rather than living in any single
deliverable:

**Data sensitivity.** Federal grant programs handle data about vulnerable
populations — tribal nations, families in poverty, children, domestic violence
survivors. Data sensitivity varies by program and field. Field-level access
control must be
baked into the schema convention from day one and enforced by System & User
Administration. Every deliverable that touches submission data must respect
sensitivity tiers. This is a design constraint, not a feature to retrofit.

**Audit trail.** Every deliverable emits audit events — form creation, field
edits, permission changes, submission state transitions, review actions, export
operations. The Compliance & Audit value stream consumes these events through
the Reporting Platform and System & User Administration. Audit is not a
deliverable — it is an obligation that every deliverable fulfills.

---

## Value Streams Through Deliverables

Each value stream traces a path through multiple deliverables. These narratives
show how the streams and deliverables connect — where value flows, where
handoffs happen, and which deliverables are load-bearing for which streams.

### Grantee Submission

Begins in **System & User Administration** — authenticate the user, resolve
their organizational membership and role, determine what they have permission
to access. **Inbound Integration** has already seeded the **Form Engine
Backend** with prior-year data via pre-population pipelines. The **Recipient
Application** pulls the assigned form definition from the Backend, renders it
according to the **Form Schema Convention**, and the grantee works through it
across sessions — saving progress, collaborating with colleagues, running
validation in real time. When the form is complete and leadership has attested,
submission lands in the Backend, where it becomes visible to **Internal
Workflows UI** and the Federal Review stream begins.

### Federal Review

Starts where Grantee Submission ends. The **Workflow Rules Engine** picks up
the submission and applies the configured routing rules — who reviews first,
whether steps are sequential or parallel, whether budget thresholds trigger
additional review. **Internal Workflows UI** renders this for the reviewer:
submission data pulled from the **Form Engine Backend**, review actions (approve,
reject, request revision with feedback), routing status. Each action updates the
submission lifecycle state in the Backend and may trigger notifications. Revision
requests cycle back to the **Recipient Application** via the Grantee Submission
stream.

### Reporting & Analytics

Consumes submission data that has flowed through the full Grantee Submission →
Federal Review cycle. The **Reporting Platform** queries the **Form Engine
Backend** for aggregate views — portfolio-level grantee status, cross-grantee
comparisons, year-over-year trends, outlier detection. **Outbound Integration**
packages the data for export — CSV for analysts, PDF for formal reports, APIs
for downstream systems. This stream cannot produce value until upstream streams
are generating approved submission data.

### System Administration

Two deliverables are primary. **Form Administration** is where program staff
configure and manage form definitions — build new forms against the **Form
Schema Convention**, test them in a sandbox, publish versions, manage PRA
metadata. **System & User Administration** is where org hierarchy, user
accounts, roles, and permissions are managed across all tiers. Together, these
deliverables enable the platform to operate without engineering involvement —
new reporting cycles, form updates, and organizational changes are handled by
program staff.

### Data Integration

Split across the timeline. **Inbound Integration** runs early and
continuously — pulling grant management system data, authoritative entity
lookups, and prior-year submissions into the **Form Engine Backend**, mapping
external data into the
**Form Schema Convention's** vocabulary. **Outbound Integration** runs
late — APIs, CSV, PDF export, and public access links serve external consumers
after data exists in the system. The schema convention is the contract that
makes both halves coherent: external data maps into convention primitives on
the way in, and maps out of them on the way out.

### Compliance & Audit

Touches every deliverable indirectly — all emit audit events. Primarily lives
in **System & User Administration** (access logs, permission changes, user
provisioning history), the **Form Engine Backend** (submission history, version
chain-of-custody, field-level edit trails), and the **Reporting Platform**
(audit trail queries, retention enforcement, compliance artifact generation).
**Form Administration** manages PRA metadata that compliance officers need to
verify (OMB control numbers, expiration dates). The Compliance & Audit stream
does not have its own dedicated deliverable — it is a consumer of audit data
that every other deliverable produces. This is intentional: compliance is a
cross-cutting obligation, not a separate application.

### Grantee Support

Begins when Grantee Submission breaks down. **Support Tooling** provides the
staff-side console — program office staff can see the grantee's form state (scoped by
data sensitivity and permissions via **System & User Administration**), diagnose
whether the issue is usability, data, permissions, or policy, and guide the
grantee to resolution. On the grantee side, the **Recipient Application**
surfaces contextual help, explanatory validation messages, and guided
walkthroughs. The **Form Engine Backend** provides the form state and validation
context that both sides need. Support interactions are tracked for pattern
analysis — systemic issues feed into product improvement via the **Reporting
Platform**.

---

## Sequencing & Prioritization Implications

### Natural Build Order

The dependency graph defines a logical sequence that any implementation must
respect, regardless of methodology or team structure. This is not a project
plan — it is the order in which investment weight should shift.

| Phase               | Deliverables                                                                         | Rationale                                                                                                                                                                                                                                                                  |
| ------------------- | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **0 — Convention**  | Form Schema Convention                                                               | Everything else implements or consumes this grammar. Includes explicit adopt-vs-build evaluation against existing specifications. Time-boxed to 2-4 weeks — the goal is "right enough to start" with a defined process for evolution, not a complete formal specification. |
| **1 — Foundation**  | Form Engine Backend, Workflow Rules Engine, System & User Admin, Inbound Integration | The four core-layer deliverables. Can be built in parallel. Nothing above them functions without them. This is the heaviest investment phase.                                                                                                                              |
| **2 — Application** | Recipient App, Form Admin, Internal Workflows UI, Support Tooling                    | Four frontends consuming the foundation. Can be built in parallel, prioritized by value stream importance. Each is independently deployable and replaceable.                                                                                                               |
| **3 — Terminal**    | Reporting Platform, Outbound Integration                                             | Need data flowing through the system before they deliver value. Last to ship, but high stakeholder visibility — leadership cares most about this layer.                                                                                                                    |

This is not strictly waterfall. In practice, you build thin vertical slices
through all layers — a single form type rendered end-to-end touches the schema
convention, the backend, the recipient app, and possibly inbound integration in
one pass. But the investment weight shifts: Phase 1 dominates early, Phase 2
dominates mid-development, Phase 3 dominates late.

### Where the PWS and This Analysis Diverge

The Performance Work Statement (PWS Section 2.0) organizes requirements by
capability area — form fields, workflow, permissions, security. This is
standard for government procurement. But it creates blind spots when translated
into product strategy:

- **The schema convention is invisible.** The PWS does not distinguish the
  specification of what a form is from the implementation of the form engine.
  The specification is the most leveraged investment in the entire platform —
  get it wrong and every deliverable inherits the debt.

- **Form Administration is barely mentioned.** But it is the deliverable that
  transforms the platform from a bespoke build into a reusable engine. Without
  it, every new form requires engineering. With it, program staff can iterate
  independently.

- **Workflow rules are treated as a frontend concern.** The PWS puts routing
  and approval in the same sections as recipient-side collaboration. In
  practice, workflow rules are backend design decisions — the submission
  lifecycle state machine, routing logic, and approval conditions must be
  designed alongside the form engine, not deferred to the review UI.

- **Inbound Integration is treated as a form feature.** Pre-population appears
  as a bullet under "Form Field Types." In practice, it is a foundational
  service that must be operational before the Recipient Application can deliver
  its full value.

- **Grantee Support and Compliance & Audit are invisible.** The PWS contains
  no requirements for support tooling, contextual help, or the compliance
  lifecycle. Both are certainties in a federal system serving grant recipients
  with widely varying technical capacity.

- **Reporting is a single line.** "Real-time access to system data that does
  not hinder application performance." In practice, this is a full product with
  its own users, its own UX, and its own value proposition.

The PWS's "Top Problems to Solve" list actually maps well to this analysis —
the government's instincts about what matters are sound. The procurement
structure just does not reflect the product structure.

### The Monolith Question

Starting as a monolith is expected for a 6-person team. Eleven deliverables
does not mean 11 services, 11 repositories, or 11 deployment pipelines. It
means you think in 11 deliverables even when the code lives in one repo and
ships as one artifact.

The Form Schema Convention is a design document, not a microservice. The
Workflow Rules Engine is a module, not a separate deployment. But the
boundaries between them are real in the code — clean interfaces, clear
ownership of concerns, and minimal cross-boundary coupling.

This conceptual clarity is what preserves structural flexibility. When a new
program office onboards, when scale demands separation, when team topology
changes, or when a program needs a specialized frontend — the seams are already
there. Without them, the monolith
becomes a monolith in the pejorative sense: a system where everything depends
on everything, and changing one thing means understanding all of it.

### Team Operating Model

Eleven deliverables for a 6-person team requires a translation layer. The full
decomposition is a conceptual map, not an org chart.

At current team size, individuals wear multiple hats across deliverables. A
developer working on the Recipient Application also contributes to the Form
Engine Backend. A designer working on Form Administration also shapes Support
Tooling. This is normal and expected.

The decomposition becomes operationally relevant — separate backlogs, separate
ownership, dedicated teams — when the organization exceeds approximately 15-20
people or 3 stream-aligned teams. Until then, it serves as a thinking tool:

- **Architecture decisions** reference deliverable boundaries to keep concerns
  clean
- **Sprint planning** maps work to value streams to ensure coherent slices
- **Prioritization conversations** use the dependency graph to sequence
  investment
- **Stakeholder communication** uses the value streams to explain what the team
  is building and why

The map is not the territory. But a team without a map builds without
direction.

---

## Appendix: Value Stream × Deliverable Matrix

Which deliverables does each value stream touch? A quick reference for tracing
dependencies and identifying which streams are affected by changes to a given
deliverable.

|                           | Schema Conv. | Engine Backend | Workflow Rules | Sys & User Admin | Inbound Integ. | Recipient App | Form Admin | Workflows UI | Support Tooling | Reporting Platform | Outbound Integ. |
| ------------------------- | ------------ | -------------- | -------------- | ---------------- | -------------- | ------------- | ---------- | ------------ | --------------- | ------------------ | --------------- |
| **Grantee Submission**    |              | ●              |                | ●                | ●              | ●             |            |              |                 |                    |                 |
| **Federal Review**        |              | ●              | ●              | ●                |                |               |            | ●            |                 |                    |                 |
| **Reporting & Analytics** |              | ●              |                |                  |                |               |            |              |                 | ●                  | ●               |
| **System Administration** | ●            |                |                | ●                |                |               | ●          |              |                 |                    |                 |
| **Data Integration**      | ●            | ●              |                |                  | ●              |               |            |              |                 |                    | ●               |
| **Compliance & Audit**    |              | ●              |                | ●                |                |               | ●          |              |                 | ●                  |                 |
| **Grantee Support**       |              | ●              |                | ●                |                | ●             |            |              | ●               | ●                  |                 |

---

*This analysis is a greenfield decomposition from first principles. It is
independent of the current codebase, current team structure, or current
procurement framing. It describes a general-purpose, cross-program-office
forms platform — not a CSBG-specific application. CSBG tribal forms are the
initial instantiation; the architecture, value streams, and deliverables are
designed to serve any ACF program office that needs to collect, review, and
report on grant recipient data. It serves as an evaluative lens — a reference
for assessing what exists, prioritizing what to build next, and communicating
the full scope of what CSFEER/CORE is to both the team and stakeholders.*

*Sources: PRD_CSFEER.md, PWS Section 2.0, UNDERSTANDING.md, product
analysis sessions.*
