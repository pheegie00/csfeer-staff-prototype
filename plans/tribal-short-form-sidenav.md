# Plan: Tribal Short Form Side Navigation

> Source PRD: `thoughts/shared/research/tribal_short_form_sidenav_prd.md`

## Architectural decisions

Durable decisions that apply across all phases:

- **Scope**: Limit the new navigation model to the Tribal Short Form. Other forms keep the existing step-indicator layout and behavior.
- **Routes**: Continue using `form_edit` for edit destinations with `step` and `page` query parameters, and keep `form_review` as the separate review destination.
- **Navigation source of truth**: Build the sidenav hierarchy from the existing schema UI after applying the same filter-driven visibility rules already used to remove excluded pages and fields.
- **Navigation shape**: Model the left rail as top-level sections plus page-level child items for the active section, with `Review and Submit` as a top-level leaf item.
- **Save behavior**: Treat edit-page sidenav interactions as save-and-navigate actions that reuse the existing draft-save workflow rather than introducing client-side state or autosave.
- **Fallback resolution**: Centralize destination resolution so post-save filtering changes can redirect users to a viable visible destination instead of a removed page.
- **Review behavior**: Keep `Review and Submit` on its existing route and preserve the current inline `Edit section` links on the review page.
- **Data model**: Do not introduce database schema changes; this feature should fit within the current form schema, view, and template structure.

---

## Phase 1: Short-Form-Only Left Rail Shell Completed

**User stories**: 1, 2, 8, 18, 19, 23

### What to build

Introduce a desktop two-column layout for the Tribal Short Form that replaces the top horizontal step indicator with a USWDS side navigation rail. The left rail should show all top-level section titles plus `Review and Submit`, while the main content column continues to render the current edit or review content. Titles should be taken directly from the existing short-form schema without renaming or numbering changes.

### Acceptance criteria

- [x] Tribal Short Form edit pages render a left-rail navigation and no longer show the horizontal step indicator.
- [x] The left rail lists the existing top-level section titles and `Review and Submit`.
- [x] Non-tribal forms continue to use the current step-indicator layout unchanged.
- [x] The plan does not introduce title renames, numbering, or duplicate-label workarounds in this phase.

---

## Phase 2: Active Section Expansion and Current-State Marking Completed

**User stories**: 3, 4, 7, 15, 19

### What to build

Expand only the active section in the sidenav while editing so users can see the page-level structure for the section they are currently in. The expanded child list should include only currently visible pages, and the navigation should clearly indicate the active parent section and active child page.

### Acceptance criteria

- [x] The active edit section expands to show its visible child pages.
- [x] Inactive sections remain collapsed.
- [x] The current parent section and current child page are both visually marked as current on edit pages.
- [x] Hidden pages caused by filtering do not appear in the sidenav.

---

## Phase 3: Clickable Sidenav Navigation With Draft Save Completed

**User stories**: 5, 6, 9, 12, 13, 14, 20, 21

### What to build

Make the sidenav interactive on edit pages so top-level section clicks route to the first visible page in that section, child-page clicks route to that exact visible page, and `Review and Submit` remains directly reachable. Each sidenav interaction should save the current draft values first using the existing save workflow, then navigate to the requested destination even when required fields are incomplete.

### Acceptance criteria

- [x] Clicking a top-level section on an edit page saves current draft data and moves to the first visible page in that section.
- [x] Clicking a child page on an edit page saves current draft data and moves to that visible page.
- [x] Clicking `Review and Submit` from an edit page saves current draft data and routes to review even if required fields are incomplete.
- [x] Posted values persist across sidenav navigation in the same way they do for the current draft-save flow.

---

## Phase 4: Review-Page Sidenav Parity Completed

**User stories**: 10, 11, 17

### What to build

Render the same left-rail navigation on the review page so the overall navigation model stays consistent from editing through submission. On review, collapse the edit sections and highlight only `Review and Submit`, while keeping the existing review content and inline `Edit section` links intact.

### Acceptance criteria

- [x] The review page renders the same left-rail navigation container used on short-form edit pages.
- [x] `Review and Submit` is the highlighted current item on review.
- [x] Other sections are collapsed on review.
- [x] Existing inline `Edit section` links remain available and functional.

---

## Phase 5: Filter-Change Fallback Resolution Completed

**User stories**: 15, 16, 20, 22

### What to build

Add centralized destination resolution that recomputes visible pages after save and checks whether the requested sidenav destination still exists. If filtering removes the requested page, redirect the user to a sensible fallback such as the selected parent section or the first visible page in that section, avoiding broken destinations and preserving the existing server-side filtering model.

### Acceptance criteria

- [x] Visible destinations are recomputed after sidenav-triggered saves using the same filtering logic as the rest of the form flow.
- [x] If a requested child page disappears after save, the user is redirected to a viable fallback instead of an invalid destination.
- [x] If a selected section still has visible pages, fallback routing lands on that section's first visible page.
- [x] Destination resolution behavior is covered by focused tests for missing-target recovery and filtered visibility changes.
