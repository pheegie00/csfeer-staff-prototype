# WS-xx Lineage Analysis

> **Purpose:** Trace all 24 workstream-identified items from WORKSTREAMS back to source-of-truth documents in `docs/files/`. Determines which items should be promoted into MATRIX.md and which remain supplementary.
>
> **Source constraint:** Only `docs/files/` counts as source of truth. AI-generated summaries in `docs/summarized/` and `recovered_agent_results.md` are not authoritative.
>
> **Date:** 2026-03-03

---

## Category 1: Remapped to MATRIX IDs (7 items — already fixed in V3)

These were V2 items that had direct MATRIX counterparts I missed during V3 drafting. Fixed in V3.

| V3 ID | V2 ID | MATRIX Match | Action Taken |
|-------|-------|-------------|-------------|
| ~~WS-04~~ | SCH-19 | **FE-40** (low-code/no-code builder) | Deleted from V3 — already present as FE-40 in workstream 7 |
| ~~WS-06~~ | ENG-15 | **FE-32** (historical comparison "comparatively") | Deleted from V3 — already present as FE-32 in workstream 2 |
| WS-10 | APP-16 | **WF-15** (UI surface of multi-user workflow) | Remapped in V3 — shows as WF-15 with "(app-layer UI)" note |
| WS-14 | REV-02 | **WF-09** (review actions are verbs of multi-step review) | Remapped in V3 — shows as WF-09 with "(UI surface)" note |
| WS-15 | REV-03 | **UP-03** (transmittal letter/attestation, federal side) | Remapped in V3 — shows as UP-03 with "(federal side)" note |
| ~~WS-22~~ | RPT-06 | **UP-04** (portfolio dashboard) + **UP-05** (cross-grantee comparison) | Deleted from V3 — already present as UP-04/UP-05 in workstream 8 |
| ~~WS-23~~ | RPT-07 | **UP-05** (explicitly mentions "outlier identification") | Deleted from V3 — already present as UP-05 in workstream 8 |

---

## Category 2: Verified Against Source Docs

### Items with strong source lineage — candidates for MATRIX promotion

#### WS-24 (Conditional-logic-aware PDF) → PROMOTE to MATRIX as DA-15

- **V2 ID:** OUT-03 | **V2 Provenance:** Discovery
- **Source doc:** `docs/files/confluence-export/.../2025-09-25 Kickoff with CSBG Staff.md` line 29
- **Direct quote:** "business logic built in, but when they print it, it show everything (even questions that weren't applicable) - hard to read"
- **Source ID:** [S03]
- **MATRIX section:** §4 Integration & Data (System Requirements — S03 is an allowed source)
- **Proposed MATRIX entry:**

```
| DA-15 | Conditional-logic-aware PDF/print export: omit non-applicable sections from output | ? | [S03] — user pain point; no priority language in source |
```

#### WS-05 (Auto-save conflict handling) → PROMOTE to MATRIX as FE-47

- **V2 ID:** ENG-12 | **V2 Provenance:** PWS+
- **Source doc:** `docs/files/confluence-export/.../Tech Spec_ Form Manager Application (WIP).md` line 73
- **Direct quote:** "Simultaneous multi-user editing" (listed as known concern / future consideration)
- **Source ID:** [S21]
- **MATRIX section:** §1 Form Engine — Project Context > Implementation Decisions (extends FE-38)
- **Note:** The specific "conflict handling" wording only appears in the AI-summarized Q1 plan, not in the source doc. The source doc lists the concern but doesn't prescribe a solution.
- **Proposed MATRIX entry:**

```
| FE-47 | Concurrent edit conflict handling for periodic auto-save (extends FE-38) | ? | [S21] — "Simultaneous multi-user editing" listed as known concern |
```

#### WS-18 (Contextual help / field guidance) → PROMOTE to MATRIX as AD-13

- **V2 ID:** SUP-01 | **V2 Provenance:** PWS+
- **Source docs:**
  - `docs/files/ACF Forms Engine - User Personas.md` line 53: 'In-context guidance ("What you enter here should match your SF-424M in OLDC")'
  - `docs/files/confluence-export/.../2025-11-26 Forms Engine __ Forms Digitization.md` line 15: "Form itself does not include the substantial context that comes with very lengthy instruction and guide documents"
- **Source IDs:** [S32], [S06]
- **MATRIX section:** §5 Accessibility & Design — **System Requirements** ([S06] is a client source; [S32] is supporting internal source)
- **Note:** UP-02 in MATRIX already captures SF-424M cross-referencing specifically. This is the broader concept: field-level help, section-level instructions, and integration of companion documents (some forms have 62–150 page instruction docs per [S06]).
- **Lineage correction (2026-03-03):** Originally classified as Internally-Sourced because [S32] was listed first. But [S06] (Forms Digitization Meeting) is a client source, making this eligible for System Requirements.
- **Proposed MATRIX entry (applied):**

```
| AD-13 | In-context field guidance and companion document integration (extends UP-02) | ? | [S06] — "Form itself does not include the substantial context that comes with very lengthy instruction and guide documents"; [S32] | Broader than SF-424M cross-ref (UP-02): field-level help, section instructions, 62–150 page companion docs |
```

### Items with operational/stakeholder lineage — add as notes on existing MATRIX entries

#### WS-02 + WS-13 (PRA metadata and tracking) → ADD NOTE to MATRIX FI section

- **V2 IDs:** SCH-15 (Discovery), ADM-05 (Discovery)
- **Source docs:**
  - `docs/files/B09 SA 0001 - PWS...md` lines 50-56: Forms listed as "OMB Approved Form" / "OMB Approved Doc"
  - `docs/files/confluence-export/.../2025-09-25 Kickoff with CSBG Staff.md` line 115: "half of the forms on this new site, Melanie leads the PRA approval form"
  - `docs/files/confluence-export/.../2025-11-20 Check-in...md` line 39: "Monique manages the PRA approval for a little less than half of the other forms"
  - `docs/files/confluence-export/.../CSBG Annual Report.md` line 39: "Pending: PRA Approval - in progress"
- **Source IDs:** [S29], [S03], [S05], [S13]
- **Assessment:** PRA approval is a real operational dependency for form publishing, but no source doc frames it as a system requirement (e.g., "the system must track PRA status"). The MATRIX already lists "Capture PRA approval dependency" as a Next Step.
- **Proposed MATRIX note:** Add to §9 Form Inventory (FI) section:

```
> **Note:** PRA approval status is an operational dependency for form publishing. Melanie Durley manages PRA for approximately half the forms; Monique Alcantara for the other half. Source: [S03], [S05]. CSBG Annual Report PRA was "in progress" as of export date per [S13]. System implication: form administration needs PRA status visibility.
```

#### WS-16 (Congressional reporting) → ADD NOTE to MATRIX DA-09

- **V2 ID:** REV-06 | **V2 Provenance:** Discovery
- **Source docs:**
  - `docs/files/ACF Project Brief.md` line 25: "report on programmatic outcomes to Congress and the public"
  - `docs/files/B09 SA 0001 - PWS...md` lines 21, 37: Congressional reporting in problem statement
  - `docs/files/confluence-export/.../2025-09-25 Kickoff...md` line 115: "Melanie manages all of our congressional reporting"
  - `docs/files/confluence-export/.../2024-06-2024 Initial Conversation...md` line 40: "Data used for reporting to Congress, data performance warehouse"
- **Source IDs:** [S33], [S29], [S03], [S01]
- **Assessment:** Congressional reporting is a documented downstream workflow spanning multiple source docs including the PWS. But no source doc says "build congressional reporting tools." The system's role is to produce exportable data that Melanie's workflow consumes.
- **Proposed MATRIX note:** Expand DA-09 notes:

```
| DA-09 | Data exports feed Performance Management website (Monique Alcantara is COR) | ? | [S05]; [S03] | Congressional reporting is primary downstream consumer — Melanie manages all congressional reporting ([S03]); data flows from exports → PM website → Congress ([S01], [S33]) |
```

#### WS-17 (CQI workflow) → ADD NOTE to MATRIX WF-17

- **V2 ID:** REV-07 | **V2 Provenance:** Discovery
- **Source docs:**
  - `docs/files/confluence-export/.../2025-09-25 Kickoff...md` line 117: "she facilitates our continuous quality improvement sprints and exercises as a team"
  - `docs/files/confluence-export/.../2025-11-20 Check-in...md` line 40: same quote
- **Source IDs:** [S03], [S05]
- **Assessment:** Kayla's CQI facilitation is a documented internal workflow. No source doc says "build CQI tools." The system's role is to provide data visibility that supports CQI sprints.
- **Proposed MATRIX note:** Expand WF-17 notes to mention CQI as a specific collaboration workflow.

### Items with partial lineage — keep annotated in V3

#### WS-11 (Offline-first field administration)

- **V2 ID:** APP-17 | **V2 Provenance:** Discovery
- **Source doc:** `docs/files/confluence-export/.../2025-11-26 Forms Engine __ Forms Digitization.md` line 13: "ANA- Pull other reports grantee has filed, prepopulate portions of assessment before they go to onsite, like Alaska. Fear that what was on the internet wouldn't work."
- **Source ID:** [S06]
- **Assessment:** The user fear is documented. The "offline-first architecture" label is an engineering extrapolation. AD-09 in MATRIX covers "low-bandwidth/rural" but not zero-connectivity. The gap between AD-09 (slow internet) and WS-11 (no internet during on-site assessments) is real but not explicitly demanded by any source.
- **Action:** Keep as [WS-11] in V3 with trace to [S06]. Consider extending MATRIX AD-09 notes.

#### WS-20 (Trackable support interactions)

- **V2 ID:** SUP-03 | **V2 Provenance:** VSA
- **Source docs:**
  - `docs/files/PRODUCT SPEC — CORE (CSFEER) Tribal MVP.md` line 320: "Help desk issues tied to specific steps"
  - `docs/files/PRODUCT SPEC — CORE (CSFEER) Tribal MVP.md` line 349: "Ticket volume" (telemetry category)
  - `docs/files/ACF Forms Engine - User Personas.md` line 253: "Limited visibility into which features are causing most support tickets"
- **Source IDs:** [S36], [S32]
- **Assessment:** Metric targets and pain points exist. No doc says "build a support tracking tool." The concept is implied by the metrics.
- **Action:** Keep as [WS-20] in V3 with partial trace. Metrics already captured in MATRIX as PR-19 (<60 tickets/month) and SC-15 (≤1 ticket/org).

#### WS-21 (Help desk tooling)

- **V2 ID:** SUP-05 | **V2 Provenance:** VSA
- **Source docs:**
  - `docs/files/PMP V2.md` line 707: "Support Tiers: In-app help → help desk (email/phone) → tech escalation → on-site (as needed)"
  - `docs/files/PRODUCT SPEC — CORE (CSFEER) Tribal MVP.md` lines 43, 206: "Provide training, help desk support"
  - `docs/files/ACF Forms Engine - User Personas.md` lines 267-279: Full persona "Sri Patel – Contractor Support / DevOps & Help Desk Liaison"
- **Source IDs:** [S35], [S36], [S32]
- **Assessment:** A 4-tier support model is defined and a help desk liaison persona exists. But these describe operational support structure, not system features. The "in-app help" tier ([S35]) is the closest to a system feature requirement.
- **Action:** Keep as [WS-21] in V3. The "in-app help" tier from [S35] connects to WS-18 (contextual help).

#### WS-07/WS-08/WS-09 (Workflow complexity spectrum)

- **V2 IDs:** WFL-09 (VSA), WFL-11 (VSA), WFL-12 (VSA)
- **Source:** Traced to [S37] in MATRIX, but [S37] is listed as "synthesized" in MATRIX's source registry. The actual `Specific Requirements and Tasks.md` file doesn't contain these specific open questions.
- **Assessment:** These are MATRIX's own analytical questions about WF-09/WF-10 design gaps, not primary source requirements. They represent valid design questions but aren't traceable to source docs.
- **Action:** Keep as [WS-xx] in V3 with corrected annotation: trace is to MATRIX's analysis, not to a primary source document.

---

## Category 3: No Source Lineage (5 items — confirmed orphaned)

| WS-xx | V2 ID | V2 Provenance | Assessment |
|-------|-------|--------------|------------|
| **WS-01** | SCH-14 | VSA | "Data sensitivity classification per field" — zero hits in any source doc. CUI handling (AS-20) is document-level, not field-level. Per-field granularity is a VSA invention. |
| **WS-03** | SCH-17 | Engineering | "Schema-driven definitions decoupled from hardcoded UI" — one weak hit for "program-agnostic" which is about program scope, not schema architecture. The decoupling concept has no source. |
| **WS-12** | ADM-04 | PWS+ | "Form inventory visibility UI" — the static inventory (FI-01–FI-06) exists in source docs, but no doc asks for it as an application feature. |
| **WS-19** | SUP-02 | VSA | "Staff support console with scoped read-only access" — Personas mention "staff view" but that maps to UP-04 (portfolio dashboard). The scoped-read-only-for-support concept has no source. |
| (merged) | | | WS-07/WS-08/WS-09 have no *primary* source lineage (traced to MATRIX's own synthesized analysis, not to docs/files/). They remain as valid design questions but cannot be promoted to MATRIX. |

---

## Proposed MATRIX.md Edits

### New entries

1. **DA-15** in §4 Integration & Data (System Requirements) — conditional PDF, from [S03]
2. **FE-47** in §1 Form Engine (Implementation Decisions) — concurrent edit conflict handling, from [S21]
3. **AD-13** in §5 Accessibility & Design (Internally-Sourced) — contextual help/guidance, from [S32]/[S06]
4. **UP-12** in User Personas — support tier model, from [S35]/[S32]

### Notes on existing entries

5. **FI section** — PRA approval dependency note (from [S03], [S05], [S13])
6. **DA-09** — expand notes with congressional reporting downstream workflow (from [S03], [S29], [S33])
7. **WF-17** — add CQI workflow context (from [S03], [S05])
8. **AD-09** — note gap between "low-bandwidth" and "zero-connectivity" on-site assessments (from [S06])

### V3 cascade after MATRIX updates

Once MATRIX is updated:
- WS-24 → becomes DA-15 reference
- WS-05 → becomes FE-47 reference
- WS-18 → becomes AD-13 reference
- WS-02/WS-13 → annotation updated to reference MATRIX FI note
- WS-16 → annotation updated to reference MATRIX DA-09 expanded note
- WS-17 → annotation updated to reference MATRIX WF-17 note
- Remaining WS-01, WS-03, WS-07/08/09, WS-12, WS-19 stay as [WS-xx]

---

## Status

- [x] Lineage analysis complete against docs/files/ source of truth
- [x] Apply MATRIX.md edits (4 new entries + 4 note expansions) — applied 2026-03-03; AD-13 corrected from Internally-Sourced to System Requirements per client/internal source distinction
- [x] Cascade changes to WORKSTREAMS.md — applied 2026-03-03
- [x] Update V3 provenance summary counts — 17→14 WS-xx; ~155→~156 total
