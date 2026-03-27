# Product Requirements Document: CSFEER

**Community Services Forms Engine for Efficient Reporting (CSFEER)**

| Field           | Value                                                          |
| --------------- | -------------------------------------------------------------- |
| Product Owner   | Office of Community Services (OCS), ACF                        |
| Status          | Discovery / Pre-MVP                                            |
| Target Launch   | Phase I within 12-month base period                            |
| Total Timeline  | 24 months (12-month base + 12-month option)                    |
| Working Name    | Community Outcomes Reporting Engine (CORE) — scalable platform |
| Source Document | PWS ADMIN/OCS/CSBG/CSFEER v2 (Rev 2, August 25, 2025)          |

---

## 1. Vision

A scalable, user-centered digital forms platform that replaces legacy PDF-based data collection for ACF grant programs. The platform streamlines the entire grants reporting lifecycle — from pre-award planning through post-award reporting and Congressional performance analysis — while maintaining a simple, accessible user experience.

The long-term vision extends beyond a single program: if successful, CSFEER becomes the **single reporting platform for all ACF grant programs**, serving 25,000+ recipients across 100+ forms and hundreds of federal staff.

---

## 2. Problem Statement

### Current State

OCS administers ~$6.29B annually across 7 programs serving 36.8M Americans in poverty. Grant recipients are required by law to submit extensive pre-award and post-award forms. Today:

- Forms are **fillable PDFs** exchanged manually, requiring substantial out-of-system preparation.
- Data validation happens **after submission**, not during entry.
- Historical comparisons require **manual cross-referencing** between submissions.
- Federal staff cannot easily **export, query, or analyze** collected data at scale.
- States and tribes sometimes use **custom or third-party reporting tools**, creating compatibility issues and data variability.
- There is **no collaborative workflow** — multiple people cannot work on a single form submission, and routing/approval is manual.

### Top Problems to Solve

1. Enable new forms to be designed, updated, and tested more quickly by program staff.
2. Improve the form interface to be more intuitive and user-friendly for grant recipients.
3. Improve tracking and collaboration on forms between program staff, lead agencies, and sub-recipients around submission, reviews, and revisions.
4. Automate data validation while a grant recipient fills out a form using business logic, errors, and warnings.
5. Automate comparison to data from integrations (e.g., UIE mismatches).
6. Enable program staff to easily export, review, and correct errors (e.g., missing data, data conflicts, new elements).
7. Reduce compatibility issues and variability from custom State/Tribal plans and custom or third-party-enabled State annual reports.
8. Provide real-time access to system data without hindering application performance.

---

## 3. Users & Personas

### 3.1 Grant Recipients (~1,100 users at scale)

Users who submit pre-award and post-award forms to ACF.

| Sub-group                     | Estimated Count | Key Actions                                       |
| ----------------------------- | --------------- | ------------------------------------------------- |
| Tribal recipients             | ~66             | Submit Tribal Plan, Tribal Annual Report          |
| State/territory lead agencies | ~53             | Submit State Plan, Module 1, Eligible Entity List |
| Eligible entities (local)     | ~1,000+         | Submit Modules 2, 3, 4                            |
| Sub-recipients                | Varies          | View, edit, and collaborate on form sections      |

**Needs:** Save and resume progress, collaborate with colleagues on a single form, see historical data inline, receive clear validation feedback during data entry, upload attachments, unsubmit or revise forms after submission.

**Permission levels:** View-only, View & Edit, View & Submit.

### 3.2 Federal Staff (~75 users)

ACF/OCS program staff who review, approve, analyze, and report on submitted data.

**Needs:** Review and route submissions through customizable approval workflows, compare current submissions against historical data, export data via API/CSV for analysis, generate PDF exports, flag and return submissions for revision, access real-time dashboards and metrics.

**Permission levels:** Review, Route, Approve, Analyze, Compare Historical Data, Export.

### 3.3 Future: Non-Technical Program Staff

Staff who will build and manage forms without developer involvement (Year 2+).

**Needs:** Low-code/no-code form builder with sandbox/testing, visual workflow builder for review/approval processes.

---

## 4. Scope

### 4.1 In Scope — MVP (Phase I)

The initial production launch targets **Tribal recipients only** (~66 users) and replaces three existing fillable PDFs:

| Form                                   | Type       | OMB Status |
| -------------------------------------- | ---------- | ---------- |
| CSBG Tribal Plan and Application       | Pre-award  | Approved   |
| CSBG Tribal Annual Report              | Post-award | Approved   |
| CSBG Tribal Annual Report (Short Form) | Post-award | Approved   |

MVP capabilities:

- Digital form submission replacing PDF workflows
- Authentication via Login.gov
- Save-and-resume form progress
- Basic field validation (hard errors + warnings)
- Pre-population from prior submissions
- Multi-person collaboration on a single form
- Submit / unsubmit / revise workflow
- Federal staff review and approval workflow
- Data export (API + CSV)
- PDF export of individual submissions
- Section 508 / WCAG AA compliance
- USWDS-based UI

### 4.2 In Scope — Phase II

Scale to include State and Territory forms with an opt-in migration (legacy system remains operational):

| Form                          | Type       | OMB Status |
| ----------------------------- | ---------- | ---------- |
| CSBG Eligible Entity List     | Reference  | Approved   |
| CSBG State and Territory Plan | Pre-award  | Approved   |
| CSBG Annual Report 3.0        | Post-award | Approved   |

Additional capabilities:

- Module-based reporting (Modules 1–4)
- Eligible entity hierarchical data collection (state → local agency)
- Dual-system operation during migration period

### 4.3 In Scope — Phase III

Full migration: all users on the new platform, legacy system sunset.

### 4.4 Out of Scope (for now)

- Forms for non-CSBG grant programs (future CORE vision)
- Low-code/no-code form builder (post-Year 1)
- Visual workflow builder for non-technical staff (post-Year 1)
- Integration with other ACF systems beyond data export

---

## 5. Functional Requirements

### 5.1 Form Engine

| ID    | Requirement                                                                   | Priority |
| ----- | ----------------------------------------------------------------------------- | -------- |
| FE-01 | Support manual data entry fields (open text, numeric, date, select)           | Must     |
| FE-02 | Support auto-calculated fields using formulas based on other field values     | Must     |
| FE-03 | Support pre-populated fields from prior submissions and cross-form data       | Must     |
| FE-04 | Support complex form logic: conditional fields, branching questions           | Must     |
| FE-05 | Support one-to-many response types (multiple responses for a single question) | Must     |
| FE-06 | Support file attachment fields stored with the submission                     | Must     |
| FE-07 | Support free-text narrative fields alongside structured data entry            | Must     |
| FE-08 | Support financial detail fields with appropriate formatting and validation    | Must     |

### 5.2 Validation Engine

| ID    | Requirement                                                                                   | Priority |
| ----- | --------------------------------------------------------------------------------------------- | -------- |
| VE-01 | Flexible validation rules engine supporting calculations and comparisons to prior submissions | Must     |
| VE-02 | Hard-error validations that block submission                                                  | Must     |
| VE-03 | Warning/notification validations that inform but do not block                                 | Must     |
| VE-04 | Field-level validation (individual field)                                                     | Must     |
| VE-05 | Field-group-level validation (related fields)                                                 | Must     |
| VE-06 | Form-level validation (cross-section checks)                                                  | Must     |
| VE-07 | Real-time validation during data entry (not only on submit)                                   | Must     |

### 5.3 Version Control & Data Integrity

| ID    | Requirement                                                                                           | Priority |
| ----- | ----------------------------------------------------------------------------------------------------- | -------- |
| VC-01 | Support multiple simultaneous versions of a form definition while preserving existing submission data | Must     |
| VC-02 | Robust version history: federal staff can view any submission's state at any point in the workflow    | Must     |
| VC-03 | Recipients can view and compare past submissions side-by-side                                         | Must     |

### 5.4 Form Submission Workflow

| ID    | Requirement                                                                                    | Priority |
| ----- | ---------------------------------------------------------------------------------------------- | -------- |
| WF-01 | Auto-create and initialize forms for recipients based on reporting schedules                   | Must     |
| WF-02 | Pre-populate new forms with previous-year data to show trends                                  | Must     |
| WF-03 | Multiple individuals on the recipient side can collaborate on a form before submission         | Must     |
| WF-04 | Recipients can save progress and return later                                                  | Must     |
| WF-05 | Recipients can unsubmit forms                                                                  | Must     |
| WF-06 | Recipients can submit revisions to already-submitted forms                                     | Must     |
| WF-07 | Customizable multi-step, multi-person federal review and approval process                      | Must     |
| WF-08 | Visual/no-code workflow builder for federal approval workflows (workflows differ by form)      | Should   |
| WF-09 | Customizable real-time alerts and notifications (new form available, past due, rejected, etc.) | Must     |

### 5.5 Permissions & User Management

| ID    | Requirement                                                                                | Priority |
| ----- | ------------------------------------------------------------------------------------------ | -------- |
| PM-01 | Flexible permissions system controlling read, write, and export access                     | Must     |
| PM-02 | Self-service user management: recipients administer their own accounts and permissions     | Must     |
| PM-03 | Hierarchical administration: sub-recipient admins manage their users, states manage theirs | Must     |
| PM-04 | Minimum permission levels per tier: read-only, write-only, approve                         | Must     |
| PM-05 | Federal staff roles: review, route, approve, analyze, compare, export                      | Must     |

### 5.6 Integration & Data Access

| ID    | Requirement                                                         | Priority |
| ----- | ------------------------------------------------------------------- | -------- |
| DA-01 | Flexible read API for forms, submissions, and bulk data extraction  | Must     |
| DA-02 | Write API for importing pre-populated data                          | Must     |
| DA-03 | CSV export of submission data                                       | Must     |
| DA-04 | Human-readable export formats                                       | Must     |
| DA-05 | PDF export of individual form submissions                           | Must     |
| DA-06 | Public-access link generation for specific portions of a submission | Should   |
| DA-07 | Comprehensive, developer-friendly API documentation                 | Must     |

### 5.7 Notifications & Business Logic

| ID    | Requirement                                                                                 | Priority |
| ----- | ------------------------------------------------------------------------------------------- | -------- |
| NF-01 | Deadline-aware notifications (upcoming due dates, overdue forms)                            | Must     |
| NF-02 | Workflow-triggered notifications (submission received, review complete, revision requested) | Must     |
| NF-03 | Configurable notification channels and recipients                                           | Should   |

---

## 6. Non-Functional Requirements

### 6.1 Security & Compliance

| ID    | Requirement                                                                                           | Priority |
| ----- | ----------------------------------------------------------------------------------------------------- | -------- |
| SC-01 | Authentication via Login.gov                                                                          | Must     |
| SC-02 | Authority to Operate (ATO) within 18 months                                                           | Must     |
| SC-03 | System of Records Notice (SORN)                                                                       | Must     |
| SC-04 | FISMA compliance — all known security vulnerabilities addressed with urgency proportional to severity | Must     |
| SC-05 | All dependencies kept on recent versions                                                              | Must     |
| SC-06 | 24/7 operational availability                                                                         | Must     |

### 6.2 Accessibility

| ID    | Requirement                                             | Priority |
| ----- | ------------------------------------------------------- | -------- |
| AC-01 | Section 508 / WCAG AA compliant front end               | Must     |
| AC-02 | U.S. Web Design System (USWDS) as the design foundation | Must     |
| AC-03 | Incident management for accessibility issues            | Must     |

### 6.3 Performance & Scalability

| ID    | Requirement                                                                           | Priority |
| ----- | ------------------------------------------------------------------------------------- | -------- |
| PS-01 | Real-time system data access without degrading application performance                | Must     |
| PS-02 | Monitor response time, latency, throughput, and error rates in real time              | Must     |
| PS-03 | Track median, 95th-percentile, and 98th-percentile performance                        | Must     |
| PS-04 | Track concurrent users in real time                                                   | Must     |
| PS-05 | Scale to 1,100+ grant recipients + 75 federal staff with varying permission levels    | Must     |
| PS-06 | Platform architecture supports future scaling to 25,000+ recipients across 100+ forms | Should   |

### 6.4 Technology

| ID    | Requirement                                                                     | Priority |
| ----- | ------------------------------------------------------------------------------- | -------- |
| TC-01 | Open-source codebase using standard, sustainable open-source libraries          | Must     |
| TC-02 | Modern technology stack                                                         | Must     |
| TC-03 | CI/CD pipeline with automated testing, code reviews, and infrastructure as code | Must     |
| TC-04 | Affordable scaling of user licenses (if applicable)                             | Must     |
| TC-05 | All code, designs, and documentation are property of ACF                        | Must     |

---

## 7. CSBG Program Context

Understanding the data model is critical to building the right forms. CSBG has two reporting tracks with different form structures:

### 7.1 Tribal Track (Phase I target)

Tribes and Tribal organizations receive CSBG funding directly and report directly to OCS.

```
OCS
 └── Tribe / Tribal Org (direct-funded)
      ├── Submits: Tribal Plan (pre-award, annual or biannual)
      └── Submits: Tribal Annual Report or Short Form (post-award, annual)
           └── Contains Modules 1–3 (combined in Tribal forms)
```

### 7.2 State/Territory Track (Phase II target)

States receive funding and distribute to local eligible entities.

```
OCS
 └── State / Territory Lead Agency
      ├── Submits: State Plan (pre-award, annual or biannual)
      ├── Submits: Eligible Entity List
      ├── Submits: Annual Report Module 1 (State administration)
      └── Eligible Entities (local agencies)
           ├── Submit: Module 2 (entity administration & spending)
           ├── Submit: Module 3 (individual/family services & demographics)
           └── Submit: Module 4 (community-level strategies & results)
```

### 7.3 Reporting Cycle

- **Annual grant cycle** — each recipient submits forms once per year.
- **Plan Applications** can be submitted annually or biannually.
- **Annual Reports** are submitted once per year after the reporting period.
- Federal staff review, analyze, and ultimately report outcomes to Congress and the public.

---

## 8. Success Metrics

| Metric                              | Measurement Approach                                  |
| ----------------------------------- | ----------------------------------------------------- |
| Form completion rate                | % of initiated forms that reach submission            |
| Time to complete a form             | Median and p95 duration from first open to submit     |
| Validation error rate at submission | % of submissions with blocking errors on first submit |
| Federal review cycle time           | Time from submission to final approval                |
| User satisfaction (recipients)      | Survey / feedback mechanism embedded in platform      |
| User satisfaction (federal staff)   | Survey / feedback mechanism                           |
| Data export usage                   | API calls, CSV downloads per period                   |
| System uptime                       | % availability (target: 99.9%)                        |
| Accessibility compliance            | Automated + manual 508 audit results                  |
| Concurrent user capacity            | Real-time monitoring under load                       |

---

## 9. Phased Rollout Plan

```
Month 0–3      Discovery & user research (continuous throughout)
                ├── Stakeholder interviews (recipients, federal staff)
                ├── Current-state process mapping
                ├── Pain point prioritization
                └── Product roadmap v1

Month 3–9      MVP Development (Phase I)
                ├── 3 Tribal forms digitized
                ├── Core form engine + validation engine
                ├── Login.gov authentication
                ├── Save/resume, submit/unsubmit workflow
                ├── Federal review workflow
                ├── API + CSV export
                └── Launch to ~66 Tribal users

Month 9–18     Phase II — State/Territory Expansion
                ├── 3 additional forms (State Plan, Annual Report 3.0, Entity List)
                ├── Module-based reporting (Modules 1–4)
                ├── Opt-in migration (legacy runs in parallel)
                ├── Hierarchical permissions (state → entity)
                └── Scale to ~53+ additional state-level users

Month 18–24    Phase III — Full Migration
                ├── All users on new platform
                ├── Legacy system sunset
                ├── ATO achieved (by month 18)
                └── Transition planning for next contract period
```

*Timelines are notional and subject to change based on discovery findings and agile prioritization.*

---

## 10. Design Principles

1. **User-centered** — Discovery and user research drive every feature decision.
2. **Iterative** — Ship frequently, learn from real users, adjust.
3. **Accessible** — WCAG AA, USWDS, plain language, clear navigation.
4. **Scalable** — Architect for one program now, 100+ forms later.
5. **Open** — Open-source stack, comprehensive APIs, standard data formats.
6. **Contextual** — Show historical data inline, pre-populate where possible, minimize redundant data entry.

---

## 11. Constraints & Assumptions

### Constraints

- Must use Login.gov for authentication.
- Must achieve ATO within 18 months to collect real data in production.
- Must comply with Section 508 / WCAG AA.
- Must comply with FISMA security requirements.
- All artifacts are government property.
- System must operate 24/7.
- Team available 9 AM – 5 PM ET on business days.

### Assumptions

- The initial MVP focuses on CSBG Tribal forms but the architecture should not be CSBG-specific.
- Grant recipients currently invest significant time preparing submissions outside the system — reducing this overhead is a primary value driver.
- Forms change over time; the platform must handle form version evolution without breaking existing submissions.
- The annual reporting cycle means there are natural deadlines that drive user behavior and system load patterns.
- Federal staff needs extend beyond data collection into analysis, comparison, and Congressional reporting.

---

## 12. Open Questions

| #   | Question                                                                                           | Impact    |
| --- | -------------------------------------------------------------------------------------------------- | --------- |
| 1   | What are the specific validation rules for each of the 3 Tribal forms?                             | MVP scope |
| 2   | What does the current federal review/approval workflow look like in practice?                      | WF-07     |
| 3   | What existing systems (if any) hold historical submission data that needs to be migrated/imported? | DA-02     |
| 4   | What are the specific SORN and ATO requirements and timelines?                                     | SC-02/03  |
| 5   | How do Tribal recipients currently collaborate on form preparation?                                | WF-03     |
| 6   | What analytics and reporting does Congress require from this data?                                 | DA-01     |
| 7   | Are there existing ACF CI/CD pipelines or infrastructure to integrate with?                        | TC-03     |
| 8   | What is the desired notification delivery mechanism (email, in-app, both)?                         | NF-03     |
| 9   | How should the system handle the biannual Plan Application option vs. annual?                      | WF-01     |
| 10  | What are the specific UIE integration points for automated mismatch detection?                     | VE-01     |

---

## Appendix A: Form Inventory

| Form Name                              | Track           | Phase | Type       | Complexity |
| -------------------------------------- | --------------- | ----- | ---------- | ---------- |
| CSBG Tribal Plan and Application       | Tribal          | I     | Pre-award  | Medium     |
| CSBG Tribal Annual Report              | Tribal          | I     | Post-award | High       |
| CSBG Tribal Annual Report (Short Form) | Tribal          | I     | Post-award | Low        |
| CSBG Eligible Entity List              | State/Territory | II    | Reference  | Low        |
| CSBG State and Territory Plan          | State/Territory | II    | Pre-award  | High       |
| CSBG Annual Report 3.0                 | State/Territory | II    | Post-award | Very High  |

### Annual Report 3.0 Modules

| Module | Title                          | Completed By        | Content                                     |
| ------ | ------------------------------ | ------------------- | ------------------------------------------- |
| 1      | State/Territory Administration | State lead agencies | State administration of CSBG funding        |
| 2      | Eligible Entity Administration | Eligible entities   | Spending on services, capacity, admin costs |
| 3      | Individual and Family Level    | Eligible entities   | Services, demographics, outcomes            |
| 4      | Community Level                | Eligible entities   | Community strategies and results            |

---

*This PRD is derived from PWS ADMIN/OCS/CSBG/CSFEER v2 (Rev 2, August 25, 2025). Requirements are subject to change based on discovery, user research, and agile prioritization.*
