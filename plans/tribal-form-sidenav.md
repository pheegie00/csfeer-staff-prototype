# Plan: Tribal Form Side Navigation

> Source PRD: `thoughts/shared/research/tribal_short_form_sidenav_prd.md`

This plan extends the existing tribal short-form sidenav work to the Tribal Long Form and
renames the implementation around the generic `form_sidenav` pattern. The current short-form
implementation provides a reference point, but the work in this plan is not complete until both
tribal annual report variants share the same behavior and naming cleanup.

## Architectural decisions

Durable decisions that apply across all phases:

- **Scope**: Apply the sidenav behavior to `CSBG Annual Report 3.0 Tribal Annual Report (Tribes)` and `CSBG Annual Report 3.0 Tribal Short Form (Tribes)` only. Non-tribal forms keep the existing step-indicator layout and behavior for now.
- **Naming**: Standardize the implementation on `form_sidenav` naming rather than short-form-specific or tribal-variant-specific names.
- **Routes**: Continue using `form_edit` for edit destinations with `step` and `page` query parameters, and keep `form_review` as the separate review destination.
- **Navigation source of truth**: Build the sidenav hierarchy from the existing schema UI after applying the same filter-driven visibility rules already used to remove excluded pages and fields.
- **Navigation shape**: Model the left rail as top-level sections plus page-level child items for the active section, with `Review and Submit` as a top-level leaf item.
- **Save behavior**: Treat edit-page sidenav interactions as save-and-navigate actions that reuse the existing draft-save workflow rather than introducing client-side state or autosave.
- **Fallback resolution**: Reuse the existing destination resolution behavior. If filtering removes the requested page, fall back to the first visible page in the requested section, then to a nearby visible section when necessary.
- **Review behavior**: Keep `Review and Submit` on its existing route, collapse edit sections on review, and preserve the current inline `Edit section` links that return to the first page of each step.
- **Duplicate child labels**: Do not add code-level disambiguation for duplicate sibling page titles in the long-form sidenav in this pass. Leave the current labels as-is and defer any visual differentiation to design.
- **Mobile behavior**: Keep the current desktop-only sidenav behavior. This pass does not add a mobile replacement navigation pattern.
- **Data model**: Do not introduce database schema changes; this feature should fit within the current form schema, view, template, and test structure.

## Rename inventory

- `form_manager/views/short_form_navigation.py` -> `form_manager/views/form_sidenav.py`
- `form_manager/templates/form_manager/_short_form_sidenav.html` -> `form_manager/templates/form_manager/_form_sidenav.html`
- `use_short_form_sidenav` -> `use_form_sidenav`
- `short_form_sidenav_items` -> `form_sidenav_items`
- `short_form_sidenav_submit_form_id` -> `form_sidenav_submit_form_id`
- `ShortFormSidenavItem` -> `FormSidenavItem`
- `build_short_form_sidenav_items` -> `build_form_sidenav_items`
- `resolve_short_form_edit_destination` -> `resolve_form_edit_destination`
- Remove `csf-form` naming from DOM IDs in favor of generic form IDs
- Rename the generic navigation unit tests to `form_sidenav` naming while keeping schema-specific integration files variant-specific

---

## Phase 1: Tribal Form Left Rail Shell

**User stories**: 1, 2, 8, 18, 19, 23

### What to build

Extend the existing desktop two-column tribal form layout so both tribal annual report variants
use the same left-rail navigation shell in place of the horizontal step indicator. The left rail
should show all top-level section titles plus `Review and Submit`, while the main content column
continues to render the current edit or review content. Titles should be taken directly from the
existing schema definitions without renaming or numbering changes.

### Acceptance criteria

- [x] Tribal Short Form edit pages render the left-rail navigation using the generic `form_sidenav` implementation names.
- [x] Tribal Long Form edit pages render the same left-rail navigation container and no longer show the horizontal step indicator.
- [x] The left rail lists the existing top-level section titles and `Review and Submit` for both tribal forms.
- [x] Non-tribal forms continue to use the current step-indicator layout unchanged.
- [x] The plan does not introduce title renames, numbering, or duplicate-label workarounds in this phase.

---

## Phase 2: Active Section Expansion and Current-State Marking

**User stories**: 3, 4, 7, 15, 19

### What to build

Expand only the active section in the sidenav while editing so users can see the page-level
structure for the section they are currently in. The expanded child list should include only
currently visible pages, and the navigation should clearly indicate the active parent section and
active child page for both tribal variants.

### Acceptance criteria

- [x] The active edit section expands to show its visible child pages for both tribal forms.
- [x] Inactive sections remain collapsed.
- [x] The current parent section and current child page are both visually marked as current on edit pages.
- [x] Hidden pages caused by filtering do not appear in the sidenav.
- [x] Duplicate child labels in the long form remain unchanged rather than being disambiguated in code.

---

## Phase 3: Clickable Sidenav Navigation With Draft Save

**User stories**: 5, 6, 9, 12, 13, 14, 20, 21

### What to build

Make the sidenav interactive on tribal edit pages so top-level section clicks route to the first
visible page in that section, child-page clicks route to that exact visible page, and
`Review and Submit` remains directly reachable. Each sidenav interaction should save the current
draft values first using the existing save workflow, then navigate to the requested destination
even when required fields are incomplete.

### Acceptance criteria

- [ ] Clicking a top-level section on an edit page saves current draft data and moves to the first visible page in that section.
- [ ] Clicking a child page on an edit page saves current draft data and moves to that visible page.
- [ ] Clicking `Review and Submit` from an edit page saves current draft data and routes to review even if required fields are incomplete.
- [ ] Posted values persist across sidenav navigation in the same way they do for the current draft-save flow.
- [ ] The genericized submit-form IDs and context names are used consistently in templates and JavaScript hooks.

---

## Phase 4: Review-Page Sidenav Parity

**User stories**: 10, 11, 17

### What to build

Render the same left-rail navigation on the review page for both tribal forms so the overall
navigation model stays consistent from editing through submission. On review, collapse the edit
sections and highlight only `Review and Submit`, while keeping the existing review content and
inline `Edit section` links intact.

### Acceptance criteria

- [ ] The review page renders the same left-rail navigation container used on tribal edit pages.
- [ ] `Review and Submit` is the highlighted current item on review.
- [ ] Other sections are collapsed on review.
- [ ] Existing inline `Edit section` links remain available and continue to return users to page 0 of the selected step.
- [ ] Mobile behavior remains unchanged, with the sidenav hidden outside desktop layouts.

---

## Phase 5: Filter-Change Fallback Resolution and Coverage

**User stories**: 15, 16, 20, 22

### What to build

Use centralized destination resolution that recomputes visible pages after save and checks whether
the requested sidenav destination still exists. If filtering removes the requested page, redirect
the user to a sensible fallback such as the selected parent section or the first visible page in
that section, avoiding broken destinations and preserving the existing server-side filtering model.
Complete the rollout with shared navigation unit coverage, long-form integration coverage, and
updated tribal E2E tests.

### Acceptance criteria

- [ ] Visible destinations are recomputed after sidenav-triggered saves using the same filtering logic as the rest of the form flow.
- [ ] If a requested child page disappears after save, the user is redirected to a viable fallback instead of an invalid destination.
- [ ] If a selected section still has visible pages, fallback routing lands on that section's first visible page.
- [ ] Destination resolution behavior is covered by generic `form_sidenav` unit tests that exercise both tribal schemas.
- [ ] Tribal Short Form integration coverage remains variant-specific and continues to pass under the generic naming.
- [ ] Tribal Long Form integration coverage is added in a dedicated `test_tribal_long_form_integration.py` file.
- [ ] Tribal E2E coverage is updated to reflect the left-rail navigation contract for both variants.
