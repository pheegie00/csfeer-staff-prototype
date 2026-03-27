# MVP Gap Analysis: CSBG Tribal Forms (Phase I)

> **Purpose:** Actionable gap analysis — what must be built for MVP, what exists, what's missing.
> **Sources:** [MATRIX.md](MATRIX.md) (requirements), [csfeer-architectural-review.md](csfeer-architectural-review.md) (implementation status), [requirements-traceability.md](requirements-traceability.md) (full req↔code↔Jira mapping)
> **Date:** 2026-03-05

---

## MVP Scope

Three tribal forms for ~66 end-user organizations:

| Form | Users | Build Status |
|------|-------|-------------|
| Tribal Annual Report (Long Form) — FI-02 | ~30 orgs (>$50k funding) | Schema exists |
| Tribal Annual Report [Short Form] — FI-03 | ~30 orgs (≤$50k funding) | Schema exists |
| Tribal Plan and Application — FI-01 | ~66 orgs | **Not yet built** |

The $50k funding threshold determines long vs. short form — mandatory based on allocation, not user choice.

## Done Criteria

From MATRIX AC-01 through AC-04 and SC-01 through SC-07:

| ID | Criterion | Status | Gap |
|----|-----------|--------|-----|
| AC-01 | All three tribal forms with validation + save/submit | ⚠️ | Tribal Plan not built; validation commented out in `form_finalize.py:48` |
| AC-02 | Login.gov working for pilot users | ❌ | Deferred per AS-18; conflicts with this criterion (see C-13 in MATRIX) |
| AC-03 | CSV + PDF export functional | ⚠️ | PDF works (synchronous/blocking); no CSV export |
| AC-04 | ≥10 tribal orgs successfully submit during pilot | ❌ | Pre-pilot; no production deployment |
| SC-01 | 20+ tribal orgs submit via CORE without reverting to PDFs | ❌ | Conflicts with AC-04 (10) and DL-11 (10-12) on pilot size |
| SC-02 | ≥80% of users report easier than PDFs | ❌ | No survey mechanism |
| SC-03 | 100% Section 508 compliance | ⚠️ | USWDS components accessible; no automated a11y testing |
| SC-04 | Zero OCIO security findings | ⚠️ | Strong security patterns; ATO docs in progress |
| SC-05 | Architecture docs complete for Phase II | ❌ | Not started |
| SC-06 | Platform supports both simple and complex forms | ⚠️ | Two tribal forms demonstrate complexity spectrum |
| SC-07 | First measurable baseline for Tribal reporting | ❌ | Requires day-one telemetry (DL-15) |

---

## Gap Analysis by Task Area

### 1. Form Engine Core

**What exists:** The form engine is the strongest part of the codebase. Pydantic+Django form fusion, recursive layout tree, conditional field exclusion, calculated fields, and audit trail are all implemented and well-designed.

**Gaps for MVP:**

| Gap | Requirements | Severity | Jira | Notes |
|-----|-------------|----------|------|-------|
| Tribal Plan form not built | FI-01 | **Blocking** | bd-61 (epic), bd-65, bd-70 | Third of three MVP forms; target Mar 31 |
| Validation commented out in finalize | FE-23, WF-06 | **Blocking** | — | `form_finalize.py:48` — forms submit even when invalid; no ticket |
| No warning-tier validation | FE-21 | Medium | — | All validation is blocking or nothing; PWS requires advisory warnings |
| No field-group validation | FE-22 | Low | — | Field-level and form-level exist; group-level gap |
| No auto-save | FE-38 | **High** | bd-235 | ⚠️ bd-37, bd-54 closed but only covered save-on-navigate, not periodic auto-save |
| No connection resilience | FE-44, FE-45 | **High** | bd-459 | No IndexedDB/localStorage, no connection state indicators; tribal users in rural/low-bandwidth areas |
| No screener/routing flow | FE-43 | Medium | bd-332 (epic) | Users see flat list of forms; no eligibility-based routing |
| No concurrent edit handling | FE-47 | Low | — | Boolean lock only; no optimistic locking; no ticket |

### 2. Submission Workflow

**What exists:** Save-and-resume works (WF-11). Draft status persists. Form data loads on return.

**Gaps for MVP:**

| Gap | Requirements | Severity | Jira | Notes |
|-----|-------------|----------|------|-------|
| No unsubmit capability | WF-04 | **High** | bd-10 (epic) | "amended" status exists in model but no view transitions back to draft |
| No revision submission | WF-05 | **High** | — | No amend/revise workflow; no ticket |
| No auto-creation from schedules | WF-01 | Medium | — | Users manually start forms; no reporting-schedule-driven creation |
| No year-over-year trends | WF-02 | Medium | — | No previous-year data comparison |
| No cross-submission pre-population | WF-12 | Medium | — | Own entry loads; no prior submission data |
| No deadline awareness | WF-18 | Low | — | March 31 statutory deadline not enforced |
| No tracking visibility | WF-17 | Low | — | No cross-role status visibility |

### 3. Authentication

**What exists:** OIDC via Keycloak works for dev. Role mapping, auto-provisioning, session management all functional. The OIDC abstraction layer (`django-oauth2-authcodeflow`) means the Keycloak→Okta/Login.gov switch is a configuration change, not a rewrite — the backend already handles Authorization Code Flow with PKCE and server-side token management.

**Current status (as of 2026-03-05):** Transition to ACF's NGSC environment is **in progress**. This is the gate to Okta and Login.gov integration — those services are managed within ACF's infrastructure, not something the team provisions independently. Conversations with ACF have happened; access is pending.

**Gaps for MVP:**

| Gap | Requirements | Severity | Jira | Notes |
|-----|-------------|----------|------|-------|
| Okta/Login.gov not yet wired | AS-01, AS-03 | **Blocked on ACF environment access** | bd-111 (epic), bd-13, bd-24 | NGSC transition in progress; Okta/Login.gov integration follows environment access |
| ATO documentation incomplete | AS-14, AS-15 | **Blocking** (for pilot) | bd-438 (epic), bd-188, bd-469, bd-472 | Target May 29, 2026; multiple artifacts in progress |
| Claim structure uncertainty | AS-07 | Medium | bd-477 | Will Okta tokens emit roles in `realm_access.roles` (Keycloak convention) or a different claim path? Backend may need updating once Okta token structure is known |

The auth gap is **not a code-readiness problem** — the OIDC plumbing is built. It's an environment-access dependency. The open risk is whether Okta's token claims match the Keycloak claim structure the backend currently expects (AS-07).

### 4. Data & Integration

**What exists:** PDF export via WeasyPrint. 7 read-only API endpoints. Auto-generated OpenAPI docs.

**Gaps for MVP:**

| Gap | Requirements | Severity | Jira | Notes |
|-----|-------------|----------|------|-------|
| No CSV export | DA-03, AC-03 | **Blocking** | — | Explicitly in MVP acceptance criteria; **no ticket** |
| Synchronous PDF generation | DA-04 | **High** | bd-49 | bd-36 closed (POC); bd-49 in_progress |
| No conditional-logic-aware PDF | DA-15 | Medium | — | Prints everything including non-applicable sections |
| API has no pagination | DA-01 | Medium | — | ⚠️ bd-31 closed but only covered scaffolding; pagination/rate-limiting never built |
| PII exposure via API | DA-01 | **High** | — | Full form data JSON, audit old/new values, org contact details exposed; no ticket |
| PII logged at INFO level | — | **Critical** | — | `form_manager/utils.py:193+` logs form data; no ticket |

### 5. Accessibility

**What exists:** USWDS 93-component library. Skip-nav, landmarks, ARIA labels. Step indicator for multi-page progress.

**Gaps for MVP:**

| Gap | Requirements | Severity | Jira | Notes |
|-----|-------------|----------|------|-------|
| No automated a11y testing | AD-01, SC-03 | **High** | bd-471 (epic), bd-103 | 100% 508 compliance is a success criterion; no axe-core or equivalent in CI |
| No low-bandwidth support | AD-09 | **High** | bd-459 | Full page POST on every navigation; no offline resilience |

### 6. Permissions

**What exists:** Org-level admin/editor/viewer roles with edit/submit/view permission checks.

**Gaps for MVP:**

| Gap | Requirements | Severity | Jira | Notes |
|-----|-------------|----------|------|-------|
| No self-service user management | PM-02 | **High** | bd-108, bd-475 | No user management UI; Django admin only |
| No organizational hierarchy | PM-03 | Medium | — | Flat org model; no sub-recipient/state/federal tiers |

### 7. Performance & Observability

**What exists:** Helm HPA configured (min 2 / max 10). Modern browser support. Aurora PostgreSQL with CloudWatch alarms.

**Gaps for MVP:**

| Gap | Requirements | Severity | Jira | Notes |
|-----|-------------|----------|------|-------|
| No telemetry/instrumentation | PR-04, PR-05, DL-15 | **High** | bd-2 (epic) | Day-one instrumentation required for 90-day baseline; nothing exists |
| No load testing | PR-02, PR-11 | **High** | — | No evidence system handles 200 concurrent users; no ticket |
| No test coverage reporting | PR-15 | Medium | bd-481, bd-9 | >80% target; tool installed but not configured |
| Gunicorn not tuned | PR-11 | Medium | — | Default worker config; no explicit worker/thread/timeout settings |

---

## Deployment Blockers

From the architectural review's "Deployment / Config Drift" section — the deploy artifacts in the repo likely don't work:

| Issue | Severity | Jira |
|-------|----------|------|
| Prod Docker image likely missing app code — only copies `./csfeer`, not `core/`, `users/`, `form_manager/` | **Critical** | bd-460 (epic) |
| Helm values/schema mismatch — templates reference different paths than values define | **Critical** | bd-460 (epic) |
| Ingress health check hits `/` which redirects to OIDC login (not 200) | **High** | — |
| Logging writes to `/app/logs/*.log` but K8s root filesystem is read-only, no writable volume mounted | **High** | — |
| SECRET_KEY env var name mismatch between Helm and Pydantic settings | **High** | — |
| CI/CD triggers commented out — no automated quality gates on PRs | **High** | bd-460 (epic) |

---

## Delivery Constraints

### Timeline

| Target | Milestone | Status |
|--------|-----------|--------|
| Mar 1, 2026 | Landing page deployed | DL-01 |
| **Mar 15, 2026** | **Tribal Annual Report (long form) complete** | DL-02 |
| **Mar 31, 2026** | **Tribal Plan and Application complete** | DL-03 |
| Mar 31, 2026 | ATO documentation package submitted | DL-04 |
| Month 9 | Soft launch to 10-12 tribal orgs | DL-11 |
| May 29, 2026 | ATO authorization | AS-15 |
| Month 12 | Full rollout of remaining orgs | DL-12 |

### Build Sequence (DL-05)

Strictly sequential — no flexibility in ordering:

```
rendering → saving → review page → auto-save → PDF export
```

Each step depends on the previous. This is the critical path for March 15.

### Capacity

192 story points across 6 epics, ~4.75 FTE, ~11-12 weeks. No velocity benchmarks stated (DL-06). Government shutdown risk mitigated by prioritizing ACF-independent work first (DL-07).

---

## Priority Stack

Organized by blocking severity, then by dependency order:

### Tier 1: Blocking for any deployment
1. Fix prod Docker build to include all Django apps
2. Fix Helm chart mismatches (values schema, env vars, health check, logging)
3. Enable CI/CD triggers on PRs
4. Fix commented-out validation in `form_finalize.py`
5. Remove PII from INFO logs (`form_manager/utils.py:193+`)

### Tier 2: Blocking for MVP acceptance
6. Build Tribal Plan form (FI-01) — target Mar 31
7. Implement CSV export (AC-03)
8. Implement auto-save (FE-38) — in DL-05 critical path
9. Implement unsubmit/amend workflow (WF-04, WF-05)
10. Add automated a11y testing (SC-03)

### Tier 3: High severity for pilot readiness
11. Make PDF generation async (Celery/Redis or background task)
12. Wire Okta/Login.gov auth once NGSC environment access is granted — verify token claim structure matches backend expectations (AS-07)
13. Add self-service user management UI (PM-02)
14. Add connection resilience / low-bandwidth support (AD-09, FE-44, FE-45)
15. Implement telemetry/instrumentation (DL-15)
16. Tune gunicorn and run load tests (PR-11)
17. Harden API: pagination, rate limiting, PII scoping (DA-01)

### Tier 4: Medium — improves quality but not blocking
18. Add warning-tier validation (FE-21)
19. Implement screener/routing flow (FE-43)
20. Add year-over-year data comparison (WF-02)
21. Configure test coverage reporting (PR-15)
22. Add cross-submission pre-population (WF-12)
23. Conditional-logic-aware PDF export (DA-15)

---

## Jira Coverage Notes

Of 23 priority items above, **14 have at least one Jira ticket** and **9 have none**. Ticketless gaps that are Blocking or High:

| # | Gap | Severity | Action Needed |
|---|-----|----------|---------------|
| 4 | Validation commented out in finalize | **Blocking** | Needs ticket |
| 5 | PII in INFO logs | **Critical** | Needs ticket |
| 7 | CSV export | **Blocking** | Needs ticket — MVP acceptance criterion |
| 16 | Load testing | **High** | Needs ticket |
| 20 | Year-over-year comparison | Medium | Needs ticket (if MVP) |

**Discrepancies found** (Jira closed but gap remains open):

| Gap | Jira | Issue | Why gap persists |
|-----|------|-------|-----------------|
| Auto-save (FE-38) | bd-37, bd-54 | Both closed | Covered save-on-navigate only; periodic 30-60s auto-save never built |
| API hardening (DA-01) | bd-31 | Closed | Covered initial scaffolding; pagination, rate limiting, PII scoping not addressed |
| File attachments (FE-06) | bd-399 | Closed | USWDS component built; no storage backend wired |

See [requirements-traceability.md](requirements-traceability.md) for the full 111-requirement mapping.

---

## Open Decisions

> **Consolidated.** All open decisions now tracked as D-01 through D-08 in [open-items.md](open-items.md). The five from this section are D-01 (validation timing), D-02 (pilot size), D-03 (FISMA baseline), D-04 (Okta claims), D-05 (async infra). Three additional decisions were added: D-06 (multi-tenancy), D-07 (review workflow design), D-08 (Login.gov in MVP).
