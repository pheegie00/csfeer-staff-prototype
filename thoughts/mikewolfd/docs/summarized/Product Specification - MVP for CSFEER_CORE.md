# Product Specification: MVP for CSFEER/CORE -- Synthesized

**Summary:** Defines the Phase I MVP scope targeting 66 tribal organizations with three specific forms (Tribal Plan, Tribal Annual Report, Tribal Annual Report Short Form). Establishes concrete success metrics, non-functional requirements, role-based permissions, and a 12-month release timeline. Most content aligns with core context but adds specificity on SLAs, governance, and acceptance criteria.

---

## Additions Beyond Core Context

### Alternate System Name
The document references the name **CORE** (Community Outcomes Reporting Engine) as a tentative system name alongside CSFEER. This may cause confusion in external communications if not resolved.

### Role-Based Permissions (MVP)
Three roles defined for MVP:
- **Contributor** -- can edit forms
- **Approver** -- can submit forms
- **Viewer** -- read-only access

Core context mentions "multi-person collaboration" but does not specify these roles.

### Success Metrics
| Metric                         | Target                         |
| ------------------------------ | ------------------------------ |
| Tribal adoption (Year 1)       | >= 75% submit through platform |
| Form completion time reduction | >= 25% vs legacy PDF           |
| Automated validation pass rate | >= 90% before submission       |
| User satisfaction              | >= 4/5                         |

### Non-Functional Requirements (Concrete Targets)
| Requirement            | Target                                |
| ---------------------- | ------------------------------------- |
| Security baseline      | FISMA Moderate, FIPS 140-2 encryption |
| Form load/save latency | <= 3 seconds                          |
| Concurrent users       | >= 200                                |
| Uptime                 | >= 99.5%                              |

### Governance and ATO
- Aligned with ACF OCIO Governance Framework (PMP, bi-weekly dashboards, monthly CSRs, mid-year performance reports).
- **ATO target: 18 months** from project start, with core security controls in place for MVP.

### MVP Acceptance Criteria
- All three tribal forms available digitally with validation + save/submit.
- Login.gov working for all pilot users.
- CSV + PDF export functional.
- **At least 10 tribal orgs** successfully submit during pilot (lower bar than the 75% Year 1 metric).
- Section 508 conformance verified with VPAT available.

### Release Timeline
| Phase                                                | Months |
| ---------------------------------------------------- | ------ |
| Discovery (user research, form mapping, tech spikes) | 1-2    |
| Wireframes, prototypes, validation workshops         | 3-5    |
| MVP development (forms engine + 3 pilot forms)       | 4-8    |
| Soft rollout to tribal orgs                          | 9      |
| Iteration and stabilization                          | 9-12   |

### Explicit MVP Exclusions
- **Low-code/no-code form builder** -- planned post-Year 1 (implies eventual non-developer form authoring).
- Advanced analytics/dashboards beyond CSV/API export.
- Legacy system retirement (post-Phase III).

### MVP Forms (Exactly Three)
1. CSBG Tribal Plan and Application
2. CSBG Tribal Annual Report
3. CSBG Tribal Annual Report (Short Form)

Core context mentions Modules 1-3 "combined" for tribal track. The short form variant is not mentioned in core context.

### User Cohorts
- **Primary:** Staff from 66 tribal orgs.
- **Secondary:** OCS program officers reviewing submissions.
- **Support:** System admins (contractor + ACF IT). Core context does not mention a contractor admin role.

### API Constraint
APIs described as **read-only** endpoints for ACF staff data extraction. Core context describes "API + CSV + PDF export" without the read-only qualifier. This may need revisiting if write APIs are needed for integrations.

### Accessibility
Document specifies **WCAG 2.0 AA**. Current best practice is WCAG 2.1 AA; confirm which standard is contractually required.

---

## Contradictions / Ambiguities

1. **System name:** "CORE" vs "CSFEER" -- document uses CORE as tentative name. Current codebase uses CSFEER.
2. **Tribal Annual Report Short Form** -- not mentioned in core context's description of tribal track forms. Clarify if this is a distinct form definition or a conditional variant of the full Annual Report.
3. **Read-only API** -- core context implies broader API capability. Confirm whether MVP truly excludes write endpoints or if this is outdated.
4. **WCAG 2.0 vs 2.1** -- document says 2.0 AA. Modern federal guidance often requires 2.1 AA. Verify contractual obligation.
5. **Version control of forms** -- document mentions "historical versions with timestamped submission records." Core context does not address form versioning. Clarify if this means form *definition* versioning or submission *snapshot* history.
