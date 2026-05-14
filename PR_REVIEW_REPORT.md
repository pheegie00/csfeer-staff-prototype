# Pull Request Code Review Report

**Repository:** focusconsulting/csfeer  
**Reviewed:** 2026-05-14  
**Reviewer:** Claude (claude-sonnet-4-6)

---

## Summary of Open PRs

| # | Title | Author | State | CI |
|---|-------|--------|-------|----|
| [#261](#pr-261) | [CORE-103] Tribal P&A Design QA Sections 3, 5, 6, 7 & 8 | LogvnR | Open (non-draft) | ✅ All passing |
| [#242](#pr-242) | reduce wait times | ryanbagwell | **Draft** | — |
| [#214](#pr-214) | fix(form-manager): block finalize when invalid and scroll to banner | mikewolfd | Open (non-draft) | ❌ e2e-tests failing |
| [#213](#pr-213) | fix(form-manager): prune steps with no pages after field exclusion | mikewolfd | Open (non-draft) | ❌ e2e-tests failing |

---

## PR #261 — [CORE-103] Tribal P&A Design QA Sections 3, 5, 6, 7 & 8 {#pr-261}

**Branch:** `logvnr/core-103-3_design-qa` → `main`  
**CI:** pre-commit ✅, tests ✅  
**Existing reviews:** Active back-and-forth between ryanbagwell and LogvnR (3 rounds as of 2026-05-13).

### What this PR does

- Introduces a new `PercentageField` / `ACFPercentageField` (whole-number, `%`-suffix input).
- Converts all Section 5.1 allocation fields from `DecimalField` (2 d.p.) to the new `PercentageField` (0 d.p.).
- Caps administrative cost at 5%; validates total must equal 100% (field-level errors instead of form-level `ValidationError`).
- Renames "Targeted Community Eligibility" → "Community Eligibility" throughout.
- Minor text and style changes (accordion button colour, `text_block.html` layout, etc.).
- Adds `boolean_review.html` template for rendering boolean fields on the review page.

### Findings

#### 🔴 High — `inputmode` conflict in `percentage.html` template

`ACFPercentageField.widget_attrs` sets `"inputmode": "numeric"` (integers only), but
`form_manager/templates/form_manager/widgets/percentage.html` hardcodes `inputmode="decimal"`.
The template wins, so mobile keyboards will show a decimal keypad instead of a numeric keypad,
which is misleading for whole-number-only fields.

**File:** `form_manager/templates/form_manager/widgets/percentage.html` (line 7)  
**Fix:** Remove the hardcoded `inputmode="decimal"` from the template and let `:attrs` propagate
the value set by `widget_attrs` (`inputmode="numeric"`).

#### 🔴 High — `boolean_review.html` silently drops "No" / unchecked state

The new template only renders `"Yes"` when `component.value` is truthy, and renders nothing
when it is falsy (and there are no errors). On the review page an unanswered required checkbox
and a deliberately-unchecked checkbox are visually indistinguishable. Users and reviewers will
not be able to tell whether the applicant checked or left unchecked the
"The Tribe or Tribal Organization acknowledges and assures compliance…" checkbox.

**File:** `form_manager/templates/form_manager/forms/boolean_review.html`  
**Fix:** Add an `{% else %}No{% endif %}` branch, or render "Not answered" / a dash so the
state is always explicit.

#### 🟡 Medium — Contextual error messages replaced with generic "This field is required."

The `clean()` method previously surfaced descriptive errors, e.g.:
- `"Names of all represented tribes are required when representing more than one tribe."`
- `"Provide a citation to the State statute or code acknowledging State recognition."`
- `"Upload supporting recognition documentation."`

All have been replaced with `"This field is required."` This is a regression in accessibility
and usability: screen-reader users and applicants unfamiliar with the form will lose the
explanation of *why* a field is required in a given context.

**File:** `form_manager/schema/forms/tribal_plan/fields.py`, `clean()` method  
**Recommendation:** Keep contextual messages, or at minimum add the condition reason:
e.g. `"Required when delegating signature authority."`.

#### 🟡 Medium — Alpine.js `$money` mask applied to percentage inputs

`ACFPercentageField.widget_attrs` adds `"x-mask:dynamic": "$money($input, '.', ',', 0)"`.
The `$money` Alpine mask is a currency formatter (adds thousands commas). For 0–100 integer
percentage fields this never triggers visually, but semantically it's the wrong mask, could
confuse future maintainers, and will produce `"5,"` if someone types `"5000"` into an admin
cost field.

**File:** `form_manager/schema/fields.py`, `ACFPercentageField.widget_attrs`  
**Fix:** Replace with a simpler integer mask such as `"x-mask": "999"` or remove the mask
entirely since validation enforces the range.

#### 🟡 Medium — `field_review.html` no longer shows value alongside errors

Before this PR, the template rendered both the field value *and* the error in the same block.
After, any presence of errors hides the value entirely. A field that has a value *and* a
post-submission error (e.g., a calculated total that exceeds 100%) will show only the error
text, losing the actual submitted value on the review page. This makes it harder for applicants
to see what they entered.

**File:** `form_manager/templates/form_manager/forms/field_review.html`

#### 🟢 Low — `text_block.html` removes margin utilities from bordered variant

The bordered variant previously applied `margin-top-2 margin-bottom-3` (via `usa-card__container`);
the replacement only adds `border border-base-lighter radius-md padding-205`. If any callers
relied on that top/bottom margin for spacing, this could cause layout regression.

**File:** `form_manager/templates/form_manager/text_block.html`  
**Recommendation:** Verify the Debarment Certification text block (the only changed callsite,
`form.py` line ~652) renders with adequate spacing in a browser.

#### 🟢 Low — `%%` in `error_messages` is implicit

`error_messages={"max_value": "Cannot exceed 5%%"}` relies on Django's `%`-style format
interpolation collapsing `%%` to `%`. The tests confirm it works, but using a plain `%` with no
format specifiers would be more readable and does not depend on the interpolation side-effect.
Django's `ValidationError` with explicit `params={}` avoids this entirely.

### Positive notes

- Field-level errors on `alloc_total_y1`/`alloc_total_y2` (instead of form-level
  `ValidationError`) are a clear improvement: errors now appear next to the relevant field
  rather than at the top of the page.
- New `PercentageInput` widget mirrors the existing `CurrencyInput` pattern well.
- Admin-cost 5% cap properly applied to both Y1 and Y2 fields.
- Test data in integration tests correctly updated to reflect whole-number constraints.

---

## PR #242 — reduce wait times {#pr-242}

**Branch:** `speed-up-e2e-tests` → `main`  
**State:** **Draft** — not ready for merge  
**CI:** No checks run

### What this PR does

Replaces many `page.wait_for_timeout(N)` calls in E2E tests with
`page.wait_for_load_state("networkidle")` (a semantically correct wait after navigation), and
reduces JS-event timeouts from 500 ms → 300 ms. Adds `--durations=15` to all test targets and
`-s` to local targets.

### Findings

#### 🟡 Medium — `wait_for_load_state("networkidle")` after `blur()` (no navigation)

In `test_integer_field_comma_formatting.py` the last change in the Alpine.js section replaces:
```python
page.locator('input[name="employment__unknown"]').blur()
page.wait_for_timeout(1000)
```
with:
```python
page.locator('input[name="employment__unknown"]').blur()
page.wait_for_load_state("networkidle")
```
A `blur()` event triggers Alpine.js recalculation (JS only, no HTTP request), not a page
navigation. `networkidle` waits for no in-flight network requests; it would pass immediately
(or fail if a background request happens to be in-flight) and may miss the Alpine re-render.
A short `wait_for_timeout(300)` is more appropriate here.

**File:** `tests/e2e/test_integer_field_formatting.py` (near the employment blur assertions)

#### 🟢 Low — `-s` (no output capture) added to CI unit test target

`test-unit-ci` in `Makefile` now includes `--durations=15` but *not* `-s`. `test-e2e-ci` gets
both `--durations=15` and retains existing `-s`. This is consistent and correct.

#### 🟢 Low — Remaining 300 ms waits after `blur()`

Several 300 ms waits after `blur()` remain (Alpine.js calculation). This is fine and expected;
they are intentionally *not* replaced.

### Overall

The changes are a straightforward quality improvement. The draft status is appropriate — the
one misused `networkidle` call should be fixed before merging.

---

## PR #214 — fix(form-manager): block finalize when invalid and scroll to banner {#pr-214}

**Branch:** `fix/form-finalize-validation` → `main`  
**CI:** pre-commit ✅, **e2e-tests ❌ (failing)**  
**Created:** 2026-04-20, **last updated:** 2026-04-20 (3+ weeks stale)  
**Existing review:** ryanbagwell asked for a better description (outstanding, no response).  
**Note:** "Made with [Cursor](https://cursor.com)" in PR body.

### What this PR does

- `form_finalize` view now validates the full form before marking it submitted; on failure it
  redirects to the review page at `#form-validation-summary`.
- Adds `id="form-validation-summary"` to the review page error container with ARIA live region
  and `tabindex="-1"` for focus management.
- Adds an inline `<script>` that smooth-scrolls to the error banner when the fragment is
  present, then strips the fragment from the URL.

### Findings

#### 🔴 High — e2e CI is failing

The `e2e-tests` check failed at the time of the last push (2026-04-20) and the PR has not been
updated since. The failure must be investigated and resolved before this PR is mergeable.

#### 🔴 High — `from django.contrib import messages` becomes a dead import

The diff removes the only `messages.error(...)` call. If `messages` is not used elsewhere in
`form_manager/views/form_finalize.py`, this becomes an unused import (F401). Pre-commit passed,
which means either `messages` is still used (e.g., `messages.success(...)` elsewhere in the
file outside the diff window) or the import was somehow not flagged. This should be verified.

**File:** `form_manager/views/form_finalize.py`

#### 🟡 Medium — No user-facing explanation when redirect is due to validation failure

When `form_finalize` detects an invalid form and redirects to `…/review/#form-validation-summary`,
the review page does display the error alert banner. However, there is no flash message
explaining that the *submission was blocked*. A user who clicks "Submit" and sees the review
page again may not immediately understand why. Consider adding a
`messages.error(request, "Please correct the errors below before submitting.")` before the
redirect.

**File:** `form_manager/views/form_finalize.py`

#### 🟡 Medium — `entry.data` passed as both `data` and `initial`

```python
form = django_form_class(entry.data, initial=entry.data)
```
Passing the same dict as both the bound `data` argument and `initial` is unusual. Django uses
`initial` to populate unbound forms; in a bound form it is only used for fields that are not
present in `data`. This should be harmless here, but it is worth confirming that
`entry.data` always contains every field key (including checkboxes/booleans that are absent
when unchecked). If a checkbox field is absent from `entry.data` (as is normal for unchecked
HTML checkboxes), the bound validation may incorrectly mark it as missing rather than False.

**File:** `form_manager/views/form_finalize.py`

#### 🟡 Medium — Inline `<script>` placement in template

The `<script>` block is placed *after* the closing `</div>` of the validation summary but
*before* `<c-accordion ...>`. It runs immediately on parse (no `defer`/`DOMContentLoaded`),
relying on the `div#form-validation-summary` already existing above it in the DOM. This is
fine because the element is rendered above it. However, placing script logic inline in a
Django template makes CSP hardening harder if a strict Content Security Policy is ever
applied. Consider moving this to a static JS file.

**File:** `form_manager/templates/form_manager/review_and_submit.html`

#### 🟢 Low — Double `requestAnimationFrame` is correct

Using `rAF(function() { rAF(function() { ... }) })` to ensure the painted state before
scrolling is a well-known browser idiom. The implementation is correct.

#### 🟢 Low — `role="alert" aria-live="polite"` combination

`role="alert"` implies `aria-live="assertive"` by default. Overriding with `aria-live="polite"`
is unusual and may result in inconsistent announcement behaviour across screen readers. Consider
either using `role="status"` with `aria-live="polite"` (for a non-urgent message) or
`role="alert"` alone (which defaults to assertive).

**File:** `form_manager/templates/form_manager/review_and_submit.html`

### Positive notes

- Blocking submission server-side (not only client-side) when the form is invalid is the
  correct defense-in-depth approach.
- Unit test `test_form_finalize_rejects_invalid_data_and_redirects_to_review` is well-structured
  and directly tests the redirect and the non-submission side-effect.
- Removing the dead `logger`, `schema.model_construct()`, and commented-out `# if form.is_valid()`
  code is good housekeeping.

---

## PR #213 — fix(form-manager): prune steps with no pages after field exclusion {#pr-213}

**Branch:** `fix/form-prune-empty-steps` → `main`  
**CI:** pre-commit ✅, **e2e-tests ❌ (failing)**  
**Created:** 2026-04-20, **last updated:** 2026-04-21 (3+ weeks stale)  
**Existing review:** No reviews submitted.

### What this PR does

- Adds `prune_steps_without_pages(steps)` to `navigation.py` — filters out steps that have no
  `AbstractPageBlock` children (e.g., after `remove_nodes_with_excluded_fields` runs).
- Calls the new function in `form_edit` before `normalize_step_and_page`, raising `Http404`
  if the result is empty.
- Removes the TODO comment that flagged this gap.
- Adds a unit test for `prune_steps_without_pages`.

### Findings

#### 🔴 High — e2e CI is failing

Same situation as PR #214 — the `e2e-tests` check failed on the initial push (2026-04-20) and
the branch has not been updated. Both PRs were opened on the same day and the failures likely
share a root cause (possibly the branch is not rebased against a recent `main`). The failure
must be investigated before merging.

#### 🟡 Medium — No test for the `Http404` path when all steps are pruned

The PR adds:
```python
ui_components = prune_steps_without_pages(ui_components)
if not ui_components:
    raise Http404("No form sections remain visible for this entry.")
```
but there is no unit test for this branch. An unexpected pruning could silently break a user's
form session. A test that configures all fields as excluded and asserts a 404 response would
provide a safety net.

**File:** `form_manager/views/form_edit.py` + `tests/unit/form_manager/test_navigation.py`

#### 🟡 Medium — Unit test uses `children=[]` not a realistically pruned step

```python
StepBlock(title="Dropped", children=[]),
```
In production, a dropped step would have had children (pages) that were removed by
`remove_nodes_with_excluded_fields`. The test does not cover this case — it should also test
a step whose children are all non-`AbstractPageBlock` nodes (e.g., `TextBlock`s) to ensure
`get_step_pages` returns `[]` for them and the step is correctly pruned.

**File:** `tests/unit/form_manager/test_navigation.py`

#### 🟢 Low — `prune_steps_without_pages` is called after `remove_nodes_with_excluded_fields`

The ordering in `form_edit` is correct: field exclusion first, then step pruning, then
step/page normalization. The comment update in `remove_nodes_with_excluded_fields` accurately
documents this.

#### 🟢 Low — `Http404` message is user-visible in DEBUG mode only

`Http404("No form sections remain visible for this entry.")` is safe; the message is only
surfaced in debug views, not in production 404 pages.

### Positive notes

- This is a clean, focused fix for a genuine bug (`normalize_step_and_page` would crash on an
  empty step) surfaced by a clear TODO.
- The `prune_steps_without_pages` function is simple, testable, and placed appropriately in
  `navigation.py` alongside `get_step_pages`.
- Removing the TODO + adding the explanatory comment is good maintenance.

---

## Cross-cutting observations

1. **PRs #213 and #214 are both 3+ weeks stale with failing e2e CI.** Neither has been updated
   since their initial push. They should be rebased on `main` and the CI failures investigated
   before they can be considered mergeable.

2. **Both #213 and #214 were "Made with Cursor"** (noted in PR bodies). Per `CLAUDE.md`, PR
   bodies should not include tool attribution. More importantly, both PRs lack a Jira link
   (`Jira: https://jira.acf.gov/browse/FE-XXX`) required by the conventions in `CLAUDE.md`.

3. **PR #242 is a draft** and should not be reviewed for merge yet. The changes are
   directionally sound.

4. **PR #261** is the only PR actively in review, has passing CI, and is closest to merge-ready.
   The two high-severity findings (template `inputmode` conflict and missing boolean "No" state
   in review) should be addressed before approval.
