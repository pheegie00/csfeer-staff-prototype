# Product Spec -- CORE (CSFEER) Tribal MVP (v2.0, 2025-11-17)

## Summary

Product specification for the Tribal MVP scope: digitize three OMB-approved Tribal CSBG forms with low-connectivity resilience, validation, pre-population, and role-based collaboration. The document establishes concrete success metrics (75% digital adoption, 3-second load/save, zero data loss) and a 90-day baseline telemetry plan. Current Tribal reporting takes 12-20 days per form submission; the target is 3-7 days initially, aspirationally under one hour.

---

## Forms In Scope (MVP)

- **Tribal Plan & Application** (pre-award)
- **Tribal Annual Report** (post-award, full)
- **Tribal Annual Report Short Form** (post-award, abbreviated)

No other forms are in scope. State/Territory forms, CSBG Annual Report 3.0, and Eligible Entity List are explicitly excluded.

> **Clarification vs. core context:** Core context mentions "Modules 1-3 combined" for Tribal track but does not name the Short Form as a distinct third form. The spec treats it as a separate OMB-approved form requiring its own implementation.

## User Roles

| Role                             | Capabilities                                                                         |
| -------------------------------- | ------------------------------------------------------------------------------------ |
| Authorized Official              | Must appear on all forms (SF-424 linkage); inputs data that pre-populates into forms |
| Grant Administrator              | Primary operational role (not further defined)                                       |
| Tribal Contributor               | Data entry                                                                           |
| Tribal Approver                  | Review, attest, submit                                                               |
| Tribal Viewer                    | Read-only (leadership / council sign-off)                                            |
| OCS Program Officer              | Review submissions, export, API access                                               |
| Administrator (ACF + Contractor) | Account management, system monitoring, audit logs                                    |

> **Addition vs. core context:** Core context lists user counts (~66 Tribes, ~75 federal staff) but does not enumerate the role taxonomy. The Authorized Official / SF-424 linkage and the Viewer role for council sign-off are product-specific details relevant to RBAC implementation.

## Screener Flow

Users encounter a screener after login that determines which form they should fill out (or presents the best form based on answers). This is a routing mechanism before form entry begins.

> **Addition vs. core context:** The screener concept is not mentioned in core context. It implies a form-selection UI component that must be built and maintained.

## Pre-population via UEI

Authorized Official inputs data (potentially keyed by UEI -- Unique Entity Identifier) that is then pre-populated across forms. UEI is called out as a potential cross-form identifier.

> **Addition vs. core context:** Core context mentions "pre-population from prior years." This spec adds that the Authorized Official's data entry and UEI lookup are potential pre-population mechanisms, not just year-over-year carryforward.

## Low-Connectivity Requirements

Contract requires **resilient behavior**, explicitly NOT full offline editing.

- Auto-save when connected (incremental)
- **IndexedDB / localStorage** for temporary browser-side caching during connection drops
- Sync cached data on reconnection
- Three status indicators: "Saved", "Connection lost -- your work is stored locally", "Reconnected -- sync successful"
- Target: zero data loss in rural/intermittent environments

> **Engineering implication:** The spec prescribes specific browser storage APIs (IndexedDB/localStorage) and three distinct connection state indicators. This constrains frontend architecture -- a service worker or connection-monitoring layer with a local persistence strategy is required.

## Out-of-System Touchpoints

MVP must accommodate items that live outside the digital form, such as PDFs and signed documents that users upload as part of the application package. File upload (FR7) supports this.

> **Addition vs. core context:** Core context does not mention out-of-system touchpoints or the need to handle externally-signed documents uploaded alongside digital form data.

## Nonfunctional Requirements (Specifics)

| Requirement            | Target                                                 |
| ---------------------- | ------------------------------------------------------ |
| Form load/save latency | <= 3 seconds on typical 4G                             |
| Concurrent users       | >= 200                                                 |
| Uptime                 | >= 99.5% (excl. maintenance)                           |
| Security               | FISMA Moderate, FedRAMP hosting, FIPS 140-2 encryption |
| Browser support        | Chrome, Firefox, Edge, Safari (modern versions)        |
| Responsive design      | Tablets and laptops (NOT phones)                       |

> **Clarification vs. core context:** The "4G" benchmark for latency testing is specific. Responsive design targets tablets/laptops, not phones -- consistent with the non-goal of mobile apps.

## Success Metrics (MVP)

| Category     | Metric                                          | Target   |
| ------------ | ----------------------------------------------- | -------- |
| Adoption     | Tribal orgs submitting digitally                | >= 75%   |
| Adoption     | Pilot orgs with successful submission           | 100%     |
| Data quality | Submissions passing validation without OCS help | >= 90%   |
| Data quality | Errors resolved without OCS intervention        | >= 85%   |
| Data quality | Reduction in OCS follow-up emails               | >= 30%   |
| Performance  | Load/save latency                               | <= 3s    |
| Performance  | Uptime                                          | >= 99.5% |
| Resilience   | Autosave success rate                           | >= 98%   |
| Resilience   | Data loss                                       | 0%       |
| UX           | User satisfaction                               | >= 4/5   |
| UX           | Help desk tickets per org                       | <= 1     |

## OKR Targets (Beyond MVP)

- Reduce submission time from 12-20 days to 3-7 days (aspirational: < 1 hour)
- 70% component reuse across forms
- New form onboarding <= 6 weeks
- OCS review time reduced >= 25% (long-term: >= 50%)
- Year-over-year data consistency increase >= 20%
- Usability testing with >= 9 Tribal orgs (noted as "max" -- implies limited pool of willing participants)
- Incorporate >= 80% of Tribal feedback into UX
- API uptime >= 99.9% (stricter than system uptime)
- Scale to 5-10x current user base

## 90-Day Baseline Telemetry Plan

First 90 days post-launch focus on establishing measurement baselines across four dimensions:

1. **User interaction:** sessions per submission, time per section, autosave frequency/success, sync patterns on reconnect
2. **Submission quality:** validation error types/frequency, resolution rates, submit-unsubmit cycles
3. **Performance:** load times, save/sync times, export performance
4. **Operational:** ticket volume, time-to-resolution, OCS review time

> **Engineering implication:** Requires instrumentation from day one -- event tracking for autosave, section timing, validation error categorization, and connectivity state transitions. This is not a post-MVP concern.

## Legacy Workflow Burden (Baseline)

12-20 days per form submission breakdown:
- 1-3 days: locating correct forms/guidance
- 5-10 days: internal data gathering
- 3-5 days: offline drafting across multiple files
- 2-5 days: leadership review and signatures
- 1-2 days: OLDC upload and formatting
- 1-5 days: corrections and resubmissions

Estimated 1,800 hours total annual burden across Tribal organizations.

## V1 Post-MVP Enhancements

- Improved offline capability (beyond MVP's resilient caching)
- Full submission dashboards for OCS
- Batch export tools
- Enhanced reporting UX
- Expanded support materials
- Better analytics for ACF staff

## Risks

- **Government shutdown** delays ATO/governance (flagged for January specifically)
- **Tribal connectivity variability** complicates testing -- need representative low-bandwidth test environments
- **Unclear legacy data structures** for pre-population -- data mapping from OLDC/prior systems is unresolved
- **Submission attestation / signature workflow** lacks clarity -- how does council sign-off work digitally?
- **Scope creep** without change control
- **Policy interpretations** may alter form logic mid-development

## Dependencies

- Login.gov integration
- ACF internal auth for staff (separate from Login.gov)
- ACF AWS hosting environment and access patterns
- ATO timelines
- OMB-approved form definitions and policy interpretations
- OCS availability for validation logic review

> **Clarification vs. core context:** Dual auth paths are confirmed: Login.gov for Tribal users, ACF-approved SSO for federal staff. This matches the Okta-brokered architecture identified in the ITB kickoff analysis.
