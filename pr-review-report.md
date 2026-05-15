# PR Code Review Report

Generated: 2026-05-15

---

## PR #264 — Typed User Model (Draft)
**Author:** ryanbagwell | **Branch:** `typed-user-model` → `main`

### Summary
Introduces `django-typed-models` to create a polymorphic user hierarchy (`CoreUser` →
`RecipientUser` / `FederalStaffUser`). Adds `get_recipient_user_model()` and
`get_federal_staff_user_model()` static methods on `CoreUser`. Updates tests, management
commands, and the OIDC backend to create users through `RecipientUser` instead of
`CoreUser` directly.

### Issues

#### High
- **`Meta` class removed from `CoreUser` without explanation** — The original
  `class Meta(AbstractUser.Meta, BaseModel.Meta): abstract = False` was deleted. If
  `BaseModel.Meta` sets `ordering`, `default_manager_name`, or any other DB-level
  option, those are now silently lost. The PR description says nothing about this.
  Verify `TypedModel` doesn't conflict with those meta options, and if not, restore the
  explicit `Meta`.

#### Medium
- **Confusing `cast()` / name shadowing in `oidc_backend.py`** — Line:
  `CoreUser = cast("CoreUser", get_user_model())` rebinds the local name `CoreUser`
  (which is also the `TYPE_CHECKING`-only import) to an untyped runtime value. At
  runtime `cast()` is a no-op, so `CoreUser.get_recipient_user_model()` only works
  because `get_user_model()` happens to return the real `CoreUser` class. If
  `AUTH_USER_MODEL` were ever changed, this would blow up silently. Use a clearer name
  (e.g. `UserModel = get_user_model()`) and call `UserModel.get_recipient_user_model()`
  with an explicit type-ignore or forward reference.

- **Same pattern in `conftest.py`** — `User = cast("CoreUser", get_user_model())` —
  same concern as above; the cast is a lie the type checker accepts but at runtime it's
  just `get_user_model()`. Rename the local variable to avoid confusion.

- **`TypedModelManager` MRO with `BaseUserManager`** — `CoreUserManager` now inherits
  from both `TypedModelManager` and `BaseUserManager`. Both ultimately extend
  `django.db.models.Manager`. The MRO is `CoreUserManager → TypedModelManager →
  BaseUserManager → BaseUserManager → Manager`. Confirm there are no method conflicts
  (especially `create_user` / `create_superuser` which are only on `BaseUserManager`).
  A quick `python -c "from users.managers import CoreUserManager; print(CoreUserManager.__mro__)"` check is advisable.

- **No test for the new static methods** — `get_recipient_user_model()` and
  `get_federal_staff_user_model()` are used everywhere but there are no unit tests for
  them. A single test asserting the return value is `RecipientUser` / `FederalStaffUser`
  would provide a safety net against accidental refactors.

#### Low
- **`RecipientUser` and `FederalStaffUser` are empty** — Both subclasses just `pass`.
  That is fine for now, but it is worth a brief comment explaining the intended
  distinction (what makes a Federal Staff user different from a Recipient user) so
  future contributors know why the split exists.

- **Inline imports in test fixtures** — Several fixtures in `test_form_permissions.py`
  contain `from faker import Faker` inside the function body. CLAUDE.md requires all
  imports at the top of the file. This is pre-existing code, but the PR touches those
  functions; it would be clean to fix them in the same pass.

---

## PR #262 — [CORE-185] Form Card Markdown Formatting (Draft)
**Author:** LogvnR | **Branch:** `logvnr/core-185_form-card-formatting` → `main`

### Summary
Adds a `markdown` flag to `TextBlock` that renders text through Python-Markdown
(`sane_lists` extension) and marks the output safe. Converts
`_CSBG_ASSURANCES_NARRATIVE` to Markdown, adds SCSS for nested ordered lists, and
promotes `markdown` to a direct dependency.

### Issues

#### High
- **`mark_safe` without HTML sanitization** — `markdown_lib.markdown()` passes raw HTML
  through by default (even `<script>` tags). The `sane_lists` extension does not
  sanitize output. The current `_CSBG_ASSURANCES_NARRATIVE` is author-controlled and
  safe, but the template tag and `TextBlock` field are not technically constrained to
  static constants. Any future use with partially-dynamic content (e.g. a content
  editor populating `text` from the database) would be a direct XSS vector. Either:
  (a) add HTML sanitization with `bleach` or `nh3` before calling `mark_safe`, or
  (b) enforce in code (not just a docstring comment) that `markdown=True` is only
  reachable for values from a trusted constant (e.g. restrict to a specific Literal
  type or validator on `TextBlock`).

#### Medium
- **Inline CSP consideration** — No direct issue in this PR, but if the project ever
  adds `Content-Security-Policy: script-src 'self'` headers, `mark_safe` Markdown
  output containing `<script>` elements would be blocked. Document the dependency on
  CSP posture.

- **Return type annotation inaccurate** — `def markdown_filter(value: str) -> str`
  actually returns `django.utils.safestring.SafeString`. This is a subclass of `str`
  so it is not wrong, but type checkers that check Django template filters may warn.
  Use `-> SafeString` for precision.

#### Low
- **`markdown` version pin is a lower-bound only** — `"markdown>=3.10.2"` permits
  future major versions that could introduce breaking API changes. Consider
  `"markdown>=3.10.2,<4"` given that library major version bumps often change
  extension APIs.

- **SCSS nesting requires a modern CSS preprocessor** — The nested `.usa-prose { ol { ol { ... }}}` syntax is SCSS, which is fine given the project already uses it. No issue, just confirming it's not raw CSS.

---

## PR #242 — Reduce Wait Times (Draft)
**Author:** ryanbagwell | **Branch:** `speed-up-e2e-tests` → `main`

### Summary
Replaces many fixed `wait_for_timeout` calls in e2e tests with
`wait_for_load_state("networkidle")`, reduces some 500ms waits to 300ms, and adds
`--durations=15` to all pytest invocations.

### Issues

#### Medium
- **`wait_for_load_state("networkidle")` after `blur()`** — In
  `test_integer_field_formatting.py` at the end of the employment section,
  `page.locator('input[name="employment__unknown"]').blur()` is immediately followed by
  `page.wait_for_load_state("networkidle")`. A `blur` event triggers client-side
  JavaScript (Alpine.js), not a network request. `networkidle` may resolve before the
  JS completes its DOM updates, making this replacement flakier than the original
  `wait_for_timeout(1000)`. A short `wait_for_timeout(300)` is more appropriate after
  JS-only interactions.

- **Inconsistent strategy** — Some 500ms timeouts became `networkidle`, others became
  300ms, and a few 1000ms timeouts were left as-is (e.g. `page.wait_for_timeout(500)`
  still appears in several spots in `test_form_error_states.py` lines ~75 and ~220).
  A consistent rule (e.g. "use `networkidle` after navigation, `wait_for_timeout(300)`
  after JS-only interactions") would make the test suite easier to reason about.

#### Low
- **`-s` (no-capture) added to local unit test run** — `make test-unit` now passes
  `-s` to pytest. This suppresses output capture even for passing tests, which makes
  CI-style local runs noisier. Consider moving this to a separate `test-unit-debug`
  target if the intent is debugging.

- **`--durations=15` is a developer convenience** — Useful during active performance
  work but adds noise to routine CI output. Consider removing it from CI targets or
  gating it behind a `PYTEST_DURATIONS` env var.

---

## PR #214 — fix(form-manager): block finalize when invalid and scroll to banner
**Author:** mikewolfd | **Branch:** `fix/form-finalize-validation` → `main`
**Status:** Ready for review (not draft)

### Summary
Validates the full Django form in `form_finalize` before marking an entry as submitted.
On failure, redirects to the review page at `#form-validation-summary`. Adds a smooth
scroll/focus script in `review_and_submit.html`. Removes the old dead-code error path.
Adds a regression test.

### Issues

#### High
- **Inline `<script>` and CSP** — The scroll/focus logic is an inline `<script>` block
  inside `review_and_submit.html`. If the project sets or later adds a
  `Content-Security-Policy: script-src 'self'` header (common for gov-facing apps),
  inline scripts are blocked by default and require a `nonce` attribute or
  `'unsafe-inline'`. Move this logic to an external JS file (or the existing JS bundle)
  and trigger it based on the presence of `#form-validation-summary` in the URL on
  page load.

#### Medium
- **Unusual Django form instantiation** — `form = django_form_class(entry.data,
  initial=entry.data)` passes stored entry data as both the POST data (`data=`) and the
  initial values (`initial=`). Django `Form.__init__` treats `data` as submitted form
  data and `initial` as display-only defaults; they serve different purposes. If the
  intent is just to validate the stored data, only `data=entry.data` is needed.
  The redundant `initial=` is misleading (it has no effect on validation).

- **`use_default_if_excluded=True` is a non-standard `is_valid()` argument** —
  Django's `Form.is_valid()` takes no keyword arguments. This must be a custom override
  on the project's base form class. Confirm this is defined and tested; a typo here
  would silently fall through to the standard `is_valid()` without the exclusion logic.

- **Logging removed** — `import logging` and `logger = logging.getLogger(__name__)` were
  deleted from `form_finalize.py`. The view now has no observability when a finalize
  attempt fails validation. At minimum, add a `logger.info` or `logger.warning` when
  the form is invalid and the redirect occurs.

#### Low
- **`form_entry.status != "submitted"` string literal in test** — If `FormEntry.status`
  has choices (enum or `TextChoices`), use the constant
  (e.g. `FormEntry.Status.SUBMITTED`) rather than the bare string `"submitted"` to
  avoid test breakage on a rename.

- **`"Made with Cursor"` in PR body** — Minor: the PR description ends with "Made with
  [Cursor](https://cursor.com)". Per CLAUDE.md, PR bodies should not include tool
  attribution lines.

---

## PR #213 — fix(form-manager): prune steps with no pages after field exclusion
**Author:** mikewolfd | **Branch:** `fix/form-prune-empty-steps` → `main`
**Status:** Ready for review (not draft) | **Reviewer requested:** ryanbagwell

### Summary
Fixes an `Http404` that occurred when `fields_to_exclude` processing left a step with
zero pages. Adds `prune_steps_without_pages()` in `navigation.py` and calls it in
`form_edit` after field exclusion. Returns 404 if all steps are pruned. Adds a unit
test.

### Issues

#### Low (mostly clean)
- **No edge-case tests** — The unit test covers the happy path (mix of kept/dropped
  steps) but not:
  - An empty `steps=[]` input (returns `[]` — correct, but worth asserting).
  - A step whose `children` contains only non-`AbstractPageBlock` nodes (e.g. a lone
    `SectionBlock`) — `get_step_pages` would return `[]` and the step would be pruned,
    which may or may not be the desired behavior.

- **Http404 message could be more actionable** — `"No form sections remain visible for
  this entry."` is correct but unhelpful to an admin debugging why a form disappeared.
  Including the entry `pk` would aid log triage:
  `f"No form sections remain visible for entry {entry.pk}."`.

- **No integration test** — There is no test that exercises the full `form_edit` view
  path with `fields_to_exclude` causing all pages in a step to be removed and verifies
  the step is actually pruned. The unit test isolates the utility function well, but an
  integration test would guard against regressions in how `form_edit` wires everything
  together.

### Positive notes
- The implementation is minimal and correct — a single list comprehension that reuses
  the existing `get_step_pages` helper.
- The `TODO` comment in `remove_nodes_with_excluded_fields` was properly replaced with a
  description of the new behavior.
- Import grouping and formatting follow project conventions.

---

## Summary Table

| PR  | Title                                              | Status | Risk   | Ready to merge? |
|-----|----------------------------------------------------|--------|--------|-----------------|
| 264 | Typed User Model                                   | Draft  | Medium | No — needs Meta class review, cast cleanup |
| 262 | Form Card Markdown Formatting                      | Draft  | High   | No — XSS/sanitization concern |
| 242 | Reduce Wait Times                                  | Draft  | Low    | Near — fix networkidle-after-blur instances |
| 214 | block finalize when invalid + scroll to banner     | Open   | Medium | No — inline script CSP risk, logging removed |
| 213 | prune steps with no pages after field exclusion    | Open   | Low    | Near — add edge-case tests and pk in 404 message |
