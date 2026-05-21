# staff_review

Production federal-staff workflow, served at `/staff/`.

## Status: Phase 2 (in progress)

Per-screen translation of `staff_prototype/` (the React handoff bundle) into
real Django templates using USWDS Cotton components.

## Migration plan

| Screen                              | Production location                                            | Status               |
|-------------------------------------|----------------------------------------------------------------|----------------------|
| Inbox (Table view)                  | `templates/staff_review/inbox.html`                            | done (mock data)     |
| Inbox (Kanban view)                 | (todo)                                                         | todo                 |
| Inbox (Card view)                   | (todo)                                                         | todo                 |
| Submission detail (review)          | `templates/staff_review/submission_detail.html`                | done (mock data)     |
| Submission detail (edit-on-behalf)  | `templates/staff_review/submission_detail.html` (mode=edit)    | done (mock data)     |
| Return for revision builder         | `templates/staff_review/return_builder.html`                   | done (mock data)     |
| Rationale flow                      | inline in `submission_detail.html` (edit mode w/ pending edits)| done (mock data)     |
| Determination form                  | `templates/staff_review/determination.html`                    | done (mock data)     |
| Returned-state ack panel            | inline in `submission_detail.html` (status=Returned)           | done (mock data)     |
| Activity log drawer                 | inline `<details>` in right rail (prototype has a full drawer) | partial              |
| Login                               | already in `csfeer/templates/index.html`                       | n/a                  |

## Data (currently mock)

Lives in `staff_review/mock_data.py` -- Python port of
`hifi-data.js`. 9 sample submissions with full per-submission data
(contact, plan, budget, narrative, attestation, AO, events, return items).

**Phase 3:** replace `mock_data.py` imports with real querysets:

- `SUBMISSIONS` -> `Submission.objects.filter(...)` with permission scoping per CORE-132
- `FORM_DEFS` -> already exists in `form_manager/schema/forms/`
- `USER` -> `request.user` from Okta auth (CORE-138)

## Run locally

```bash
make start-local
# http://ui.csfeer:8000/staff/
```

You'll need to be signed in via the dev OAuth.

## Jira ticket coverage (authoritative)

Per current Jira (NOT the stale PRD), this app covers:

| Jira ticket | Behavior in this app                                                                  | Status |
|-------------|---------------------------------------------------------------------------------------|--------|
| CORE-29     | Federal Staff cross-region access (all submissions visible)                           | done (no region filter; mock data) |
| CORE-41     | Email federal staff on new org submission                                             | NOT WIRED (mock only)   |
| CORE-42     | Email recipient users on submission return                                            | NOT WIRED (mock only)   |
| CORE-43     | Clear AO signature on return                                                          | UI shows cleared state; real clear not wired |
| CORE-44     | Record final determination (Accepted / Closed without Acceptance) -- backend          | UI present; DB write not wired |
| CORE-45     | Lock submission from editing after final determination                                | UI present; lock not enforced server-side |
| CORE-46     | CSV export of resolved submissions (scoped by form type + FY)                         | TODO (not built)        |
| CORE-47     | System-wide tamper-evident audit log (FISMA / NIST 800-53)                            | TODO (not built)        |
| CORE-132    | Federal Staff permissions (view any form, edit on behalf, resolve / revise / archive) | TODO (no permission scope yet) |
| CORE-138    | Federal Staff login via ACF Okta                                                      | uses existing project Okta auth |
| CORE-161    | Recipient acknowledges each review item before resubmit                               | UI shows ack state; recipient flow not in this app |
| CORE-167    | Federal Staff rationale required when editing on behalf                               | UI present; DB write not wired |
| CORE-168    | Federal Staff returns submission with one or more review items                        | UI present; DB write not wired |
| CORE-169    | One return limit per submission                                                       | UI enforces (Return button hidden after 1 return) |
| CORE-170    | Original submission preserved read-only on resubmit                                   | TODO (not built)        |

PRD.md is stale outside of Sections 5-7; do not use as a source of truth.
All citations in templates and code should reference CORE-xxx Jira tickets,
not REQ-xxx.

## Why separate from staff_prototype?

`staff_prototype/` is a static React SPA -- great for fast iteration and
stakeholder demos. `staff_review/` is the production Django app that backs the
real feature. Keeping them separate means:

- We can ship the prototype today without polluting production code paths
- Per-screen migration is incremental -- the prototype stays as a reference
- When the migration is complete, delete `staff_prototype/` cleanly
