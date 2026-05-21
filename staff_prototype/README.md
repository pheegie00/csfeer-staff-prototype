# staff_prototype

Federal-staff workflow prototype, served at `/staff-prototype/`.

## What this is

Hi-fi React prototype of the staff review/return/edit-on-behalf/determination flow,
delivered as a handoff bundle from Claude Design (`claude.ai/design`). Lives as
static assets inside Django so it can be demoed via `make start-local` without
standing up a separate server.

## Run locally

```bash
make start-local
# then open http://ui.csfeer:8000/staff-prototype/
```

You'll need to be signed in via the dev OAuth (`make oauth-setup` if it's your
first time).

## What's in the bundle

| File | Purpose |
|------|---------|
| `static/staff_prototype/styles.css` | All visual styles (USWDS 3.x derived) |
| `static/staff_prototype/hifi-data.js` | Mock data: 9 sample submissions across Tribal Plan + Annual Report |
| `static/staff_prototype/hifi-atoms.jsx` | Shared UI atoms (Btn, Card, Section, Field, Alert, Modal, Rail, Toast) |
| `static/staff_prototype/hifi-workflow.jsx` | Return builder, Rationale modal, Determination modal, Returned-state panel, Login |
| `static/staff_prototype/hifi-detail.jsx` | Submission detail (review + edit-on-behalf modes), form renderers, activity log |
| `static/staff_prototype/hifi-inbox.jsx` | Inbox with 3 views: Table, Kanban, Cards |
| `static/staff_prototype/hifi-app.jsx` | Router + state store + main App |
| `templates/staff_prototype/index.html` | Entry HTML; loads React, Babel, and all the JSX files via `{% static %}` |

## Screens

1. **Login** -- `#/login` -- ACF Okta (Federal Staff) or Login.gov (Recipients)
2. **Inbox** -- `#/inbox` -- 3 switchable views (Table / Kanban / Cards), filters by status, form, region, state
3. **Submission detail (review)** -- `#/sub/:id` -- read-only form with sticky action bar
4. **Submission detail (edit-on-behalf)** -- `#/sub/:id/edit` -- inline-editable form with pending-edits tracking
5. **Return builder** -- `#/sub/:id/return` -- compose review items with email preview
6. **Rationale modal** -- triggered when saving edits-on-behalf (mandatory)
7. **Determination modal** -- Accept / Close without acceptance (final + locked)

## Requirements coverage (Jira refs in the source)

- REQ-023 -- Each review item individually acknowledged before resubmit
- REQ-024 -- One return per submission
- REQ-026 -- Lock submission from editing after final determination
- REQ-027 -- CSV export of resolved submissions only
- REQ-035 -- Original submission preserved read-only
- REQ-041 -- Email notification to recipients on return
- REQ-042 -- AO signature cleared on return
- REQ-043 -- Edit-on-behalf logged with rationale
- REQ-044 -- Functional parity with current review memo

## Migration to production templates

This app is intentionally a separate Django app from the rest of the codebase
so it can be deleted or merged later. Phase 2 of the work:

- [ ] Translate Inbox to Django template using `csfeer/templates/patterns/`
      Cotton components, backed by real Submission queryset
- [ ] Translate Submission detail (review + edit modes)
- [ ] Translate Return builder
- [ ] Wire Rationale + Determination modals to real backend (CORE-44, CORE-45)
- [ ] Replace mock data with real Submission models
- [ ] Add Federal Staff permission scope (CORE-132)
- [ ] Delete this prototype app once production templates land

## Why not auto-translate React to Django?

Because the prototype lies about backend reality. It uses a React store with
mock data and synchronous mutations. Real Django views need:
- Permission checks (CORE-132, CORE-29 cross-region)
- Database mutations through Submission models
- Audit log writes (CORE-36, CORE-47)
- Email sends (CORE-41, CORE-42, CORE-157)

The translation is a per-screen exercise that requires backend coordination.
The prototype's job is to align on **what the screens look like and how the
flow connects** so the backend work has a clear UI target.
