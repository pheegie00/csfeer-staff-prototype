# UNDERSTANDING.md — CSFEER Project Context

> Project narrative and context.
> For requirements, see [MATRIX.md](MATRIX.md) (authoritative).
> For conflicts, risks, decisions, and questions, see [open-items.md](open-items.md).
> For value stream architecture, see [VALUE_STREAM_ANALYSIS.md](VALUE_STREAM_ANALYSIS.md).
> Last updated: 2026-03-05

---

## Mission

- Replace legacy PDF-based data collection for ACF grant programs with a scalable, user-centered digital forms platform
- Streamline the full grants reporting lifecycle: pre-award planning → post-award reporting → Congressional performance analysis
- Long-term vision: become the **single reporting platform for all ACF grant programs** (25,000+ recipients, 100+ forms, hundreds of federal staff)
- Working name: Community Outcomes Reporting Engine (CORE) — the platform; CSFEER — this initial engagement
- Product owner: Office of Community Services (OCS), Administration for Children and Families (ACF)
- **Legacy baseline:** Current system dates to **2015**; validation of submitted data currently takes **9–12 months** of manual effort per cycle — the primary pain point to compress
- **Requirements are non-exhaustive and mutable** — agile discovery and user research drive changes; Government is Product Owner

### Current State (As-Is)

OCS administers ~$6.29B annually across 7 programs serving 36.8M Americans in poverty. Grant recipients are required by law to submit extensive pre-award and post-award forms. Today:

- Forms are **fillable PDFs** exchanged manually, requiring substantial out-of-system preparation
- Data validation happens **after submission**, not during entry
- Historical comparisons require **manual cross-referencing** between submissions
- Federal staff cannot easily **export, query, or analyze** collected data at scale
- States and tribes sometimes use **custom or third-party reporting tools**, creating compatibility issues and data variability
- There is **no collaborative workflow** — multiple people cannot work on a single form submission, and routing/approval is manual

### Government's Prioritized Problems (ranked)

1. Faster form design iteration — program staff can design, update, and test forms without engineering
2. Intuitive recipient UX — replace PDF-era friction
3. Submission tracking & collaboration — visibility across program staff, lead agencies, and subrecipients
4. Real-time validation — business-logic-driven errors and warnings during data entry
5. Integration validation — automated comparison to external data (e.g., UEI mismatches from SAM.gov)
6. Error correction workflow — staff can export, review, and fix data issues
7. Reduce variability — standardize away from custom state/tribal plan formats and third-party tools
8. Real-time data access — analytics/reporting without degrading app performance

## Users & Scale

- **Grant recipients (~1,100 at scale):** Tribal recipients (~66), State/territory lead agencies (~53), eligible entities (~1,000+), sub-recipients (varies)
- **Federal staff (~75):** OCS program staff who review, approve, analyze, and report on submitted data; a single Program Specialist manages **15–25 tribal grantees** across multiple time zones
- **Future (Year 2+):** Non-technical program staff who build/manage forms via low-code/no-code tools
- **Future scale targets (named):** LIHEAP, Diaper Program, Rural Development — beyond generic "all ACF programs"
- **Connectivity reality:** Rural tribal users have spotty broadband; shared devices are common — UX must be resilient

> For role-permission matrix and grantee access tiers, see [MATRIX.md §6](MATRIX.md#6-permissions--user-management-pm).

## Data Model

- **CSBG has two reporting tracks** with different form structures
- **Tribal track (Phase I):** Tribes/tribal orgs receive funding directly from OCS → submit Tribal Plan (pre-award) + Tribal Annual Report or Short Form (post-award, contains Modules 1–3)
- **State/Territory track (Phase II):** States receive funding → distribute to eligible entities → State submits Plan + Entity List + Module 1; eligible entities submit Modules 2–4
- **Reporting cycle:** Annual grant cycle; plan applications annual or biannual; annual reports once per year; federal staff review/analyze → report to Congress

## How Federal Staff Actually Work Today

This narrative context matters for design decisions.

**Melanie Durley** handles PRA approval for ~half the forms and manages all Congressional reporting. **Monique Alcantara** handles the other half as OLDC BI/testing lead and is COR for the Performance Management website. Review process today is entirely manual via email and spreadsheets.

**Validation as workflow cue:** Contributors use validation errors to guide data entry — inline messages must be explanatory (e.g., "Total of Sections A-C must equal your CSBG award amount") and clearly distinguish hard errors vs warnings. This shapes how the validation engine surfaces feedback.

**Federal review is substantially complex.** Open design questions remain: sequential vs parallel steps, conditional routing (e.g., budget threshold triggers CFO step), unanimous vs any-one-approves, who configures workflows, delegation/override rules, reviewer permission tiers (view-only / comment / final approve). See conflict C-7 below.

**Portfolio tracking doesn't exist.** Current OLDC has no portfolio view — all tracking is via email and spreadsheets. Federal staff need per-grantee status (Not Started / In Progress / Submitted / Needs Correction) across all forms.

**Batch review pattern:** Federal staff review submissions in batches, export to CSV/Excel for comparison, identify outliers (major year-over-year changes). This is a distinct workflow from individual submission review.

---

## Conflicts, Risks, Open Questions

> **Moved.** All conflicts (C-1–C-13), risks (R-01–R-16), open decisions (D-01–D-08), and open questions (Q-01–Q-12) are now in [open-items.md](open-items.md).
>
> Key numbers: 5 MVP-blocking conflicts, 16 risks (2 new from arch review), 8 open decisions, 12 open questions. 4 conflicts effectively resolved by implementation or deferral.

---

## Legacy Systems & Data Sources

| System | Detail | Source |
|--------|--------|--------|
| OLDC | Operational since ~2015; couldn't afford sub-recipient level collection at launch; validation cycles take 9–12 months of manual effort | [S01]; [S34] |
| GrantSolutions | Broader ACF forms platform; expensive, not user-friendly; parallel $1.2M–$1.71M modernization (CHMT-3186) — see C-11 | [S23]; [S13] |
| SmartForms | External tools for sub-recipients; XML/XSD validation; macro-blocking issues; UEI failures; NASCSP distributes specs to vendors | [S01]; [S13] |
| COPOS | Pennsylvania state system integrated with local systems | [S03] |
| CSG (Community Software Group) | State-level third-party software | [S26] |
| Performance Management website | Downstream consumer of exports (csbgpm.acf.gov); Monique Alcantara is COR | [S05]; [S23] |
| NASCSP vendor portal | Distribution channel for tech specs to state vendors | [S13]; [S26] |
| Qualtrics | Only ATO'd digitization option currently; "painful to use," poor JS support | [S06] |

**FY24 data exports:** Available for State Plan, Modules 1/2/4 (Module 3 absent); RVW/RPT prefix naming convention. Field-level mapping between OLDC columns and CSFEER schema fields is unknown.

### Cross-Program Expansion Interest

Not part of MVP requirements. Captured from Confluence for long-term planning.

| Program/Office | Interest Level | Key Detail | Source |
|----------------|---------------|------------|--------|
| ANA (Administration for Native Americans) | Active | Offline/in-person administration needed; Alaska connectivity issues | [S06] |
| CB (Children's Bureau) | Active | Title IV-E Foster Care Review — 26-page form + 62-page instructions + 150-page guide | [S06] |
| LIHEAP | Named next target | Next expansion after CSBG success | [S05]; [S02]; [S34] |
| Diaper Program | Named by OCS | Near-term scale target beyond CSBG | [S34] |
| Rural Development | Named by OCS | Near-term scale target beyond CSBG | [S34] |
| Community Needs Assessment | Broad applicability | Cross-program candidate for early expansion | [S06] |
| 64 ACF forms across 8 offices + 4 cross-office | Long-term vision | ANA: 3, CB: 18, OCC: 5, OCS: 14, OCSS: 7, OFA: 5, OFVPS: 2, ORR: 2, ACF-Wide: 4 | [S26] |

---

## Legacy Burden Baseline

Current 12–20 days per form submission:

1. 1–3 days locating forms/guidance
2. 5–10 days internal data gathering
3. 3–5 days offline drafting
4. 2–5 days leadership review/signatures
5. 1–2 days OLDC upload/formatting
6. 1–5 days corrections/resubmissions

Estimated **1,800 hours total annual burden** across Tribal organizations. Target: reduce to 3–7 days (aspirational: <1 hour).

## 90-Day Baseline Telemetry Plan

First 90 days post-launch: establish measurement baselines across four dimensions:

1. **User interaction:** sessions per submission, time per section, autosave frequency/success, sync patterns
2. **Submission quality:** validation error types/frequency, resolution rates, submit-unsubmit cycles
3. **Performance:** load times, save/sync times, export performance
4. **Operational:** ticket volume, time-to-resolution, OCS review time

Requires instrumentation from day one — event tracking for autosave, section timing, validation error categorization, connectivity state transitions.

## Tribal Engagement Plan

- **Tribal Advisory Group:** 6–8 representatives, geographically diverse, formed Months 1–6
- **Site visits:** 8–10 planned during discovery
- **Pilot cohort:** 10–12 orgs with weekly check-ins tapering to bi-weekly
- **Rollout:** Wave-based with parallel operations (old PDF + new system simultaneously)

## USWDS Component Inventory

15 components in three tiers:

1. **Core form:** text inputs, textareas, selects, checkboxes, radio buttons
2. **Layout/navigation:** headers, footers, navigation, breadcrumbs, progress indicators
3. **Advanced form:** file upload, date picker, address validation, calculation fields, repeatable sections

## Key Assumptions

- The initial MVP focuses on CSBG Tribal forms but the architecture **must not be CSBG-specific** — form engine, schema, and multi-program architecture stay generic from day one
- Grant recipients currently invest significant time preparing submissions outside the system — reducing this overhead is a primary value driver
- Forms change over time; the platform must handle **form version evolution without breaking existing submissions**
- The annual reporting cycle means there are natural deadlines that drive user behavior and **system load patterns** (peak at Tribal Plan due dates and March 31 Annual Report deadline)
- Federal staff needs extend beyond data collection into **analysis, comparison, and Congressional reporting**

---

## Research Next Steps

- [ ] Validate MVP scope boundaries with product owner input (resolves C-1, C-3, C-5, C-7, C-13 — see [open-items.md](open-items.md))
- [ ] Capture PRA approval dependency and PII-in-upstream approval as blockers
- [ ] Re-source internally-sourced NFRs (PR-01, PR-03, PR-11–14) — check if PWS or contract mods contain equivalent performance language

---

*This document provides project context and narrative. Authoritative requirements: [MATRIX.md](MATRIX.md). Open items: [open-items.md](open-items.md). Value stream architecture: [VALUE_STREAM_ANALYSIS.md](VALUE_STREAM_ANALYSIS.md).*
