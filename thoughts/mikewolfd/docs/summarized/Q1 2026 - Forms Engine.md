# Q1 2026 Forms Engine Plan -- Synthesized

Q1 2026 (Jan-Mar) plan focuses on delivering two tribal CSBG forms as the MVP: Tribal Annual Report (long form) by March 15, Tribal Plan and Application by March 31. The plan was structured around government shutdown risk mitigation, prioritizing work executable without ACF input. Sprint-level detail reveals the actual development sequence: form rendering, data saving, review page, auto-save, then PDF export.

---

## Additions & Clarifications vs. Core Context

### Tribal AR Short Form Variant
Story 2.6 explicitly calls out a **short form variant** of the Tribal Annual Report, derived from the long form base with a simplified field set. The UI must support clear differentiation between long and short variants and seamless switching between them. This confirms the short form mentioned in the Project Brief.

### Pre-Population Is Cross-Form
Pre-population is not just from prior-year submissions of the same form -- **Tribal Plan (Form 2) pre-populates from Tribal AR (Form 1) data**. This means cross-form data dependencies and shared field identifiers are architectural requirements, not just same-form year-over-year copy.

### Auto-Save with Interval
Sprint 8 specifies **periodic auto-save every 30-60 seconds** with success/failure messaging. This is more specific than core context's "save/resume" capability and implies debounced persistence, conflict handling, and user feedback UX.

### PDF Export from Review Page
PDF generation is specified to work **from the review page data**, not from raw form data. This means the review page's data aggregation logic is a dependency for PDF export.

---

## Delivery Timeline

| Milestone                                 | Target Date |
| ----------------------------------------- | ----------- |
| Landing page deployed                     | March 1     |
| Tribal Annual Report (long form) complete | March 15    |
| Tribal Plan and Application complete      | March 31    |
| ATO documentation package submitted       | March 31    |

---

## Sprint Sequence (Actual Build Order)

| Sprint   | Dates     | Focus                                                                                                                                 |
| -------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Sprint 6 | Jan 14-28 | Long form rendering, USWDS components, review page start, project rename                                                              |
| Sprint 7 | TBD       | Complete long form rendering with real data, data saving across all sections, review page MVP (read-only), researcher + PM onboarding |
| Sprint 8 | TBD       | PDF export from review page, auto-save Phase 1 (30-60s interval), research plan                                                       |

Key sequencing: data saving must precede review page; review page must precede PDF export.

---

## Epic Budget (Story Points)

| Epic                                    | Points  | Shutdown-Safe % |
| --------------------------------------- | ------- | --------------- |
| 1: Foundation Infrastructure & Security | 25      | 90%             |
| 2: Tribal Annual Report (Form 1)        | 35      | 75%             |
| 3: USWDS Component Library              | 45      | 95%             |
| 4: Tribal Plan (Form 2)                 | 32      | 70%             |
| 5: Data Management & Export APIs        | 25      | 85%             |
| 6: Continuous ATO & Security            | 30      | 90%             |
| **Total**                               | **192** |                 |

---

## USWDS Component Inventory

The plan specifies 15 components in three tiers:

1. **Core form** (Stories 3.1-3.5): text inputs, textareas, selects, checkboxes, radio buttons
2. **Layout/navigation** (Stories 3.6-3.10): headers, footers, navigation, breadcrumbs, progress indicators
3. **Advanced form** (Stories 3.11-3.15): file upload, date picker, address validation, calculation fields, repeatable sections

---

## ATO / Security Detail

ATO work is distributed as **weekly 3-point stories from Weeks 2-11**, not a big-bang effort. The weekly cadence:

- Weeks 2-4: Documentation (controls, risk assessment, SSP)
- Weeks 5-6: Vulnerability assessment planning + security testing
- Weeks 7-8: Compliance gap analysis + security hardening
- Weeks 9-10: Penetration testing + documentation finalization
- Week 11: ATO package preparation and review
- Week 12: Final submission (budgeted in other epics)

---

## Infrastructure Notes

- **Session management without Login.gov** (Story 1.3) confirms that initial MVP does not integrate Login.gov auth -- a basic user identification system is used instead. Login.gov integration is deferred.
- **Performance optimization for rural connections** is called out as an acceptance criterion for the data persistence layer (Story 1.4). This implies bandwidth-constrained design considerations (small payloads, progressive loading, offline-resilient saves).
- **Email capabilities** are mentioned alongside PDF download (Story 2.4), suggesting email delivery infrastructure is in scope for Q1.

---

## Potential Contradictions / Notes

- Core context lists Login.gov auth as a core capability, but Story 1.3 explicitly designs session management **without Login.gov**. These are consistent if Login.gov is a later integration, but the timeline for Login.gov is not addressed in this document.
- The plan mentions "API endpoints for data export" as a **stretch goal** under Objective 1, but Epic 5 allocates 25 story points to it as planned work. The stretch goal framing suggests it may be deprioritized if forms slip.
- Story 2.4 mentions "email capabilities" for PDF export, which is not referenced anywhere in core context. This may imply an email notification system or could be aspirational scope.
- The total story point budget (192 across 11-12 weeks) is aggressive for the team size (~4.75 FTE per Project Brief). Sprint velocity benchmarks are not stated.
