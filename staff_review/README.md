# staff_review

Production federal-staff workflow, served at `/staff/`.

## Status: Phase 2 (in progress)

Per-screen translation of `staff_prototype/` (the React handoff bundle) into
real Django templates using USWDS Cotton components.

## Migration plan

| Screen                 | Prototype location                          | Production location                              | Status |
|------------------------|---------------------------------------------|--------------------------------------------------|--------|
| Inbox (Table view)     | `staff_prototype` `hifi-inbox.jsx`          | `staff_review/templates/staff_review/inbox.html` | done (mock data) |
| Inbox (Kanban view)    | `staff_prototype` `hifi-inbox.jsx`          | (todo)                                           | todo   |
| Inbox (Card view)      | `staff_prototype` `hifi-inbox.jsx`          | (todo)                                           | todo   |
| Submission detail (review) | `staff_prototype` `hifi-detail.jsx`     | (todo)                                           | todo   |
| Submission detail (edit-on-behalf) | `staff_prototype` `hifi-detail.jsx` | (todo)                                          | todo   |
| Return builder         | `staff_prototype` `hifi-workflow.jsx`       | (todo)                                           | todo   |
| Rationale modal        | `staff_prototype` `hifi-workflow.jsx`       | (todo)                                           | todo   |
| Determination modal    | `staff_prototype` `hifi-workflow.jsx`       | (todo)                                           | todo   |
| Login                  | `staff_prototype` `hifi-workflow.jsx`       | already in `csfeer/templates/index.html`         | n/a    |

## Data

Currently uses `staff_review/mock_data.py` (Python port of `hifi-data.js`)
so screens render without real backend wiring.

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

## Requirements coverage

Same Jira tickets as `staff_prototype/` (REQ-023, 024, 026, 027, 035, 041, 042,
043, 044) -- this is the production implementation. Refs live in the screen
templates as comments.

## Why separate from staff_prototype?

`staff_prototype/` is a static React SPA -- great for fast iteration and
stakeholder demos. `staff_review/` is the production Django app that backs the
real feature. Keeping them separate means:

- We can ship the prototype today without polluting production code paths
- Per-screen migration is incremental -- the prototype stays as a reference
- When the migration is complete, delete `staff_prototype/` cleanly
