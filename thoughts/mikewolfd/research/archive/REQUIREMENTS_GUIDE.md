# CSFEER Requirements — Plain Language

> Rewritten from [MATRIX.md](MATRIX.md) for readability. Original IDs appear in parentheses for traceability.
> Omits implementation decisions, ATO artifact tracking, and contract governance details — see MATRIX.md for those.
> Date: 2026-03-05

### Glossary

| Abbreviation | Meaning |
|---|---|
| ACF | Administration for Children and Families (HHS division) |
| ATO | Authority to Operate — federal security certification required before launch |
| CSBG | Community Services Block Grant — the federal grant program |
| CUI | Controlled Unclassified Information — sensitive but not classified data |
| FedRAMP | Federal Risk and Authorization Management Program — cloud security standard |
| FIPS | Federal Information Processing Standards — encryption requirements |
| FISMA | Federal Information Security Modernization Act — security compliance framework |
| NGSC | Next Generation Security Cloud — ACF's AWS hosting environment |
| NIST | National Institute of Standards and Technology — sets security standards |
| OCS | Office of Community Services — the ACF office that runs CSBG |
| OLDC | Online Data Collection system — the legacy system CORE replaces |
| PIA | Privacy Impact Assessment |
| SF-424M | Standard federal grant application form; tribes cross-reference fields against it |
| SORN | System of Records Notice — required Privacy Act documentation |
| UEI | Unique Entity Identifier — the key that links an organization across federal systems |
| USWDS | United States Web Design System — federal UI component library |
| VPAT | Voluntary Product Accessibility Template — accessibility conformance report |
| WCAG | Web Content Accessibility Guidelines — the accessibility standard (target: AA level) |

## What We're Building

A web application called CORE that replaces PDF-based grant reporting for tribal organizations receiving CSBG funding. Phase I targets ~66 tribal organizations submitting three forms digitally. The long-term vision: 25,000+ recipients across 100+ forms for all ACF program offices (64 currently documented).

### MVP Forms

| Form | Users | Notes |
|------|-------|-------|
| CSBG Tribal Plan and Application | ~66 orgs | Pre-award planning document |
| CSBG Tribal Annual Report (Long Form) | ~30 (up to 66) | 3 modules: Admin, Expenditures, Individual/Family |
| CSBG Tribal Annual Report (Short Form) | ~30 (up to 66) | Mandatory for orgs receiving <$50k — not a choice |

*(FI-01–FI-03)*

---

## 1. Forms

### Field Types

The system supports six field types: open text, auto-calculated values (formulas based on other inputs), pre-populated data from prior submissions or related forms, conditional/branching questions, one-to-many responses, and file attachments stored with the submission. *(FE-01–FE-06)*

### Validation

A rules engine validates data at three levels: individual fields, groups of fields, and whole forms. Each rule produces either a hard error (blocks submission) or a soft warning (informs but does not block). Rules compare values against formulas, prior submissions, and external registries like SAM.gov. The system catches errors during form completion, not afterward. *(FE-20–FE-25)*

> **Unresolved (C-1):** The contract says validation happens "while a grant-recipient fills out a form." The tech spec proposes review-page-only validation with partial saves of invalid data. Resolution needed.

### Version History

Multiple form versions coexist without losing existing submissions. Federal staff view any submission's state at any workflow point. Recipients compare current entries against past years, with per-field "what changed" indicators. *(FE-30–FE-32, UP-06)*

### Complexity Spectrum

The platform must support both simple and complex forms — from short-form tribal reports to multi-module annual reports with conditional logic. *(FE-07)*

### Standardization

Reduce the inconsistency that comes from custom state/tribal plans and third-party tools like SmartForms. *(FE-12)*

### Audit Trail

Every form action is logged by user. Field-level changes are tracked in detail. *(FE-34, FE-35)*

### Form Builder (Post-MVP)

A low-code/no-code builder for non-technical staff, with a testing sandbox. Explicitly deferred past year one. MVP uses hard-coded Python/Pydantic schemas. *(FE-40–FE-42)*

---

## 2. Workflow

### Filling Out Forms

- The system auto-creates forms for each recipient based on reporting schedules and pre-populates them with prior-year data. Previous submissions remain available for trend comparison and to avoid repeat data entry. *(WF-01, WF-02, WF-12)*
- Users save progress and return later. Auto-save runs every 30–60 seconds. Partial saves of invalid data are allowed. *(WF-11, FE-38)*
- Submission is a distinct action. After submitting, users can unsubmit or submit revisions. *(WF-04–WF-06)*
- Cross-form pre-population: the Tribal Plan draws data from the Tribal Annual Report, keyed by UEI. MVP limits pre-population to high-confidence data only. *(FE-03, FE-37, FE-46, DA-11)*

### Attestation

Transmittal letters require signatures, upload tracking, and status visibility. This is a separate workflow artifact, not just a form field. *(UP-03)*

### Collaboration and Review (Mostly Post-MVP)

- Multiple users entering data into one form, with routing and re-submission. **Out of MVP scope.** *(WF-15)*
- Customizable multi-step federal review and approval. **Out of MVP scope.** *(WF-09)*
- Visual/no-code workflow builder for review processes. **Post-MVP, aspirational.** *(WF-10)*

### Notifications (Post-MVP)

Real-time alerts tied to workflow events (submission received, form past due) and deadline-aware notifications — particularly the March 31 statutory deadline for CSBG Annual Reports per the CSBG Act. **Out of MVP scope per tech spec.** *(WF-13, WF-14, WF-18)*

### Tracking

Program staff, lead agencies, and sub-recipients all need visibility into form status across the submission-review-revision lifecycle. *(WF-17)*

---

## 3. Authentication & Security

### Who Logs In

- Government staff authenticate through `login.acf.gov` (Okta). *(AS-03)*
- Non-government users get a separate authentication path — **undefined and flagged as a risk.** *(AS-04)*
- Login.gov integration is contractual but **deferred from MVP.** MVP uses basic session management. *(AS-01, AS-18)*

> **Unresolved (C-13):** One acceptance criterion requires Login.gov working for all pilot users. The Q1 plan defers it. Which is it?

### Compliance

- **ATO required.** Target: May 29, 2026. This is the project's highest risk. *(AS-14, AS-15)*
- SORN and Privacy Impact Assessment required. PIA under review as of Feb 2026. *(AS-16, AS-17)*
- Zero Trust strategy per Executive Order 14028. CUI handling per NIST. *(AS-19, AS-20)*
- Federal data cannot train commercial AI models without approval. *(AS-21)*
- Incident response SLAs: Critical <1hr, High <4hrs, Medium <24hrs, Low <72hrs. *(AS-24)*
- Personnel: High-risk Public Trust clearance, background investigations, NDAs, annual security/privacy training. *(AS-22, AS-23)*

> **Unresolved (C-3):** FISMA classification is unclear. One source says Moderate; the compliance tracker references Low baseline controls. This determines the entire security posture.

---

## 4. Permissions

Role-based access across three tiers — sub-recipient, state, and federal. Recipients manage their own users (self-service). *(PM-01–PM-08)*

### Grantee Roles

| Role | Edit | Submit/Attest | Export | View |
|------|------|---------------|--------|------|
| Approver | Yes | Yes | Yes | Yes |
| Contributor | Yes | No | Yes | Yes |
| Viewer | No | No | PDF only | Yes |

*(UP-01)*

Federal staff (OCS) get read-only form access, a portfolio dashboard showing per-grantee status, batch review tools, and structured CSV/Excel exports for cross-grantee comparison. Admins manage users (search by org/person/email/UEI, few-click role changes) and view audit logs. *(UP-04, UP-05, UP-08)*

Leadership needs a simplified summary view: funding amount, major goals, key outcomes — separate from the full dense form. *(UP-07)*

> **Unresolved (C-5):** The contract lists permissions as Must priority. The tech spec says authorization is out of MVP scope.

---

## 5. Data & Integration

### Exports

- Individual submissions as PDFs, conditional-logic-aware: omit sections that don't apply. *(DA-04, DA-15)*
- Bulk data as CSV and human-readable formats for cross-grantee comparison. *(DA-03, UP-05)*
- Public-access links to specific portions of a submission. *(DA-05)*
- Exports feed the Performance Management website and congressional reporting. *(DA-09)*

### APIs (Scope Disputed)

- Read API for forms, submissions, and bulk extraction. *(DA-01)*
- Write API to import pre-populated data. *(DA-02)*
- Comprehensive API documentation. *(DA-06)*
- Real-time data access that does not degrade application performance. *(DA-07)*

> **Unresolved (C-4):** The contract says APIs are Must priority. The tech spec says out of scope. The PMP says read-only for MVP. The Q1 plan calls them a stretch goal.

### Data Migration

- OLDC DataConnect or Excel exports as the migration source. *(DA-10)*
- FY24 raw data exports and SmartForms XML/XSD artifacts available as schema references. *(DA-12, DA-13)*
- Program staff need to easily export, review, and correct data errors. *(DA-14)*

---

## 6. Accessibility & Design

- **508 compliance is mandatory.** WCAG AA front end. Contract specifies 2.0; building to 2.1/2.2 is advisable since 2.0 is outdated. Accessibility Conformance Report (VPAT) required. *(AD-01, AD-11, AD-12)*
- **USWDS** as the design system. The contract says "ideally" — 508 is the hard requirement. *(AD-02)*
- **Navigation:** clear progress indicators in multi-step forms. Plain language throughout. Consistent agency branding. *(AD-05, AD-06, AD-08)*
- **Low bandwidth:** support rural environments (Alaska named explicitly). The system must operate reliably despite poor connectivity, using auto-save and client-side caching with three connection states: "Saved," "Connection lost — work stored locally," "Reconnected — sync successful." *(AD-09, PR-14, FE-44, FE-45)*
- **In-context help:** field-level guidance linking fields to SF-424M/OLDC counterparts, plus companion document integration. Some forms have 62–150 page instruction guides — the form itself lacks that context today. *(AD-13, UP-02)*
- **Devices:** optimized for tablets and laptops. Modern browsers: Chrome, Firefox, Edge, Safari. *(AD-04, PR-13)*

---

## 7. Performance & Reliability

- **Speed:** form load/save in ≤3 seconds on 4G. Test on 3G as well. Target form completion time: <25 minutes. *(PR-01, PR-16, PR-17)*
- **Scale:** 200+ concurrent users. 1,100 grant recipients + sub-recipients + 75 federal staff. Peak load must hold around March 31 and other reporting deadlines. *(PR-02, PR-11, UP-09)*
- **Uptime:** ≥99.5% system, ≥99.9% API. Available 24/7. *(PR-03, PR-10, SC-20)*
- **Monitoring:** real-time dashboards for response time, latency, throughput, error rates, and concurrent users. Track median, P95, and P98. Aggregate user behavior. A/B testing support in production as needed. *(PR-04–PR-09)*
- **Testing:** >80% code coverage. Degraded-network test environments for reproducing low-connectivity issues. *(PR-15, UP-11)*
- **Hosting:** FISMA Moderate, FedRAMP, FIPS 140-2 encryption. AWS ECS on NGSC. *(PR-12, IT-02, IT-03)*
- **Operational targets:** <60 support tickets/month, <$50/form processing cost, 75% tribal digital adoption in Year 1. *(PR-19–PR-21)*
- **Feature flags:** runtime configuration for policy or OMB form changes without full redeployments. *(UP-10)*
- **Support model:** four tiers — in-app help, help desk (email/phone), tech escalation, on-site visits. *(UP-12)*

---

## 8. MVP Success

### Targets

| What | Target | Tension |
|------|--------|---------|
| Tribal orgs submitting digitally | 20+ (contract) vs. 10–12 (pilot plan) | **C-2** |
| Users reporting digital is easier than PDFs | ≥80% | |
| Section 508 compliance | 100% | |
| Security/compliance findings | Zero | |
| Architecture docs ready for Phase II | Complete | |
| Pilot submissions passing validation without OCS help | ≥90% | |
| Platform supports simple and complex forms | Demonstrated | |
| First measurable baseline for tribal reporting | Established | |
| Autosave success rate | ≥98% | |
| Data loss | 0% | |

*(SC-01–SC-07, SC-09, SC-12, SC-13)*

### Operational Targets (Internally Sourced)

These metrics come from internal product specs, not the contract. They extend the success criteria above.

| What | Target | ID |
|------|--------|----|
| Pilot orgs with successful submission | 100% | SC-08 |
| Errors resolved without OCS intervention | ≥85% | SC-10 |
| Reduction in OCS follow-up emails | ≥30% | SC-11 |
| User satisfaction rating | ≥4/5 | SC-14 |
| Help desk tickets per org | ≤1 | SC-15 |
| Submission time (currently 12–20 days) | 3–7 days | SC-16 |
| Component reuse across forms | ≥70% | SC-17 |
| New form onboarding time | ≤6 weeks | SC-18 |
| OCS review time reduction | ≥25% (long-term ≥50%) | SC-19 |
| API uptime | ≥99.9% | SC-20 |
| Form completion time reduction vs. legacy PDF | ≥25% | SC-21 |

### Concrete "Done" Gates

1. All three tribal forms available digitally with validation, save, and submit.
2. Login.gov working for all pilot users. **(Conflicts with Login.gov deferral — C-13.)**
3. CSV and PDF export functional.
4. At least 10 tribal orgs submit successfully during pilot.

*(AC-01–AC-04)*

---

## 9. Open Conflicts & Key Risks

Thirteen source-document disagreements (C-1–C-13) and fourteen project risks (R-01–R-14) are maintained in [UNDERSTANDING.md](UNDERSTANDING.md). Five conflicts are MVP-blocking: C-1, C-3, C-5, C-7, C-13. The top risk is ATO delays (p×i = 0.45).

Inline ⚡ C-xx flags throughout this document mark where conflicts touch specific requirements.

---

## 10. Timeline

| Milestone | Target |
|-----------|--------|
| Landing page deployed | 2026-03-01 |
| Tribal Annual Report (long form) | 2026-03-15 |
| Tribal Plan and Application | 2026-03-31 |
| ATO documentation submitted | 2026-03-31 |
| ATO authorization target | 2026-05-29 |
| Soft launch (10–12 tribal orgs, white-glove support) | Month 9 |
| Full rollout (remaining orgs) | Month 12 (post-ATO) |

Build order: rendering → saving → review page → auto-save → PDF export. Each step depends on the previous one.

Stage gates: Discovery (M2), MVP (M8), Pilot (M9), Continuous Development (M15).

*(DL-01–DL-15)*

---

## 11. Technology

Python 3.12, Django 6, PostgreSQL on AWS ECS (NGSC). Alpine.js for frontend reactivity. USWDS 3.13+ for design. Django Ninja for REST APIs. WeasyPrint for PDFs. Django Cotton for reusable template components. Keycloak for local dev auth mock. Forms defined as Python/Pydantic schemas (single source of truth for UI structure, validation, and UX).

Open-source codebase preferred. GitLab repo with GitHub mirroring. Jira for sprints, Confluence for docs, Figma for design, Mural for workshops.

*(IT-01–IT-20)*

---

## 12. Beyond MVP

| Phase | Scope |
|-------|-------|
| **Phase II** | State/territory forms (~53+ orgs). OLDC runs in parallel. |
| **Phase III** | Full migration. OLDC sunset. |
| **Long-term** | 25,000+ recipients, 100+ forms across all ACF offices (64 currently documented). |

Phase II adds three forms: CSBG Eligible Entity List (a document, not a form), CSBG State and Territory Plan, and CSBG Annual Report 3.0 (4 modules, 53+ users). *(FI-04–FI-06)*

Interested programs: ANA (needs offline support), Children's Bureau (26-page forms with 150-page guides), LIHEAP (named as next target), Diaper Program, Rural Development.

*(PH-01–PH-04)*

---

## Appendix: Traceability Map

### IDs Traced in Body

Each ID below appears in at least one prose sentence or table row in this document.

| Section | Original IDs |
|------------|-------------|
| Forms — field types | FE-01–FE-07, FE-12 |
| Forms — validation | FE-20–FE-25 |
| Forms — version history | FE-30–FE-32, UP-06 |
| Forms — audit trail | FE-34, FE-35 |
| Forms — builder | FE-40–FE-42 |
| Workflow — filling out forms | WF-01, WF-02, WF-04–WF-06, WF-11, WF-12, FE-03, FE-37, FE-38, FE-46, DA-11 |
| Workflow — attestation | UP-03 |
| Workflow — collaboration & tracking | WF-09, WF-10, WF-15, WF-17 |
| Workflow — notifications | WF-13, WF-14, WF-18 |
| Auth & security | AS-01, AS-03, AS-04, AS-14–AS-24 |
| Permissions | PM-01–PM-08, UP-01, UP-04, UP-05, UP-07, UP-08 |
| Data & integration | DA-01–DA-07, DA-09, DA-10, DA-12–DA-15, UP-05 |
| Accessibility & design | AD-01, AD-02, AD-04–AD-06, AD-08, AD-09, AD-11–AD-13, FE-44, FE-45, PR-14, UP-02 |
| Performance & reliability | PR-01–PR-13, PR-15–PR-21, UP-09, UP-10, UP-11, UP-12 |
| MVP success — contractual | SC-01–SC-07, SC-09, SC-12, SC-13, AC-01–AC-04 |
| MVP success — internally sourced | SC-08, SC-10, SC-11, SC-14–SC-21 |
| Form inventory | FI-01–FI-06 |
| Beyond MVP | PH-01–PH-04 |

### IDs Summarized as Groups (Not Individually Addressed)

These ranges appear as bulk citations. The body captures the theme but not every individual item. See MATRIX.md for specifics.

| Section | Original IDs | Notes |
|------------|-------------|-------|
| Risks | R-01–R-14 | Conflicts and risks maintained in [UNDERSTANDING.md](UNDERSTANDING.md); see MATRIX.md for requirement-level traceability |
| Timeline | DL-01–DL-15 | V2 covers milestones and build order; omits story point estimates (DL-06) and sprint-level detail |
| Technology | IT-01–IT-20 | V2 summarizes the stack; omits operational details like PIV card requirements (IT-18), ServiceNow provisioning (IT-20) |

### IDs Intentionally Omitted

These IDs describe implementation decisions, ATO artifact tracking, contract governance, or low-priority items. They remain in MATRIX.md and are excluded from this plain-language summary by design.

| Category | Omitted IDs | Reason |
|----------|-------------|--------|
| Form engine implementation | FE-08–FE-11, FE-33, FE-36, FE-39, FE-43, FE-47 | HOW decisions (JSON storage, Pydantic schema wiring, status lifecycle, screener flow, conflict handling) — not WHAT requirements |
| Auth implementation | AS-02, AS-05–AS-13 | OIDC flow mechanics, Keycloak config, token lifetimes, auto-provisioning, group sync — implementation details |
| Data implementation | DA-08 | WeasyPrint choice — covered in Technology section prose without ID |
| Accessibility | AD-10 | Prototype-to-implementation variance caveat — process note, not a requirement |
| Workflow | WF-07, WF-16 | WF-07 is a probable duplicate of WF-06; WF-16 is a misplaced contract deliverable workflow |
| Contract governance | CG-01–CG-14 | Contract structure, FTE model, governance cadences, IP ownership — see MATRIX.md §Contract & Governance |
| ATO artifacts | AS-A1–AS-A14 | Individual artifact status tracking — see MATRIX.md §ATO Artifacts |
| Derived stretch items | WS-01–WS-03, WS-07–WS-09, WS-11–WS-13, WS-16, WS-17, WS-19, WS-20 | Value stream derived requirements — data sensitivity, PRA metadata, schema decoupling, conditional routing, parallel approval, delegation, offline-first, form inventory, congressional reporting, CQI workflow, support console. All post-MVP or stretch; themes covered in body where applicable (e.g., offline in §6, review workflows in §2) |

*Condensed from [MATRIX.md](MATRIX.md). Full source document registry, implementation decisions, ATO artifact inventory, and contract governance details remain in the original.*
