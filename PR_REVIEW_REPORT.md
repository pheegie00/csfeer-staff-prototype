# Pull Request Review Report

Generated: 2026-05-15  
Repository: focusconsulting/csfeer  
Reviewed by: Claude Code (automated review — not yet posted to GitHub)

---

## Summary

| PR | Title | Author | Status | Severity |
|----|-------|--------|--------|----------|
| [#265](#pr-265) | Enhance documentation and add tests for semantic versioning | talebbits | Open | Medium |
| [#264](#pr-264) | Typed user model | ryanbagwell | Draft | **Critical** |
| [#262](#pr-262) | [CORE-185] Form Card Markdown formatting | LogvnR | Draft | High |
| [#242](#pr-242) | reduce wait times | ryanbagwell | Draft | Low |
| [#214](#pr-214) | fix(form-manager): block finalize when invalid and scroll to banner | mikewolfd | Open | Medium |
| [#213](#pr-213) | fix(form-manager): prune steps with no pages after field exclusion | mikewolfd | Open | Medium |

---

## PR #265 — Enhance documentation and add tests for semantic versioning {#pr-265}

**Branch:** `talebbits/core-23-test-coverage-for-template` → `main`

### Changes
Adds `__test__ = False` guards on Pydantic schema classes, a `TestSchema_3_1` sibling fixture,
and three new test files covering `SemVerField` validation, form versioning invariants, and
`load_initial_forms` management command behaviour. Also commits a new AI agent commit-skill file
and a AGENTS.md documentation rule.

---

### 🔴 Medium

**1. `order_by("variant")` on a VARCHAR is not semver-safe**  
_`tests/unit/form_manager/test_form_versioning.py:29`, `test_management.py:146`_

Both tests call `.order_by("variant")` on the `variant` column (a `CharField`/`VARChar`).
Lexicographic ordering breaks the moment any component reaches two digits —
`"10.0.0"` sorts before `"2.0.0"` alphabetically. The tests pass today only because
`"1"`, `"2"`, `"3"` compare correctly as single characters.

If this ordering pattern gets copied into production query code (e.g. to find the latest
version of a form) it will silently return the wrong row. Consider using `SPLIT_PART`/`CAST`
or padding to fixed-width segments for any query that depends on semver ordering.

---

**2. SKILL.md instructs `git add -A`, contradicting project policy**  
_`.agents/skills/commit/SKILL.md:45`_

The committed skill file says: "If there are only unstaged changes, stage everything (`git add -A`)."
`CLAUDE.md` explicitly prohibits `git add -A` / `git add .` because they can accidentally include
`.env` files or large binaries. The skill should match project policy — stage specific files by name.

---

### 🟡 Low

**3. `TribalShortForm_3_1` referenced in docstrings does not exist**  
_`use_test_schema.py:135`, `test_management.py:122`_

Both docstrings say "mirrors the real-world pattern of publishing a new version (see
`TribalShortForm_3_1`)" / "exercised by `TribalShortForm_3_1`". No such class exists in the
codebase. References to phantom identifiers mislead readers doing a grep.

**4. `family_prop.get("const") or family_prop.get("default")` silently resolves to `None`**  
_`test_management.py:85`_

If Pydantic v2 ever emits neither `"const"` nor `"default"` for a frozen enum field (it can
emit `"allOf"` + `"enum"` instead), both `.get()` calls return `None`, the assertion becomes
`definition.family == None`, and it passes silently instead of surfacing a schema-extraction bug.
Assert that at least one key exists before comparing.

**5. `type: ignore[attr-defined]` on `entry.form_definition_id` without explanation**  
_`test_form_versioning.py:52`_

The suppressed error should have a comment explaining *why* mypy can't see the attribute (likely
a django-stubs limitation for auto-generated `_id` fields on FK). Per `AGENTS.md`: "if you must
use `# type: ignore`, leave a comment as to why."

---

### ⚪ Nit

**6. `_make_definition("2.0.0")` return value discarded without comment**  
_`test_form_versioning.py:52`_

The intent is clear in context, but a one-line comment (`# create v2 to prove v1's FK is
unaffected`) would help future readers.

**7. `TestSchema_3_1` name violates PEP 8 CapWords convention**  
_`use_test_schema.py:134`_

Not a blocker, but if this naming pattern is intentional for versioned schema classes it should
be documented in `AGENTS.md` so contributors know it is deliberate.

---

## PR #264 — Typed user model {#pr-264}

**Branch:** `typed-user-model` → `main` (Draft)

### Changes
Introduces `django-typed-models` to give `CoreUser` a `type` discriminator column, with
`RecipientUser` and `FederalStaffUser` as proxy subclasses. Updates `CoreUserManager` to inherit
from `TypedModelManager`, adds two migrations, and threads `get_recipient_user_model()` calls
through the OIDC backend, `seed_test_users`, and test fixtures.

---

### 🔴 Critical

**1. `CoreUser.Meta` inherits `abstract = True` — no DB table will be created**  
_`users/models.py`_

The new `Meta` class is:
```python
class Meta(BaseModel.Meta, AbstractUser.Meta, TypedModel.Meta):
    pass
```
`BaseModel.Meta` (the project's `core.models.BaseModel`) has `abstract = True`, which is first
in the MRO. Without an explicit `abstract = False`, `CoreUser._meta.abstract` resolves to `True`
via Python MRO. Django will not create a `users_coreuser` table; every database query on
`CoreUser`, `RecipientUser`, or `FederalStaffUser` will fail with a `ProgrammingError`. The old
code had `abstract = False` explicitly and that line must be restored.

**2. `RecipientUser.objects.get_or_create(email=email)` will raise `IntegrityError` for federal staff logging in via OIDC**  
_`csfeer/auth_backends/oidc_backend.py`_

`TypedModelManager` appends `WHERE type = 'users.recipientuser'` to every query on
`RecipientUser.objects`. When a `FederalStaffUser` authenticates via OIDC, the `get_or_create`
call fails to find their existing row (type mismatch on the WHERE clause), then attempts to
INSERT a new row with the same email — hitting the `unique=True` constraint and raising an
unhandled `IntegrityError` that surfaces as a 500 error.

The lookup should use `CoreUser.objects.get_or_create(email=email)` (unfiltered base manager)
so existing users of either type are found. The `type` field should only be set when creating a
brand-new account (defaulting to `RecipientUser` for OIDC users if that is the intended policy).

---

### 🟠 High

**3. `TypedModel` as the rightmost base class may break the `typedmodels` metaclass machinery**  
_`users/models.py`_

`django-typed-models` works by having `TypedModel` at or near the root of the hierarchy so
`TypedModelMetaclass` (its custom `ModelBase`) runs first. Placing it rightmost in
`CoreUser(BaseModel, AbstractUser, TypedModel)` means the metaclass MRO is non-standard; the
`type` field injection, queryset filtering setup, and `__init_subclass__` hooks may not fire
correctly. The documented pattern is to inherit from `TypedModel` as the primary base. This
needs a test that actually verifies the `type` field is populated on save.

**4. `'typedmodels'` is likely missing from `INSTALLED_APPS`**  
_`csfeer/settings.py` (not changed in this PR)_

`django-typed-models` requires `'typedmodels'` in `INSTALLED_APPS` for its app-level setup
(migration discovery, signal registration). The PR adds the package to `pyproject.toml` but
does not update `INSTALLED_APPS`. If the app is absent, migrations may silently not include the
`type` column setup. Verify CI passes before merging.

**5. `seed_test_users` still creates users via `CoreUser.objects` — tests can't find them**  
_`users/management/commands/seed_test_users.py`, `tests/conftest.py`_

`seed_test_users` calls `UserModel.objects.create_user(...)` where `UserModel` is `CoreUser`.
With `TypedModel`, creating a user via the base class manager sets `type = ''` (no subtype).
The updated `conftest.py` then calls `RecipientUser.objects.get(email=...)`, which filters for
`type = 'users.recipientuser'` — the user exists in the DB but is invisible to that manager.
The fixture will raise `DoesNotExist` and every test depending on `create_user` will fail.
`seed_test_users` must use `RecipientUser.objects.create_user(...)` (or
`FederalStaffUser.objects` for staff).

---

### 🔴 Medium

**6. OIDC hard-codes `RecipientUser` for all new logins; federal staff get the wrong type**  
_`csfeer/auth_backends/oidc_backend.py`_

Every OIDC-authenticated user who does not already exist is created as `RecipientUser`. There
is no claim-based logic to assign `FederalStaffUser`. Any federal staffer logging in for the
first time gets `type = 'users.recipientuser'`, silently breaking any authorization that checks
`isinstance(user, FederalStaffUser)` or filters via the typed manager.

**7. `cast("CoreUser", get_user_model())` is a no-op — string argument is not a type**  
_`csfeer/auth_backends/oidc_backend.py`, `tests/conftest.py`_

`typing.cast` takes a **type** as its first argument, not a string literal. `cast("CoreUser",
...)` passes a `str`, which mypy/pyright treats as `cast(str, ...)` — providing no type
narrowing. The correct form is `cast("type[CoreUser]", get_user_model())`. Additionally, naming
the local variable `CoreUser` in `oidc_backend.py` shadows the `TYPE_CHECKING`-only imported
type, confusing type checkers in the surrounding scope.

**8. Two-migration approach leaves a window where `FederalStaffUser` accounts cannot be saved**  
_`users/migrations/0003_*`, `users/migrations/0004_*`_

Migration 0003 adds the `type` field with `choices` that only include `RecipientUser`. Migration
0004 adds `FederalStaffUser` to the choices. If 0003 applies on a server that has existing
`FederalStaffUser` accounts and 0004 fails, those rows will fail Django's `choices` validation
on next save. Both choices should be present from the start in a single migration, with a
`RunPython` backfill step for existing rows.

---

### 🟡 Low

**9. No admin registration for `RecipientUser` or `FederalStaffUser`**  
_`users/admin.py`_

Only `CoreUser` has an admin entry. Each subclass likely needs its own `ModelAdmin` (or at
minimum its own proxy model registration) so staff can filter and manage users by type in the
Django admin.

**10. `get_recipient_user_model()` / `get_federal_staff_user_model()` create hard coupling**  
_`users/models.py`_

These static methods on the parent class return concrete subclasses defined below it in the same
file, creating a forward-reference dependency. The conventional approach is to let callers import
the concrete models directly (`from users.models import RecipientUser`), which is both cleaner
and avoids the string-annotation gymnastics needed to satisfy the forward reference.

---

## PR #262 — [CORE-185] Form Card Markdown formatting {#pr-262}

**Branch:** `logvnr/core-185_form-card-formatting` → `main` (Draft)

### Changes
Adds a `markdown` boolean flag to `TextBlock`, a `|markdown` template filter backed by
`python-markdown` + `mark_safe`, CSS for nested ordered list numbering under `.usa-prose ol`,
and converts the `_CSBG_ASSURANCES_NARRATIVE` static text to Markdown format.

---

### 🟠 High

**1. `markdown.markdown()` passes raw HTML through; `mark_safe` makes this an XSS vector if ever misused**  
_`form_manager/templatetags/form_manager_tags.py`_

`markdown.markdown('<script>alert(1)</script>')` returns the `<script>` tag verbatim (no
escaping), and the filter wraps it in `mark_safe`. For the current use-case (static string
constants in `texts.py`) this is safe. The risk is the filter being added to a general-purpose
tag library that any future template author can apply to any value.

`safe_mode` was removed in python-Markdown 3.0. To make the filter inherently safe for future
callers, post-process the output with an HTML sanitiser (e.g. `bleach` or `nh3`) that strips
disallowed tags, or at minimum rename the filter to `static_markdown` to signal it is
intentionally restricted.

---

### 🔴 Medium

**2. No tests for the `markdown_filter` template tag**  
_`form_manager/templatetags/form_manager_tags.py`_

There are no unit tests verifying:
- `sane_lists` extension is applied (nested list numbering works as expected)
- `None` / empty string input returns an empty `SafeString` without raising
- Raw HTML is not passed through unescaped (catches any future sanitisation regression)
- The template renders the `{% if markdown %}` branch correctly end-to-end

Given the `mark_safe` boundary this warrants at least a smoke test.

---

### 🟡 Low

**3. No enforcement prevents the filter from being used on user-controlled content**  
_`form_manager/templatetags/form_manager_tags.py`_

The comment in the filter body warns against pointing it at user input, but the filter is
exposed in the shared tag library with no runtime guard. Renaming to `static_markdown` (or
restricting it to a separate, explicitly named tag library) would make misuse visually
obvious in template code review.

---

## PR #242 — reduce wait times {#pr-242}

**Branch:** `speed-up-e2e-tests` → `main` (Draft)

### Changes
Replaces most `page.wait_for_timeout(1000)` calls with `page.wait_for_load_state("networkidle")`
in e2e tests. Reduces some `wait_for_timeout(500)` → `wait_for_timeout(300)`. Adds
`--durations=15` and `-s` flags to Makefile test targets.

---

### 🔴 Medium

**1. `wait_for_load_state("networkidle")` after `.blur()` does not reliably wait for JS DOM updates**  
_`tests/e2e/test_integer_field_formatting.py` (line after `employment__unknown` blur)_

`networkidle` resolves when there are ≤ 2 in-flight network requests for 500 ms. A blur event
that triggers a purely client-side Alpine.js / JavaScript calculation completes synchronously or
via microtasks — there may be zero network activity, so `networkidle` resolves immediately before
the DOM has updated. The correct Playwright idiom is `expect(locator).to_have_value(...)` or
`page.wait_for_function(...)` targeting the specific DOM state being asserted.

---

### 🟡 Low

**2. `wait_for_timeout(800)` immediately after `page.expect_navigation()` is doubly redundant**  
_`tests/e2e/test_tribal_plan_form.py`_

`expect_navigation()` already waits for the navigation to complete. The subsequent
`wait_for_load_state("networkidle")` (added in this PR) is correct, but some tests retain a
preceding `wait_for_timeout(300)` that serves no purpose after `expect_navigation`. Minor nit,
but the PR's stated goal is to eliminate unnecessary waits.

**3. `-s` flag added to local `test-unit` make target permanently enables stdout capture**  
_`Makefile`_

`-s` disables pytest's stdout/stderr capture, which is useful for debugging but makes test
output significantly noisier for normal runs. This is usually a developer convenience flag
passed ad-hoc (`make test-unit TEST=... -s`) rather than baked into the target. CI correctly
omits `-s`.

---

## PR #214 — fix(form-manager): block finalize when invalid and scroll to banner {#pr-214}

**Branch:** `fix/form-finalize-validation` → `main`

### Changes
Fixes a critical bug where `form_finalize` was submitting entries regardless of validity (the
`if form.is_valid()` check was commented out). Adds validation before submission, redirects to
the review page with `#form-validation-summary` on failure, and adds a smooth-scroll inline
script + ARIA attributes to the review template.

---

### 🔴 Medium

**1. Inline `<script>` in `review_and_submit.html` will be blocked if CSP is ever added**  
_`form_manager/templates/form_manager/review_and_submit.html`_

The project currently has no Content Security Policy headers, so this works today. However,
adding an inline script creates a future migration burden — when CSP is introduced, this script
will need a nonce or be moved to an external file. Consider moving the scroll/focus logic to a
small external JS snippet (e.g. attached via an `x-data` Alpine attribute or a dedicated `.js`
file), which is also more consistent with how the rest of the UI is built.

---

### 🟡 Low

**2. `form = django_form_class(entry.data, initial=entry.data)` — `initial` is redundant**  
_`form_manager/views/form_finalize.py`_

Django's `initial` kwarg populates unbound form fields for display. For validation, only the
`data` positional argument matters. Passing `initial=entry.data` alongside `data=entry.data` is
harmless but semantically confusing — it suggests the form might be rendered here (it is not).

**3. Removing `import logging` / `logger` leaves no diagnostic trail on validation failure**  
_`form_manager/views/form_finalize.py`_

The `logger` was unused, so removing it is correct. However, the new validation branch
(`if not form.is_valid()`) now silently redirects without any server-side logging. A single
`logger.info` or `logger.warning` on the redirect path would help diagnose issues in production
(e.g. distinguishing intentional invalid submissions from configuration errors).

---

## PR #213 — fix(form-manager): prune steps with no pages after field exclusion {#pr-213}

**Branch:** `fix/form-prune-empty-steps` → `main`

### Changes
Adds `prune_steps_without_pages()` to `navigation.py`, calls it in `form_edit` after
`remove_nodes_with_excluded_fields`, and raises `Http404` if no steps remain. Includes a unit
test for the new function.

---

### 🔴 Medium

**1. `prune_steps_without_pages` is not applied in `form_review`**  
_`form_manager/views/form_edit.py` vs `form_review.py`_

`form_edit` now prunes empty steps, but `form_review.py` calls `remove_nodes_with_excluded_fields`
without the follow-up prune. This leaves `form_review` and `form_edit` with inconsistent step
counts after field exclusion: the side nav on the review page may still render empty sections,
and `build_review_sections` will generate section entries with zero field blocks for any pruned
steps. The fix should be applied symmetrically in `form_review.py`.

**2. `Http404` when all steps are pruned is poor UX**  
_`form_manager/views/form_edit.py`_

```python
if not ui_components:
    raise Http404("No form sections remain visible for this entry.")
```

A user whose form configuration legally excludes all fields receives a 404 — technically the
entry exists, the view just has nothing to show. A redirect to the review page (which renders
submitted data without requiring any visible edit sections) would be a more appropriate and
user-friendly response.

---

### 🟡 Low

**3. Test does not cover the case where children exist but none are `AbstractPageBlock` instances**  
_`tests/unit/form_manager/test_navigation.py`_

The test uses `StepBlock(children=[])` for the dropped step. `prune_steps_without_pages`
delegates to `get_step_pages`, which filters by `isinstance(child, AbstractPageBlock)`. A step
with non-page children (e.g. only `FieldBlock` or `SectionBlock`) would also be pruned, but that
path is untested. A stronger test would include such a step.

**4. No test for the `Http404` branch in `form_edit`**  
_`form_manager/views/form_edit.py`_

The new `if not ui_components: raise Http404(...)` path is reachable via normal user flow (all
fields excluded by configuration) but has no corresponding unit test. A regression could
silently revert to an unhandled `IndexError` in `normalize_step_and_page`.

---

## Cross-cutting observations

1. **Draft PRs (#264, #262, #242) should not be merged without resolving the critical/high issues
   above.** In particular, #264 has two critical correctness bugs that would break every user
   login.

2. **PR #214 and #213 are both non-draft and related** — they both touch `form_finalize` /
   `form_edit` / navigation. They should be merged in order (#213 before #214) or rebased
   together to avoid conflicts.

3. **Test coverage gap in #265**: The new test fixtures (`TestSchema`, `TestSchema_3_1`) use
   `__test__ = False` correctly. However, tests that call `order_by("variant")` on production
   models should be revisited if semver-ordered queries are ever needed in production code.
