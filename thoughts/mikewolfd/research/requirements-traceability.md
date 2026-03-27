# Requirements Traceability: MATRIX.md vs. Codebase vs. Jira

> **Purpose:** Maps every MATRIX requirement to implementation status and Jira ticket coverage.
> **Sources:** [MATRIX.md](MATRIX.md) (requirements), [csfeer-architectural-review.md](csfeer-architectural-review.md) (implementation assessment), [.beads/issues.csv](../../../.beads/issues.csv) (Jira import)
> **Extracted from:** csfeer-architectural-review.md § Feature Matrix (2026-02-17 assessment)
> **Jira mappings added:** 2026-03-05

## Status Key

| Symbol | Meaning |
|--------|---------|
| ✅ | Implemented and functional |
| ⚠️ | Partial — core mechanism exists but incomplete |
| 🐛 | Implemented but broken or unsafe |
| ❌ | Not implemented |
| 🔮 | Post-MVP / explicitly deferred |

## Jira Column

Stateless `bd-XXX` references only — no status mirroring. Check `.beads/issues.csv` or `bd show <id>` for current status. Epic references noted with `(epic)`. `—` means no ticket covers this requirement.

---

## 1. Form Engine Core (FE)

### Field Types & Data Entry

| ID | Requirement | Status | Jira | Evidence |
|----|-------------|--------|------|----------|
| FE-01 | Manual data entry: open fields | ✅ | bd-427 (epic), bd-18, bd-210, bd-233 | `ACFFieldsMeta` generates all standard Django field types with ACF prefix |
| FE-02 | Auto-calculated fields | ✅ | bd-55, bd-89 | `CalculatedCurrency/Integer/DecimalField`; server-side sum + client-side `updateCalculatedFields()` |
| FE-03 | Pre-population: cross-form data linking | ❌ | — | `form_start` creates blank entries; no cross-form population mechanism |
| FE-04 | Conditional fields and branching | ✅ | bd-86, bd-114 | `ACFFieldFilterField` drives `fields_to_exclude`; `remove_nodes_with_excluded_fields()` prunes layout tree |
| FE-05 | One-to-many response types | ❌ | — | No FormSet, repeatable group, or dynamic field mechanism |
| FE-06 | File attachment fields | ⚠️ | bd-399 | `ACFFileField` exists; USWDS `file_input` available; not used in any deployed form, no storage backend |
| FE-12 | Reduce variability from custom plans | ⚠️ | bd-332 | Standardized schemas enforce structure for tribal forms; state/territory forms not yet built |

### Validation

| ID | Requirement | Status | Jira | Evidence |
|----|-------------|--------|------|----------|
| FE-20 | Flexible validation rules engine | ✅ | bd-114, bd-240, bd-458 | Pydantic+Django form validation with custom field validators and `fields_to_exclude` logic |
| FE-21 | Hard errors and warning validations | ⚠️ | — | Hard errors via Django form validation; no warning/notification tier |
| FE-22 | Field, field-group, and form-level validation | ⚠️ | — | Field-level and form-level exist; no explicit field-group validation |
| FE-23 | Automated validation during form completion | 🐛 | bd-114, bd-458 | Validation logic exists but commented out in `form_finalize.py:48` — forms submit even if invalid |
| FE-24 | Automated comparison to integration data (SAM.gov) | ❌ | — | No SAM.gov API, UEI field, or external data validation |
| FE-25 | Validation timing (during entry vs. review page) | ⚠️ | bd-114, bd-240 | Validates per-page on POST; review page shows errors via session flag; not inline during typing |

### Version Control & Data Integrity

| ID | Requirement | Status | Jira | Evidence |
|----|-------------|--------|------|----------|
| FE-30 | Multiple simultaneous form versions | ✅ | bd-222 | `SemVerField` on `FormDefinition`, `version_number` on `FormEntry` + `unique_together` constraints + `is_active` flag |
| FE-31 | Robust version history for federal staff | ✅ | — | Two-tier audit: `FormAuditTrail` + `FormAuditDetail`; `FormSnapshotView` reconstructs state |
| FE-32 | Historical comparison for recipients | ⚠️ | — | `FormSnapshotView` shows past state; no side-by-side diff view |

### Form Builder

| ID | Requirement | Status | Jira | Evidence |
|----|-------------|--------|------|----------|
| FE-40 | Low-code/no-code form builder | 🔮 | — | Post-year-1 per MATRIX |
| FE-41 | Sandbox/testing space for form builder | 🔮 | — | Post-year-1 |
| FE-42 | Faster form design iteration | ⚠️ | — | `load_initial_forms` + `dump_schema` commands; still requires developer involvement |

### Implementation Decisions

| ID | Decision | Status | Jira | Evidence |
|----|----------|--------|------|----------|
| FE-08 | Interview-style page-by-page POST flow | ✅ | bd-54, bd-85 | `form_edit.py` step/page navigation with `?step=N&page=N` query params |
| FE-09 | JSON field storage for form data | ✅ | bd-427 (epic) | `FormEntry.data = JSONField()` |
| FE-10 | Pydantic schemas as single source of truth | ✅ | bd-427 (epic) | `form_manager/schema/` defines UI structure, Django form classes, and validation |
| FE-11 | FormDefinition links to Python schema class | ✅ | bd-427 (epic) | `schema_class` string field dynamically imported |
| FE-33 | Status lifecycle: draft → submitted → amended → archived | ⚠️ | — | Model statuses exist; no view transitions to "amended" |
| FE-34 | Audit trail for all form actions | ✅ | — | `FormAuditTrail` + `FormAuditDetail` with field-level diffs and state reconstruction |
| FE-36 | Short form variant derived from long form | ✅ | bd-60 (epic) | `TribalShortFormFields` and `TribalLongFormFields` are separate schemas |
| FE-37 | Cross-form pre-population (Plan ← AR) | ❌ | — | No implementation; see FE-03 |
| FE-38 | Periodic auto-save every 30-60s | ❌ | bd-37, bd-54, bd-235 | Save only on explicit form POST; no JS timers or debounce |
| FE-43 | Screener flow / form routing after login | ❌ | bd-332 (epic) | `form_list` shows all definitions as flat cards; no eligibility routing |
| FE-44 | Client-side caching (IndexedDB/localStorage) | ❌ | bd-459 | No browser storage APIs, no service worker |
| FE-45 | Connection state indicators | ❌ | bd-459 | No "Saved"/"Connection lost"/"Reconnected" UI |
| FE-46 | UEI as cross-form pre-population key | ❌ | — | No UEI field on `OrganizationProfile` |
| FE-47 | Concurrent edit conflict handling | ❌ | — | Boolean `is_locked` only; no optimistic locking |

---

## 2. Form Submission Workflow (WF)

| ID | Requirement | Status | Jira | Evidence |
|----|-------------|--------|------|----------|
| WF-01 | Auto-create forms with pre-populated data | ❌ | — | `form_start` creates blank entries on user click; no schedule-driven creation |
| WF-02 | Show trends over time using previous year data | ❌ | — | No year-over-year comparison |
| WF-04 | Recipients can unsubmit forms | ❌ | bd-10 (epic) | "amended" status exists but no view transitions from submitted back to draft |
| WF-05 | Recipients can submit revisions | ❌ | — | No amend/revise view |
| WF-06 | Submit a form (distinct action) | 🐛 | — | `form_finalize` exists but validation commented out — always succeeds |
| WF-09 | Multi-step federal review and approval | 🔮 | — | Out of MVP scope |
| WF-11 | Save progress and return later | ✅ | bd-37, bd-54 | Forms save on page navigation POST; draft status preserved |
| WF-12 | Previously submitted data available | ⚠️ | — | Own entry loads on return; no cross-submission pre-population |
| WF-13 | Real-time alerts and notifications | 🔮 | — | Out of MVP scope |
| WF-14 | Deadline-aware notifications | 🔮 | — | No notification infrastructure |
| WF-15 | Multi-user form collaboration and routing | 🔮 | — | Out of MVP scope |
| WF-17 | Tracking and collaboration visibility | ❌ | — | No cross-role visibility |
| WF-18 | March 31 statutory submission deadline | ❌ | — | No deadline enforcement in application |

---

## 3. Authentication & Security (AS)

| ID | Requirement | Status | Jira | Evidence |
|----|-------------|--------|------|----------|
| AS-01 | Authentication with Login.gov | ❌ | bd-111 (epic), bd-13, bd-24, bd-35 | OIDC configured for Keycloak only; Login.gov deferred per AS-18 |
| AS-03 | Gov users via login.acf.gov (Okta) | ❌ | bd-111 (epic), bd-474, bd-476 | No Okta configuration; Keycloak dev mock only |
| AS-05 | Auth Code Flow with PKCE + client secret | ✅ | bd-35, bd-46, bd-56 | `django-oauth2-authcodeflow` handles PKCE; server-side tokens |
| AS-06 | Keycloak for local dev | ✅ | bd-473 | Docker Compose with realm `csfeer`, CSV user seeding |
| AS-07 | Role-to-group mapping from JWT claims | ✅ | bd-477 | `extend_user_with_roles` maps `realm_access.roles` to Django groups |
| AS-08 | Role mappings (admin/staff/superuser) | ✅ | bd-477 | `csfeer_admin` → staff+superuser; wildcard creates groups |
| AS-10 | Auto-provision user + org on first login | ✅ | bd-476 | `EmailOIDCAuthenticationBackend` creates user, profile, org, membership |
| AS-11 | Group memberships re-synced every login | ✅ | bd-477 | `user.groups.clear()` runs every login; groups rebuilt from token |
| AS-14 | ATO within 18 months | ⚠️ | bd-438 (epic), bd-188, bd-469, bd-472 | Security patterns in code; ATO docs in progress |
| AS-18 | MVP basic sessions (Login.gov deferred) | ✅ | bd-473 | Current state: Django sessions via Keycloak OIDC |

---

## 4. Integration & Data (DA)

| ID | Requirement | Status | Jira | Evidence |
|----|-------------|--------|------|----------|
| DA-01 | Read API for forms/submissions/bulk data | ⚠️ | bd-31 | 7 read-only GET endpoints via Django Ninja; no pagination, no rate limiting |
| DA-02 | Write API for pre-populated data import | ❌ | — | API is read-only; no POST/PUT/PATCH |
| DA-03 | Data exports via API, CSV, and human-readable | ⚠️ | — | API returns JSON; PDF exists; no CSV export |
| DA-04 | Export individual submissions as PDFs | 🐛 | bd-36, bd-49 | WeasyPrint works; synchronous in request cycle — blocking/DOS risk |
| DA-05 | Public-access links to submission portions | ❌ | — | No public/shareable link mechanism |
| DA-06 | Comprehensive API documentation | ✅ | bd-31 | Django Ninja auto-generates OpenAPI at `/api/v1/docs` |
| DA-07 | Real-time data access without perf degradation | ❌ | — | No read replica, caching, or query optimization |
| DA-14 | Staff export, review, and correct data errors | ❌ | — | Django admin only |
| DA-15 | Conditional-logic-aware PDF export | ❌ | — | PDF renders all sections regardless of conditional logic |

---

## 5. Accessibility & Design (AD)

| ID | Requirement | Status | Jira | Evidence |
|----|-------------|--------|------|----------|
| AD-01 | Section 508 WCAG AA compliance | ⚠️ | bd-471 (epic), bd-103, bd-461 | USWDS components accessible; no automated a11y testing |
| AD-02 | USWDS as design system | ✅ | bd-1 (epic) | `django-cotton-uswds` with 93 components; USWDS 3.13+ |
| AD-05 | Clear progress in multi-step process | ✅ | bd-85, bd-450 | USWDS step indicator shows complete/current/incomplete |
| AD-06 | Plain, familiar language | ⚠️ | — | Present in templates; no systematic enforcement |
| AD-09 | Low-bandwidth/rural support | ❌ | bd-459 | No offline capability, no auto-save, no client caching |
| AD-13 | In-context field guidance | ⚠️ | — | `ACFFieldMixin` adds `description`; no companion doc integration |

---

## 6. Permissions & User Management (PM)

| ID | Requirement | Status | Jira | Evidence |
|----|-------------|--------|------|----------|
| PM-01 | Flexible permissions: read, write, export | ✅ | bd-6, bd-477 | Org-level admin/editor/viewer with permission checks |
| PM-02 | Self-service user management | ❌ | bd-108, bd-475 | `users/views.py` is empty; Django admin only |
| PM-03 | Hierarchical administration (sub/state/fed) | ❌ | — | Single flat `OrganizationProfile`; no hierarchy |
| PM-04 | Minimum permission levels per tier | ⚠️ | — | Org-level exists; no federal-tier or cross-org permissions |
| PM-05 | Varying permission levels | ⚠️ | — | View/edit/submit mapped to viewer/editor/admin; no export-specific perms |
| PM-08 | Authorization and access control | ⚠️ | bd-6 | Org-scoped authz works; out of MVP scope per MATRIX but partially done |

---

## 7. Performance & Reliability (PR)

| ID | Requirement | Status | Jira | Evidence |
|----|-------------|--------|------|----------|
| PR-02 | Scalable to 1,100 recipients + 75 staff | ❌ | — | No load testing, no pagination, sync PDF blocks workers |
| PR-04 | Real-time resource utilization monitoring | ❌ | bd-2 (epic), bd-102, bd-122 | No APM or metrics collection |
| PR-05 | Performance monitoring (response time, latency) | ❌ | bd-2 (epic) | File-based Django logging only |
| PR-10 | 24/7 operational availability | ⚠️ | — | HPA configured (min 2 / max 10) but miswired; no health check endpoint |
| PR-11 | ≥200 concurrent users | ❌ | — | No load testing; default gunicorn config |
| PR-13 | Modern browser support | ✅ | — | Standard Django + Alpine.js + USWDS |
| PR-14 | Reliable despite poor connectivity | ❌ | bd-459 | No auto-save, no client caching, no offline resilience |
| PR-15 | Test coverage >80% | ❌ | bd-481, bd-9, bd-33, bd-38, bd-0fea | ~51 unit + ~21 E2E tests; no coverage reporting; zero API tests |

---

## 8. User Personas & Roles (UP)

| ID | Requirement | Status | Jira | Evidence |
|----|-------------|--------|------|----------|
| UP-01 | Three grantee role tiers (Approver/Contributor/Viewer) | ⚠️ | bd-15, bd-21, bd-108 | Admin/editor/viewer exist; naming differs from persona spec |
| UP-02 | SF-424M cross-referencing guidance | ❌ | — | No SF-424M references in schemas |
| UP-03 | Transmittal letter/attestation artifact | ❌ | — | No attestation model or signature capture |
| UP-04 | Portfolio dashboard for OCS staff | ❌ | bd-72, bd-221 (epic) | No cross-org view; staff see same interface as grantees |
| UP-05 | Batch review & structured export | ❌ | — | No bulk operations or cross-grantee comparison |
| UP-06 | Visual diff ("what changed from last year") | ❌ | — | Audit captures within-submission changes; no year-over-year |
| UP-07 | Simplified summary view for leadership | ❌ | — | No summary/dashboard view |
| UP-08 | Unified admin console | ❌ | — | Django admin only |

---

## 9. MVP Acceptance Criteria (AC)

| ID | Criterion | Status | Jira | Evidence |
|----|-----------|--------|------|----------|
| AC-01 | All three tribal forms with validation + save/submit | ⚠️ | bd-59 (epic), bd-60 (epic), bd-61 (epic) | Long + Short Form built; Tribal Plan not yet; validation commented out |
| AC-02 | Login.gov working for all pilot users | ❌ | bd-111 (epic) | Keycloak only; Login.gov deferred (contradicts this criterion) |
| AC-03 | CSV + PDF export functional | ⚠️ | bd-36, bd-49 | PDF works (synchronous); no CSV export |
| AC-04 | At least 10 tribal orgs submit during pilot | ❌ | — | Pre-pilot; no production deployment |

---

## 10. Infrastructure & Technology (IT)

| ID | Decision | Status | Jira | Evidence |
|----|----------|--------|------|----------|
| IT-01 | Python 3.12, Django 6.0+ | ✅ | bd-460 (epic) | `uv.lock` resolves Django 6.0; Python 3.12 target |
| IT-02 | PostgreSQL (Aurora RDS) | ✅ | — | Terraform defines Aurora PostgreSQL 16.6 with IAM auth |
| IT-03 | AWS ECS (not Kubernetes) | ✅ | — | **Superseded — moved to EKS/Kubernetes.** Helm charts, ArgoCD, EKS Terraform all present |
| IT-04 | Alpine.js 3.15+ | ✅ | — | Alpine.js + mask plugin in webpack bundle |
| IT-05 | USWDS 3.13+ | ✅ | bd-1 (epic) | `django-cotton-uswds` with 93 components |
| IT-06 | Django Ninja for REST APIs | ✅ | bd-31 | 7 endpoints at `/api/v1/` |
| IT-07 | WeasyPrint for PDF generation | ✅ | bd-36, bd-49 | Synchronous in `FormDownloadPDFView` |
| IT-08 | Django Cotton for template components | ✅ | bd-57 | `django_cotton_uswds` app with pattern library |
| IT-09 | Keycloak for local dev auth | ✅ | bd-473 | Docker Compose with realm `csfeer`, CSV user seeding |

---

## 11. Form Inventory (FI)

| ID | Form Name | Status | Jira | Notes |
|----|-----------|--------|------|-------|
| FI-01 | CSBG Tribal Plan and Application | ❌ | bd-61 (epic), bd-65, bd-66, bd-68, bd-69, bd-70, bd-230 | Design done; schema not yet built. Target Mar 31. |
| FI-02 | CSBG Tribal Annual Report (Long Form) | ✅ | bd-59 (epic), bd-16, bd-39, bd-47, bd-63, bd-104 | Schema exists and functional |
| FI-03 | CSBG Tribal Annual Report [Short Form] | ✅ | bd-60 (epic) | Schema exists and functional |

---

## 12. Success Criteria (SC)

| ID | Criterion | Status | Jira | Evidence |
|----|-----------|--------|------|----------|
| SC-01 | 20+ tribal orgs submit via CORE | ❌ | — | Pre-pilot |
| SC-02 | ≥80% report easier than PDFs | ❌ | bd-48, bd-92, bd-104, bd-105 | Usability research planned; no survey mechanism built |
| SC-03 | 100% Section 508 compliance | ⚠️ | bd-471 (epic) | USWDS accessible; no automated verification |
| SC-04 | Zero OCIO security findings | ⚠️ | bd-438 (epic), bd-ha7h, bd-hze3, bd-octr | Security scans run; ATO in progress |
| SC-05 | Architecture docs complete for Phase II | ❌ | — | Not started |
| SC-06 | Platform supports simple and complex forms | ⚠️ | bd-59 (epic), bd-60 (epic) | Two tribal forms demonstrate spectrum |
| SC-07 | First measurable baseline for Tribal reporting | ❌ | — | Requires day-one telemetry (DL-15) |

---

## Coverage Summary

| Category | Total | ✅ | ⚠️ | 🐛 | ❌ | 🔮 | Has Jira | No Jira |
|----------|-------|---|---|---|---|---|----------|---------|
| Form Engine (FE) | 28 | 11 | 6 | 1 | 10 | 0 | 20 | 8 |
| Workflow (WF) | 13 | 1 | 1 | 1 | 6 | 4 | 2 | 11 |
| Auth & Security (AS) | 10 | 7 | 1 | 0 | 2 | 0 | 10 | 0 |
| Integration & Data (DA) | 9 | 1 | 2 | 1 | 5 | 0 | 3 | 6 |
| Accessibility (AD) | 6 | 2 | 3 | 0 | 1 | 0 | 4 | 2 |
| Permissions (PM) | 6 | 1 | 3 | 0 | 2 | 0 | 4 | 2 |
| Performance (PR) | 8 | 1 | 1 | 0 | 6 | 0 | 4 | 4 |
| User Personas (UP) | 8 | 0 | 1 | 0 | 7 | 0 | 3 | 5 |
| MVP Acceptance (AC) | 4 | 0 | 2 | 0 | 2 | 0 | 3 | 1 |
| Infrastructure (IT) | 9 | 8 | 0 | 0 | 1 | 0 | 6 | 3 |
| Form Inventory (FI) | 3 | 2 | 0 | 0 | 1 | 0 | 3 | 0 |
| Success Criteria (SC) | 7 | 0 | 2 | 0 | 5 | 0 | 4 | 3 |
| **Totals** | **111** | **34** | **22** | **3** | **48** | **4** | **66** | **45** |

**Read:** 66 of 111 requirements have at least one Jira ticket. The 45 without coverage cluster in Workflow (11), User Personas (5), Integration/Data (6), and Performance (4) — the same areas the gap analysis flagged as weakest.

---

## Notable Gaps (No Jira Coverage)

Requirements with no ticket coverage that are **Blocking** or **High** severity per [mvp-gap-analysis.md](mvp-gap-analysis.md):

| ID | Requirement | Severity | Area |
|----|-------------|----------|------|
| FE-21 | Warning-tier validation | Medium | Validation |
| FE-47 | Concurrent edit handling | Low | Form Engine |
| DA-03 | CSV export | **Blocking** | MVP Acceptance (AC-03) |
| WF-04 | Unsubmit capability | **High** | Workflow |
| WF-05 | Revision submission | **High** | Workflow |
| WF-06 | Submit action (validation broken) | **Blocking** | Workflow |
| PM-02 | Self-service user management | **High** | Permissions |
| PR-02 | Scalability / load testing | **High** | Performance |
| PR-11 | 200 concurrent users | **High** | Performance |
