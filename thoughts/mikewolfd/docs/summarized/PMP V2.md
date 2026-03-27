# PMP V2 - Synthesized Analysis

**Summary:** The PMP V2 (Oct 2025) formalizes the 12-month delivery plan for CORE (the public-facing name for CSFEER), targeting 3 CSBG Tribal forms with a soft launch to 10-12 tribes at Month 9. It reveals several engineering-relevant details not in core context: the API layer is described as read-only for ACF staff, internal staff auth is undecided, ECS (not EKS) is the container target, and the ATO process runs parallel to development through Month 12.

---

## Naming Discrepancy

The PMP consistently uses **"Community Outcomes Reporting Engine (CORE)"** as the product name, while the codebase uses **CSFEER**. This may be an external-facing vs. internal distinction, or the name may have changed between PMP authoring (Oct 2025) and current development.

## MVP Scope Details (Additions to Core Context)

- **3 specific forms:** Tribal Plan/Application, Tribal Annual Report, Tribal Annual Report (Short Form). Core context mentions "Tribal Plan + Tribal Annual Report (Modules 1-3 combined)" -- the short form variant is an additional form not mentioned.
- **Role-based permissions:** Contributor, Approver, Viewer (3 roles, not elaborated in core context).
- **Notifications:** Email and in-app for availability, deadlines, confirmations.
- **Browser support:** Latest 2 versions of Chrome, Firefox, Safari, Edge.
- **Concurrent users target:** 200+ simultaneous during peak.
- **Adoption target:** 75% of tribal organizations within Year 1.

## Out of Scope (MVP)

- Low-code/no-code form builder (post-Year 1).
- State/Territory forms (Phase II).
- Advanced analytics dashboards (beyond CSV/API).
- SmartSheets integration (future ingestion API).
- Historical data import (TBD on data availability).
- Legacy system retirement (post Phase III).

## Tech Stack: Discrepancies and Additions

| Topic                   | PMP V2 Says                                     | Codebase Reality                            | Notes                                              |
| ----------------------- | ----------------------------------------------- | ------------------------------------------- | -------------------------------------------------- |
| API layer               | Django REST Framework (read-only for ACF staff) | Django Ninja                                | DRF is not used; Ninja is the actual API framework |
| Container orchestration | Amazon ECS                                      | Helm charts in `devops/` suggest Kubernetes | Helm is a K8s tool, contradicts ECS claim          |
| Internal staff auth     | TBD (Okta or AD, awaiting ACF decision)         | Mock OAuth in dev                           | Flagged as HIGH impact blocker, Month 1 target     |
| Project management      | Jira + GitHub Projects                          | GitHub Projects visible                     | Jira may be used on the government side            |
| PDF export              | HTML-to-PDF via headless Chrome                 | Not yet confirmed in code                   | Implementation detail to note                      |
| Component library       | "USWDS Crispy Forms" + Cotton                   | django-cotton only                          | Crispy Forms not observed in codebase              |

## Infrastructure and Deployment

- **Cloud:** AWS GovCloud (FedRAMP certified, ACF standard).
- **IaC:** Terraform (already in `devops/`).
- **CI/CD:** GitHub Actions.
- **Repo ownership:** Currently Focus Consulting fork; transfers to HHS/ACF post-development.

## Security and Compliance Requirements

- **FISMA Moderate** classification with NIST SP 800-53 Moderate baseline.
- **FedRAMP Moderate** for CSP (shared responsibility model).
- **Zero Trust** per EO 14028: identity verification, least privilege, device posture, network segmentation, encrypted comms.
- **FIPS 140-2** encryption at rest and in transit.
- **Incident response SLAs:** Critical <1hr, High <4hrs, Medium <24hrs, Low <72hrs.

## ATO Timeline (Parallel to Development)

| Phase          | Months | Activities                                     |
| -------------- | ------ | ---------------------------------------------- |
| Planning       | 1-2    | Categorization, control selection, SSP outline |
| Implementation | 3-8    | Controls, SSP, evidence, security testing      |
| Assessment     | 9-12   | 3PAO assessment, pen test, SAR, POA&M          |
| Authorization  | 12-13  | Risk determination, AO decision                |

ATO certification is the #1 risk (probability x impact = 0.45). Early ISSO engagement and staging environment for security training are key mitigations.

## Schedule: Key Dates

| Milestone                      | Month | Notes                                              |
| ------------------------------ | ----- | -------------------------------------------------- |
| Discovery complete             | 2     | Delivers research report + product strategy        |
| Design validation              | 5     | Wireframes, prototypes, architecture finalized     |
| MVP complete                   | 8     | All 3 forms, validation engine, exports, Login.gov |
| Pilot launch                   | 9     | 10-12 tribal orgs, white-glove support             |
| ATO + full rollout             | 12    | Wave-based onboarding of remaining orgs            |
| Continuous dev (if extended)   | 10-15 | Post-MVP features                                  |
| Transition out (if applicable) | 16-18 | 90-day knowledge transfer                          |

## Stage Gates (Go/No-Go Decisions)

- **Discovery Gate (M2):** Research quality, strategy, architecture feasibility.
- **MVP Gate (M8):** Functional completeness, security, performance, 508 compliance.
- **Pilot Gate (M9):** Stability, feedback integration, ATO package readiness.
- **Continuous Dev Gate (M15):** Adoption metrics, scalability, sustainability.

## Quality and Performance Targets

- **Test coverage:** >80%.
- **Sprint completion:** >85%.
- **Bug resolution:** <2 days.
- **Form completion time target:** <25 minutes.
- **First-pass validation rate:** >90%.
- **Support volume target:** <60 tickets/month.
- **Processing cost target:** <$50/form.
- **Page load:** <3s on 4G (3G testing also required).
- **Availability:** 99.5% during business hours.

## Staffing

- **Core team (M1-12):** PM, Tech Lead, Product Manager, UX Lead, 2 Senior Full-Stack Devs (6 FTE).
- **Surge team (M4-9, M13-15):** 2 additional Devs, 0.5 Security Specialist, 0.25 Accessibility Specialist.
- **Training requirement:** 40+ hours/person/year.

## Tribal Engagement Plan

- **Tribal Advisory Group:** 6-8 representatives, geographically diverse, formed in Months 1-6.
- **Site visits:** 8-10 planned during discovery.
- **Pilot cohort:** 10-12 orgs with weekly check-ins tapering to bi-weekly.
- **Rollout:** Wave-based with parallel operations (old PDF + new system simultaneously).

## Open Technical Unknowns (as of PMP authoring)

1. ACF internal auth system for API access (HIGH, target M1).
2. ACF AWS deployment patterns/constraints (HIGH, target M1).
3. ATO process timeline and specific requirements (HIGH, target M2).
4. Legacy data location, format, import requirements (MEDIUM, target M3).

## Transition and Knowledge Transfer

- GitHub repo + all infrastructure assets transfer to HHS/ACF.
- 90-day transition-out plan: Month 1 doc audit, Month 2 training (recorded), Month 3 parallel ops and validation.
- Living documentation: auto-generated code/API/infra docs, PR-required doc updates.
- Open-source contributions planned: USWDS Crispy Forms for Django, USWDS Cotton component framework.
