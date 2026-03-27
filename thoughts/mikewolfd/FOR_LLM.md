# thoughts/mikewolfd — Structured Document Map

> **Purpose:** Machine-readable guide for LLM sessions working on the CSFEER project.
> Provides file-level summaries, semantic tags, cross-references, and a reading-order guide
> so any session can quickly locate the right context without reading all 70 documents.
>
> **Last updated:** 2026-02-24

---

## How to Use This Map

1. **Starting a new session?** Read the "Tier 1" documents first (5 files, ~2,500 lines total). They synthesize everything else.
2. **Need specific context?** Use the semantic tags and cross-reference columns to find the right file.
3. **Navigating `docs/`?** The `summarized/` versions are AI-condensed (~40-60% shorter). Read those first; fall back to `files/` for exact quotes or when summaries feel incomplete.
4. **The `confluence-export/` tree mirrors the Confluence wiki structure.** `INFO_MAP.md` is the master index — read it instead of navigating the tree manually.

---

## Reading Order by Purpose

| Purpose | Read These (in order) |
|---|---|
| **Understand the project** | `research/UNDERSTANDING.md` → `research/PRODUCT_WORKSTREAMS.md` |
| **Understand the codebase** | `research/csfeer-architectural-review.md` |
| **Understand requirements** | `research/PRD_CSFEER.md` → `research/UNDERSTANDING.md` (requirements tables) |
| **Understand stakeholders & timeline** | `docs/summarized/confluence-export/INFO_MAP.md` (sections 2-7) |
| **Understand proposed form engine evolution** | `research/analysis/form-schema-landscape.md` → individual analyses as needed (parallel research stream — not current state) |
| **Understand source documents** | `docs/summarized/` versions first, `docs/files/` for exact wording |

---

## Tiered Reading Guide

### Tier 1 — Essential Context (read first)

These five documents synthesize all other sources. A session that reads only these has ~90% of the context needed for any CSFEER task.

| File | Lines | Role |
|---|---|---|
| `research/UNDERSTANDING.md` | ~430 | **Master synthesis.** Project mission, users, MVP scope, capabilities, constraints, architecture, phased rollout, requirements traceability (40+ requirement IDs), open questions. Derived from all source documents. |
| `research/PRODUCT_WORKSTREAMS.md` | ~265 | **8 workstreams with dependency graph.** Prioritized capabilities (P0-P5) organized by the core question each answers. Identifies stress points and design tensions. |
| `research/csfeer-architectural-review.md` | ~460 | **Codebase deep-dive.** Honest assessment of every layer: Django structure, form engine, frontend, auth, API, infra, testing. Lists bugs, architecture concerns, and deployment blockers. |
| `research/PRD_CSFEER.md` | ~430 | **Formal PRD.** Structured requirements document with IDs (FE-01 through PS-06). Clean for cross-referencing. Derived from PWS. |
| `docs/summarized/confluence-export/INFO_MAP.md` | ~385 | **Confluence intelligence map.** Stakeholder directory with names/roles/concerns, timeline with dates, unresolved contradictions between documents, file-by-file index. |

### Tier 2 — Parallel Research Stream (proposed new approach)

> **Important:** These documents are a **separate research track** exploring how to evolve
> the form engine architecture beyond its current Pydantic+Django implementation.
> They evaluate external standards/tools and propose a new layered architecture
> (Layer 1: Field Definitions, Layer 2: Validation Rules, Layer 3: Layout, Layer 4: Renderers).
> This is **aspirational/proposed work** — not documentation of the current codebase.
> For current codebase architecture, see `research/csfeer-architectural-review.md` (Tier 1).

Each analysis has a clear "Adopt / Don't Adopt" recommendation section.

| File | Lines | Evaluates | Key Concepts to Borrow |
|---|---|---|---|
| `research/analysis/form-schema-landscape.md` | ~405 | 8 tools/standards compared | **Anchor doc for the research stream.** Comparison matrix across all tools. Proposes Pydantic + borrowed concepts: FieldBind, ExpressionEngine, ValidationResult (~900 lines of Python). |
| `research/analysis/fhir-r5-analysis.md` | ~630 | FHIR R5 Questionnaire + SDC | **Versioning model** (canonical URL + semver + derivedFrom + response pinning). enableWhen conditional pattern. disabledDisplay (hidden vs protected). |
| `research/analysis/jsonforms-analysis.md` | ~540 | JSON Forms (EclipseSource) | **Rule system** (SHOW/HIDE/ENABLE/DISABLE effects). Renderer registry with priority-ranked testers. Validation modes (validate_and_show / validate_and_hide / no_validation). |
| `research/analysis/shacl-analysis.md` | ~435 | W3C SHACL constraint language | **Three-level severity** (Violation/Warning/Info → error/warning/info). Structured ValidationResult pattern. Constraint composition (and/or/not/xone). |
| `research/analysis/simpler-grants-analysis.md` | ~345 | CommonGrants protocol + Simpler.Grants.Gov | **MappingSchema DSL** (field/switch/const for data transformation). DecimalString type. Cross-form pre-population pattern. |

### Tier 3 — Source Documents (read for exact requirements or stakeholder quotes)

#### `docs/summarized/` — AI-condensed versions (read these first)

| File | Role | Original Source |
|---|---|---|
| `Q1 2026 - Forms Engine.md` | Q1 development plan: epics, story points, milestones | `docs/files/Q1 2026 - Forms Engine.md` |
| `Specific Requirements and Tasks.md` | PWS Section 2.0: contractual requirements | `docs/files/Specific Requirements and Tasks.md` |
| `ITB - CSFEER.md` | First IPT kickoff meeting summary | `docs/files/2026-01-13 - ITB - CSFEER.md` |
| `ACF Forms Engine - User Personas.md` | 5 user personas with workflows | `docs/files/ACF Forms Engine - User Personas.md` |
| `Product Specification - MVP for CSFEER_CORE.md` | Client's MVP spec: objectives, requirements, metrics | `docs/files/Product Specification_ MVP for CSFEER_CORE.md` |
| `ACF Project Brief.md` | High-level project brief | `docs/files/ACF Project Brief.md` |
| `ACF CSFEER Intro Client Meeting.md` | Initial client meeting notes | `docs/files/ACF CSFEER Intro Client Meeting.md` |
| `PMP V2.md` | Project Management Plan v2 | `docs/files/PMP V2.md` |
| `PRODUCT SPEC — CORE (CSFEER) Tribal MVP.md` | Detailed tribal MVP product spec | `docs/files/PRODUCT SPEC — CORE (CSFEER) Tribal MVP.md` |

#### `docs/summarized/confluence-export/` — Confluence analysis artifacts

| File | Role |
|---|---|
| `INFO_MAP.md` | **Master index** for all Confluence content (included in Tier 1) |
| `analysis_plan.md` | Agent analysis methodology for the Confluence export |
| `recovered_agent_results.md` | Raw agent analysis results from Confluence processing |

#### `docs/files/` — Original source documents (unmodified)

| File | Type | Key Content |
|---|---|---|
| `Q1 2026 - Forms Engine.md` | Planning | Epic breakdown, story points, sprint allocation |
| `Specific Requirements and Tasks.md` | Contract | PWS Section 2.0 verbatim requirements |
| `Product Specification_ MVP for CSFEER_CORE.md` | Product | Client's MVP feature list and acceptance criteria |
| `ACF Forms Engine - User Personas.md` | Research | Tribal Grant Director, Program Coordinator, Data Entry Specialist, OCS Program Specialist, System Admin |
| `B09 SA 0001 - PWS ADMIN_OCS_CSBG_CSFEER_v2.md` | Contract | Full Performance Work Statement (Rev 2, Aug 2025) |
| `ACF Project Brief.md` | Product | Executive-level project overview |
| `2026-01-13 - ITB - CSFEER.md` | Meeting | First IPT meeting: NGSC, ATO, auth decisions |
| `ACF CSFEER Intro Client Meeting.md` | Meeting | Initial stakeholder introductions |
| `PMP V2.md` | Operations | Project Management Plan: team, timeline, risks |
| `PRODUCT SPEC — CORE (CSFEER) Tribal MVP.md` | Product | Detailed MVP spec with metrics and constraints |

#### `docs/files/confluence-export/` — Confluence wiki pages (deep reference)

Navigate via `INFO_MAP.md` Section 8 (File Index) rather than browsing this tree directly.

**Engineering & Architecture:**
| File | Key Content |
|---|---|
| `Engineering.md` | Navigation index (empty) |
| `CSFEER Tech Stack.md` | Full technology inventory with versions |
| `Tech Specs/Okta Authentication DRAFT.md` | OIDC auth spec: Okta config, role mapping, 6 open questions |
| `Tech Specs/Form Manager Application (WIP).md` | Core form engine architecture: Pydantic schemas, data models, review-page validation |
| `Tech Specs/Tech Spec Template.md` | 15-section template for new tech specs |
| `Technical Architecture & Security Framework.md` | Architecture diagrams: app flows + AWS topology |

**Product & Design:**
| File | Key Content |
|---|---|
| `Product_ Forms Engine (Focus Contract).md` | Team directory: 6 Focus + 25+ ACF personnel |
| `Initial Product Spec - MVP.md` | DRAFT: 20 functional requirements, 6 NFRs, 20+ tribal user target |
| `Design & Research.md` | Figma artifact index: ecosystem map, service blueprint, prototypes |
| `Design & Research/User Research Plan.md` | Dual-track research: 5+8 tribal usability tests + OCS staff interviews |

**Discovery & Domain:**
| File | Key Content |
|---|---|
| `CSBG Data Files.md` | FY24 OLDC exports (State Plan, Modules 1/2/4). Module 3 absent. |
| `Forms Engine Onboarding Documents.md` | Project history: vendor eval, shadow systems, cross-program interest |
| `Forms Engine Discovery/CSBG Annual Report.md` | GrantSolutions parallel dev ($1.2M-$1.71M CHMT-3186), tribal user counts |
| `Forms Engine Discovery/CSBG Reporting Process.md` | Policy: 4-module structure, $50K threshold, OLDC/SmartForms procedures |
| `Forms Engine Discovery/OCS and CSBG Overview.md` | RFI (largest file): OCS mission, CSBG structure, ACF-wide forms inventory |

**Meetings (IPT / Stakeholder):**
| File | Key Content |
|---|---|
| `Forms Engine IPT Meetings/2026-01-13*.md` | NGSC confirmed, ATO inheritance, Login.gov via Okta |
| `Forms Engine IPT Meetings/2026-01-27*.md` | ATO front-loading, Appendix X flagged, beta May-June |
| `Forms Engine IPT Meetings/2026-02-03*.md` | Shutdown impact, ECS confirmed, PIV received |
| `Forms Engine IPT Meetings/2026-02-10*.md` | GitLab setup, non-gov auth risk, PIA classification |
| `Onboarding.../Meeting Notes/2024-06*.md` | Origin: 1000+ data points, 700+ hours labor, SmartForms pain |
| `Onboarding.../Meeting Notes/2025-09-17*.md` | Internal planning: contract scope, state resistance risk |
| `Onboarding.../Meeting Notes/2025-09-25*.md` | CSBG staff intro, regional portfolios, state dynamics |
| `Onboarding.../Meeting Notes/2025-09-29*.md` | Focus team intro, success criteria, Jira decision |
| `Onboarding.../Meeting Notes/2025-11-20*.md` | Melanie as contract lead, Monique as OLDC BI lead |
| `Onboarding.../Meeting Notes/2025-11-26*.md` | ANA/CB cross-ACF: offline needs, 238-page form packages |
| `Onboarding.../Meeting Notes/2025-12-05*.md` | Demo 1: service blueprint, JSON schema, conditional fields |
| `Onboarding.../Meeting Notes/2026-02-13.md` | Sprint 6 demo to federal leadership |

**Security & Compliance:**
| File | Key Content |
|---|---|
| `CSFEER_ ATO Documentation & Compliance Hub.md` | 9 ATO artifacts tracked, May 29 target, status per artifact |
| `Risk Management.md` | Shutdown continuity contacts, ISSO/SCA/Login.gov roles |

**Contract & Operations:**
| File | Key Content |
|---|---|
| `Contract Status Template/*.md` | Monthly CSRs: financials, staffing, risk logs, sprint tracking |

### Plans

| File | Role |
|---|---|
| `plans/form-standard-proposal-prompt.md` | Research prompt for designing a JSON-native form definition standard. Synthesizes requirements from XForms, SHACL, FHIR R5. Specifies 30+ requirements (FT/FL/VR/VS/VE/VX/VC/AD prefixed) and 6 hard-case examples. |

---

## Semantic Tag Index

Use these tags to find documents relevant to a specific concern.

| Tag | Files |
|---|---|
| `#requirements` | `research/PRD_CSFEER.md`, `research/UNDERSTANDING.md`, `docs/summarized/Specific Requirements and Tasks.md`, `docs/summarized/Product Specification - MVP for CSFEER_CORE.md` |
| `#architecture` | `research/csfeer-architectural-review.md`, `confluence-export/.../Form Manager Application (WIP).md`, `confluence-export/.../Technical Architecture & Security Framework.md`, `confluence-export/.../CSFEER Tech Stack.md` |
| `#form-engine` | `research/analysis/form-schema-landscape.md`, `research/analysis/jsonforms-analysis.md`, `research/analysis/fhir-r5-analysis.md`, `research/analysis/shacl-analysis.md`, `research/analysis/simpler-grants-analysis.md`, `plans/form-standard-proposal-prompt.md` (**note:** these are a parallel research stream proposing a new approach, not current-state docs) |
| `#validation` | `research/analysis/shacl-analysis.md` (proposed severity model), `research/analysis/jsonforms-analysis.md` (proposed validation modes), `research/analysis/form-schema-landscape.md` (proposed comparison matrix) |
| `#versioning` | `research/analysis/fhir-r5-analysis.md` (canonical URL + semver + derivedFrom) |
| `#mapping` | `research/analysis/simpler-grants-analysis.md` (MappingSchema DSL) |
| `#auth` | `confluence-export/.../Okta Authentication DRAFT.md`, `research/csfeer-architectural-review.md` (Section 4), `docs/summarized/confluence-export/INFO_MAP.md` (Section 6: auth ambiguity) |
| `#security` | `confluence-export/.../CSFEER_ ATO Documentation & Compliance Hub.md`, `confluence-export/.../Risk Management.md`, `research/csfeer-architectural-review.md` (Sections 5-6) |
| `#users` | `docs/summarized/ACF Forms Engine - User Personas.md`, `research/UNDERSTANDING.md` (Users & Scale section) |
| `#stakeholders` | `docs/summarized/confluence-export/INFO_MAP.md` (Section 3: Stakeholder Map) |
| `#timeline` | `docs/summarized/confluence-export/INFO_MAP.md` (Section 7), `research/UNDERSTANDING.md` (Q1 sequence + milestones) |
| `#risks` | `docs/summarized/confluence-export/INFO_MAP.md` (Section 5), `research/csfeer-architectural-review.md` (Things That Need Attention) |
| `#contradictions` | `docs/summarized/confluence-export/INFO_MAP.md` (Section 6: Unresolved Questions) |
| `#workstreams` | `research/PRODUCT_WORKSTREAMS.md` |
| `#discovery` | `confluence-export/.../CSBG Annual Report.md`, `confluence-export/.../CSBG Reporting Process.md`, `confluence-export/.../OCS and CSBG Overview.md` |
| `#meetings` | All files under `confluence-export/.../Forms Engine IPT Meetings/` and `confluence-export/.../Meeting Notes/` |
| `#contract` | `docs/files/B09 SA 0001 - PWS ADMIN_OCS_CSBG_CSFEER_v2.md`, `confluence-export/.../Contract Status Template/*.md` |
| `#planning` | `docs/summarized/Q1 2026 - Forms Engine.md`, `docs/summarized/PMP V2.md` |

---

## Cross-Reference Matrix

Documents that inform or depend on each other.

| Document | Informs | Informed By |
|---|---|---|
| `UNDERSTANDING.md` | All implementation work | All source docs, PRD, INFO_MAP |
| `PRODUCT_WORKSTREAMS.md` | Sprint planning, architecture decisions | UNDERSTANDING.md, INFO_MAP |
| `PRD_CSFEER.md` | UNDERSTANDING.md, implementation | PWS (B09 SA 0001) |
| `csfeer-architectural-review.md` | Bug fixes, infra work, deployment | Codebase itself |
| `INFO_MAP.md` | UNDERSTANDING.md, stakeholder comms | All Confluence files |
| `form-schema-landscape.md` | Anchor for proposed form engine evolution | All 4 sibling analysis docs feed into it (parallel research stream) |
| `fhir-r5-analysis.md` | Proposed versioning design | FHIR R5 spec (parallel research stream) |
| `jsonforms-analysis.md` | Proposed rule system, validation modes | JSON Forms docs (parallel research stream) |
| `shacl-analysis.md` | Proposed validation severity model | SHACL spec (parallel research stream) |
| `simpler-grants-analysis.md` | Proposed data mapping, pre-population | CommonGrants protocol (parallel research stream) |
| `form-standard-proposal-prompt.md` | Future form standard design | All analysis docs (parallel research stream) |

---

## Document Freshness

| Category | Last Updated | Staleness Risk |
|---|---|---|
| `research/` | Feb 2026 | Low — synthesized from multiple sources, internally consistent |
| `research/analysis/` | Feb 2026 | Low — based on stable standards (FHIR R5, SHACL, JSON Forms) |
| `docs/summarized/` | Feb 2026 | Low — summaries of stable source docs |
| `docs/files/` | Jan-Feb 2026 | Medium — some represent point-in-time snapshots (meeting notes) |
| `confluence-export/` | Feb 2026 | Medium — wiki may have newer content not yet exported |
| `plans/` | Feb 2026 | Low — prompt document, not time-sensitive |

---

## Known Gaps

These topics are referenced in the research but have no dedicated document:

| Gap | Mentioned In | Status |
|---|---|---|
| OLDC field-level data mapping | `UNDERSTANDING.md` open question #12 | Partially answered — FY24 export prefix conventions known, field mapping not |
| Federal review workflow details | `UNDERSTANDING.md` open question #2 | Partially answered — key personnel known, step-by-step flow not documented |
| Specific validation rules per form | `UNDERSTANDING.md` open question #1 | Open — rules live in SmartForms XSD, not in any project document |

**Note on internal references:** The analysis docs reference `form-engine-roadmap.md` and `FRAMEWORK_REQUIREMENTS.md` as companion documents. These are alternate names / earlier drafts for `form-schema-landscape.md` and inline requirements within that same analysis stream.
