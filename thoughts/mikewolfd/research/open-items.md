# Open Items — CSFEER/CORE

> **Purpose:** Single source of truth for all conflicts, risks, open questions, and open decisions.
> **Sources:** Consolidated from [UNDERSTANDING.md](UNDERSTANDING.md), [MATRIX.md](MATRIX.md), [mvp-gap-analysis.md](mvp-gap-analysis.md), [csfeer-architectural-review.md](csfeer-architectural-review.md), [VALUE_STREAM_ANALYSIS.md](VALUE_STREAM_ANALYSIS.md)
> **Last updated:** 2026-03-05

---

## Conflicts (C-1 through C-13)

Cross-document disagreements requiring product owner resolution. Inline flags (e.g., "⚡ C-7") in [MATRIX.md](MATRIX.md) cross-reference these by number.

**Five are MVP-blocking** (C-1, C-3, C-5, C-7, C-13).

| # | Topic | Source A | Source B | Question | MVP-blocking? | Resolution Status |
|---|-------|----------|----------|----------|---------------|-------------------|
| C-1 | Validation timing | [S29]: "while a grant-recipient fills out a form" (during-entry implied) | [S21]: review page validation; partial saves with invalid data allowed | When does validation fire? Determines form UX architecture. | **Yes** | **Open** — listed as open decision in gap analysis |
| C-2 | MVP pilot size | [S24]: 20+ tribal recipients | Other refs: 10–12 pilot cohort | Is 20+ the target or aspirational? Sets support staffing. | No | **Open** — listed as open decision in gap analysis |
| C-3 | FISMA classification | [S24] NFR4: FISMA Moderate ([S29] does NOT specify a level) | [S12]: Rev5-**Low** controls | Low or Moderate baseline? Determines entire security posture. | **Yes** | **Open** — listed as open decision in gap analysis |
| C-4 | MVP scope — APIs | [S29]: Must priority | [S21]: Out of scope; [S31]: stretch goal; [S39]: read-only only | Are APIs in MVP? If so, read-only per [S35]/[S39]. | No | **Effectively resolved** — read-only API exists (DA-01 ⚠️); 7 GET endpoints via Django Ninja |
| C-5 | MVP scope — Authorization | [S29]: Must priority (PM-01–PM-05) | [S21]: Out of scope | Is authz in MVP? Without it, how distinguish who can submit vs view? | **Yes** | **Effectively resolved by implementation** — org-level admin/editor/viewer roles implemented (PM-01 ✅, PM-08 ⚠️); MATRIX.md still marks PM-08 as conflict |
| C-6 | MVP scope — Notifications | [S29]: Must priority | [S21]: Out of scope | Are notifications in MVP? No deadline alerts otherwise. | No | **Open** — no notification infrastructure exists; WF-13/WF-14 are 🔮 deferred |
| C-7 | MVP scope — Approval workflows | [S29]: Must priority | [S21]: Out of scope | Are federal approval workflows in MVP? No approve/revise pipeline otherwise. | **Yes** | **Effectively resolved by deferral** — WF-09 marked 🔮 in MATRIX.md; review workflow questions remain open for Phase II (see D-07 below) |
| C-8 | Contract duration | [S29]: 12+12 = 24 months | [S02]: "1 year + 9 month option" = 21 months | Which is correct? Affects planning horizon. | No | **Open** |
| C-9 | User satisfaction metric | [S24]: ≥80% easier than PDFs | Other refs: ≥4/5 satisfaction score | Different measurement frameworks. | No | **Open** |
| C-10 | PDF generation tech | [S18]: WeasyPrint | Other refs: headless Chrome | Which approach? Determines deployment constraint. | No | **Effectively resolved** — WeasyPrint in production (IT-07 ✅); synchronous, needs async wrapper |
| C-11 | Competing platform | CSFEER (this project) | [S13]: $1.2M GrantSolutions dev | What happened to the OLDC effort? Competitive, fallback, or abandoned? | No | **Open** |
| C-12 | Transition plan duration | [S33]: 4 weeks (2 sprint cycles) | [S35]: 90-day plan (doc audit → training → parallel ops) | 4 weeks vs 90 days — order-of-magnitude difference. | No | **Open** |
| C-13 | Login.gov in MVP? | [S39] AC-02: Login.gov working for all pilot users | [S31] AS-18: MVP uses basic sessions; Login.gov deferred | Acceptance criterion contradicts Q1 plan. | **Yes** | **Open** — auth blocked on ACF NGSC environment access; not a code problem (see D-04) |

**Summary:** 6 open, 4 effectively resolved, 3 open but non-blocking.

---

## Risks (R-01 through R-14)

Source-verified from [S16], [S17], [S35], [S36], [S38], and other project documents.

| ID | Risk | Prob | Impact | Mitigation | Source |
|----|------|------|--------|------------|--------|
| R-01 | Government shutdown | Med | Med | Delivery plan for shutdown scenarios; non-blocking work sequenced first; ATO prep runs in parallel | [S16] |
| R-02 | Tribal consultation | Low | High | Ongoing consultation, opt-in approach, transparent communication, respect for sovereignty | [S16] |
| R-03 | Login.gov complexity | Low | Med | Early technical spikes; close coordination with ACF; staged integration and testing | [S16] |
| R-04 | Data migration challenges | Med | Med | Limit MVP pre-population to high-confidence data only; document expansion path for Phase II | [S16] |
| R-05 | User adoption | Med | High | Tribal-informed design, usability testing, training, phased onboarding, help desk support | [S16] |
| R-06 | ATO/Security reviews | Low | High | Parallel ATO workstream; weekly syncs; early control implementation; **#1 risk per [S35] (p×i = 0.45)** | [S17]; [S35] |
| R-07 | Dependency on external reviews | Med | Med | Questions staged early; assumptions documented; flexible sequencing | [S17] |
| R-08 | Non-gov user auth path uncertainty | ? | ? | TBD — could delay development or require rework. Relates to C-13 and D-04. | [S10] |
| R-09 | PIA classification guidance delay | ? | ? | Could block system deployment and ATO approval. See Q-08. | [S10] |
| R-10 | Competing GrantSolutions implementation ($1.2M–$1.71M) | ? | ? | Relationship to CSFEER unclear — competitive? fallback? abandoned? See C-11. | [S13] |
| R-11 | State resistance to platform adoption (e.g., NJ "empower") | ? | ? | OCS can issue DCLs (Dear Colleague Letters) | [S02] |
| R-12 | Attestation/signature workflow unclear | ? | ? | How does tribal council sign-off work digitally? See Q-12 (new). | [S36] |
| R-13 | Policy interpretations may alter form logic mid-development | ? | Med | OMB form definitions and OCS validation rules are dependencies | [S36] |
| R-14 | OLDC user data isolation | Med | Med | CSFEER creating users independently from OLDC; requires API integration to import existing users; Thomas Oldfield (ACF Tech) is data liaison | [S38] |
| R-15 | Deployment artifacts broken | High | High | Prod Docker image likely missing app code; Helm chart mismatches; health check fails. *New — from architectural review.* | Arch review |
| R-16 | PII exposure (API + logs) | High | High | API returns full form data JSON with PII; INFO-level logging dumps form data. *New — from architectural review.* | Arch review |

---

## Open Decisions (D-01 through D-08)

Decisions requiring product or technical resolution before implementation. Newly assigned IDs for tracking.

| ID | Decision | Context | Traces to | Owner |
|----|----------|---------|-----------|-------|
| D-01 | Validation timing | Inline during entry vs. review-page-only? PWS says "during entry"; tech spec says review-page. Determines entire form UX. | C-1, FE-25 | Product |
| D-02 | Pilot size | 10 (AC-04) vs. 10-12 (DL-11) vs. 20+ (SC-01)? Affects support staffing and success criteria. | C-2 | Product |
| D-03 | FISMA baseline | Low (AS-A10/S12) vs. Moderate (S24/PR-12)? Affects ATO scope, control implementation, and timeline. | C-3 | Security/Product |
| D-04 | Okta token claim mapping | Will Okta emit roles in `realm_access.roles` (Keycloak convention) or different claim path? Backend role sync depends on this. Testable once NGSC access granted. | C-13, AS-07 | Tech |
| D-05 | Async infrastructure | Celery+Redis? Django-Q? Task queue choice affects PDF generation, email, notifications. No async capability exists today. | Arch review | Tech |
| D-06 | Multi-tenancy isolation model | Tenant, permission, data partitioning, or hybrid? Constrains all foundation-layer deliverables. Not yet designed. | VALUE_STREAM_ANALYSIS.md | Tech/Arch |
| D-07 | Federal review workflow design | Six sub-questions (all post-MVP but design affects data model now): Sequential vs. parallel steps? Conditional routing? Unanimous vs. any-one-approves? Who configures? Delegation rules? Reviewer permission tiers? | C-7, WF-09, MATRIX.md [WS-07/08/09] | Product |
| D-08 | Login.gov in MVP? | AC-02 says yes; AS-18 says deferred. Blocked on ACF NGSC environment access. Not a code problem — OIDC plumbing is built. | C-13, R-08 | Product/ACF |

---

## Open Questions (Q-01 through Q-12)

Questions not captured as conflicts or decisions. Some overlap with risks.

| ID | Question | Context | Traces to |
|----|----------|---------|-----------|
| Q-01 | What are the specific validation rules for each of the 3 Tribal forms? | Rules live in the forms themselves / SmartForms XSD, not in Confluence docs | FE-20 |
| Q-02 | How do Tribal recipients currently collaborate on form preparation? | Affects multi-user workflow design | WF-15 |
| Q-03 | What analytics/reporting format does Congress require? | Melanie Durley is SME; requirements undocumented | DA-03 |
| Q-04 | How should biannual vs annual Plan Application submissions be handled? | Affects form scheduling logic | WF-01 |
| Q-05 | What are the specific UEI/SAM.gov integration points for automated mismatch detection? | | FE-24 |
| Q-06 | Field-level mapping between OLDC columns and CSFEER schema fields | FY24 export conventions documented; field-level mapping unknown | R-04, R-14 |
| Q-07 | Form definition versioning vs submission snapshot history — what exactly is required? | | FE-30, FE-31 |
| Q-08 | PIA classification: "electronic information collection" vs "application"? | Rubric needed from privacy team (Tobi/Oyindasola) | R-09 |
| Q-09 | SORN timeline and scope | Confirmed required but no timeline documented; full PII inventory needed beyond email | R-09 |
| Q-10 | Notification SLA/deadline enforcement and escalation rules — what are the business rules? | | C-6, WF-14, WF-18 |
| Q-11 | CSV export format and scope — what columns, what granularity, who consumes it? | MVP acceptance criterion (AC-03) with no specification | DA-03 |
| Q-12 | How does tribal council sign-off/attestation work digitally? | No attestation model, signature capture, or transmittal letter workflow | R-12, UP-03 |

---

## Summary

| Category | Total | Open | Resolved/Deferred |
|----------|-------|------|-------------------|
| Conflicts (C-xx) | 13 | 6 blocking + 3 non-blocking | 4 effectively resolved |
| Risks (R-xx) | 16 | 16 (7 unscored) | 0 |
| Decisions (D-xx) | 8 | 8 | 0 |
| Questions (Q-xx) | 12 | 12 | 0 |
| **Total** | **49** | **45** | **4** |
