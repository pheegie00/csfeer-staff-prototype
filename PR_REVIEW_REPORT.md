# PR Code Review Report

**Date:** 2026-05-16  
**Repo:** focusconsulting/csfeer  
**Reviewer:** Claude (automated review, not posted to GitHub)

---

## Summary

| PR | Title | Author | Status | Severity |
|----|-------|--------|--------|----------|
| [#266](#pr-266) | CORE-188: Granular auth error messaging | ryanbagwell | Draft | 🔴 High |
| [#265](#pr-265) | core-23: Semantic versioning tests | talebbits | Ready | 🟡 Medium |
| [#264](#pr-264) | Typed user model | ryanbagwell | Draft | 🟡 Medium |
| [#262](#pr-262) | CORE-185: Form card & alert Markdown | LogvnR | Draft | 🔴 High |
| [#242](#pr-242) | Reduce E2E wait times | ryanbagwell | Draft | 🟢 Low |
| [#214](#pr-214) | fix: block finalize when invalid | mikewolfd | Ready | 🟡 Medium |
| [#213](#pr-213) | fix: prune steps with no pages | mikewolfd | Ready | 🟢 Low |

---

## PR #266 — CORE-188: Granular auth error messaging {#pr-266}

**Branch:** `CORE-188/add-error-description` | **Draft** | **Author:** ryanbagwell

### What it does
Replaces the generic `/login-error/` page with inline error alerts on the home page.
Adds a `CoreAuthCallbackView` to intercept the OIDC callback and append structured
error params (`login_error`, `login_error_description`, `login_error_source`) to the
redirect URL. Also blocks users with no org memberships from authenticating.

### 🔴 Bugs

**1. Runtime `NameError` on `authenticate_oauth2` return type annotation**  
File: `csfeer/auth_backends/oidc_backend.py`

```python
if TYPE_CHECKING:
    from users.models import CoreUser

def authenticate_oauth2(self, *args, **kwargs) -> CoreUser | None:
```

`CoreUser` is only imported inside `if TYPE_CHECKING:`, so it is `None` at runtime.
Python evaluates annotations eagerly (without `from __future__ import annotations`),
meaning this raises a `NameError` as soon as the module is imported.  
**Fix:** use a string annotation `-> "CoreUser | None"`.

**2. Wrong default case in `match` statement**  
File: `csfeer/views.py`, `append_error_params` method

```python
case "_":          # ← matches the literal string "_", NOT a catch-all
    login_error = None
    ...
```

In Python `match`, `case _:` (without quotes) is the wildcard. `case "_":` is a
literal string pattern. Any unrecognized error string (e.g. `"server_error"`) falls
through without resetting variables, so `login_error` / `login_error_source` stay
`None` only by accident (they were initialised to `None` above). This won't crash,
but the intent is clearly a default/catch-all case.  
**Fix:** remove the quotes: `case _:`.

**3. `login_error_source` never added to `HomePageView` context**  
File: `csfeer/views.py`, `HomePageView.get_context_data`  
File: `csfeer/templates/index.html`

```python
# views.py – only login_error and login_error_description are added
context.update({
    "login_error": ...,
    "login_error_description": ...,
})
```

```html
<!-- index.html checks login_error_source -->
{% if login_error_source == "okta" %}
{% elif login_error_source == "app" %}
```

`login_error_source` is missing from the context dictionary. Both conditional blocks
will always evaluate as falsy, so no error alert is ever rendered.

### 🟡 Code Quality

**4. `logger.warn` is deprecated (×2)**  
Files: `csfeer/auth_backends/oidc_backend.py` and `csfeer/views.py`

```python
logger.warn(f"User {user.email} is not assigned to any organization.")
logger.warn(request.GET.get("error"))
```

`Logger.warn` was deprecated in Python 3.2 and removed in 3.12. Use `logger.warning`.
Also, using f-strings in logging calls is a minor anti-pattern; prefer `%s` lazy
formatting: `logger.warning("User %s is not assigned to any organization.", user.email)`.

**5. Fragile URL mutation in `append_error_params`**  
File: `csfeer/views.py`

```python
url += "&" + urlencode({...})
```

This assumes the URL already contains a `?`. If for any code path `url` is plain
`/` (no query string), the result is `/&login_error=...` — a malformed URL. Use
`urllib.parse.urlsplit` / `urlencode` to build the query string properly, or at
minimum check `"?" in url` before choosing `&` vs `?`.

**6. `login_error_description` passed as `"None"` string**  
File: `csfeer/views.py`

When `error_param == "OIDC authent callback, no user error"`:
```python
login_error_description = "Your account isn't set up yet."
login_error_source = "app"
```
This branch is fine, but for `"access_denied"`:
```python
login_error_description = request.GET.get("error_description")  # may be None
```
Then `urlencode({"login_error_description": None})` encodes it as the literal string
`"None"`. The template should receive `None` (empty), not `"None"`.

**7. Hardcoded contact email in template**  
File: `csfeer/templates/index.html`

`liane.peng@acf.hhs.gov` appears twice. This should be a Django setting or
context variable rather than hardcoded in a template.

---

## PR #265 — core-23: Semantic versioning tests {#pr-265}

**Branch:** `talebbits/core-23-test-coverage-for-template` | **Ready for review** | **Author:** talebbits

### What it does
Adds comprehensive tests for `SemVerField`, `FormDefinition` multi-version coexistence,
and `load_initial_forms` idempotency. Also adds `__test__ = False` guards on Pydantic
schema classes to prevent pytest from collecting them, and commits a new agent skill file.

### 🟡 Code Quality

**1. `test_form_definition_unique_constraint_on_name_and_variant` missing `empty_form_definitions`**  
File: `tests/unit/form_manager/test_form_versioning.py`

```python
@pytest.mark.django_db
def test_form_definition_unique_constraint_on_name_and_variant():
    _make_definition("1.0.0")   # may collide with CI-seeded rows
    with pytest.raises(IntegrityError):
        ...
```

All other tests in this file use the `empty_form_definitions` fixture, but this one
does not. If the CI DB contains a pre-seeded `FormDefinition` with variant `"1.0.0"`
for `TRIBAL_ANNUAL_REPORT_3_0`, the first `_make_definition("1.0.0")` call will itself
raise `IntegrityError` before the test reaches the assertion.

**2. Agent skill file committed alongside feature code**  
File: `.agents/skills/commit/SKILL.md`

This file is unrelated to form versioning. It's a configuration file for AI coding
assistants and would be cleaner in its own PR or a dedicated chore commit.

### 🟢 Positive notes

- `__test__ = False` on Pydantic schema classes is the correct and idiomatic fix for
  pytest collecting them as test suites.
- Tests cover the full lifecycle: create, uniqueness constraint, PROTECT on delete,
  idempotent publish, and version-bump-without-mutating-prior.
- Fixtures are well-scoped and rollback-safe.

---

## PR #264 — Typed user model {#pr-264}

**Branch:** `typed-user-model` | **Draft** | **Author:** ryanbagwell

### What it does
Introduces `django-typed-models` to split `CoreUser` into `RecipientUser` and
`FederalStaffUser` proxy subtypes. Adds a `type` discriminator column. Updates test
fixtures and the user-seeding management command to create `RecipientUser` instances.

### 🟡 Code Quality

**1. Migration default assigns `RecipientUser` to all existing users**  
File: `users/migrations/0003_recipientuser_coreuser_type.py`

```python
field=models.CharField(
    ...
    default="users.recipientuser",
)
```

All existing `CoreUser` rows — including staff and superuser accounts — will be
migrated to type `RecipientUser`. Intentional? If staff/admin accounts should be
`FederalStaffUser`, a data migration is needed.

**2. `get_recipient_user_model()` / `get_federal_staff_user_model()` are static methods on the parent class**  
File: `users/models.py`

```python
class CoreUser(...):
    @staticmethod
    def get_recipient_user_model() -> "type[RecipientUser]":
        return RecipientUser
```

`CoreUser` depends on `RecipientUser` which subclasses `CoreUser`. This forward
reference works at runtime (the method body runs after class definition) but it
creates tight coupling. Consider using a registry or Django's `apps.get_model()`
pattern instead, which is more consistent with the existing `get_user_model()` usage
elsewhere.

**3. `cast("CoreUser", get_user_model())` pattern is confusing**  
Files: `csfeer/auth_backends/oidc_backend.py`, `tests/conftest.py`,
`users/management/commands/seed_test_users.py`

```python
CoreUser = cast("CoreUser", get_user_model())
RecipientUser = CoreUser.get_recipient_user_model()
```

A local variable named `CoreUser` shadows the TYPE_CHECKING import from
`users.models`. The string-form cast means the type checker gets no runtime help.
Since `get_user_model()` is well-typed via Django stubs, prefer:

```python
from users.models import RecipientUser
```

or just call `RecipientUser.objects.create_user(...)` directly where the import is safe.

**4. MRO / metaclass interaction deserves a comment**  
File: `users/models.py`

```python
class CoreUser(BaseModel, AbstractUser, TypedModel):
```

`django-typed-models` installs a custom metaclass. Combining it with Django's
`AbstractUser` metaclass and any metaclass from `BaseModel` can cause subtle
`TypeError: metaclass conflict` errors that only surface under certain Django/Python
versions. A brief comment explaining why the MRO is ordered this way would help future
maintainers.

**5. No admin registrations for `RecipientUser` / `FederalStaffUser`**  
File: `users/admin.py`

Only `CoreUser` is registered with `@admin.register(CoreUser)`. This means the Django
admin shows all users regardless of subtype under the "Core User" row. This may be
intentional for now, but should be documented.

---

## PR #262 — CORE-185: Form card & alert Markdown formatting {#pr-262}

**Branch:** `logvnr/core-185_form-card-formatting` | **Draft** | **Author:** LogvnR

### What it does
Adds a `markdown` Python library and a `|markdown` template filter. Allows
`AlertBoxBlock` and `TextBlock` schema fields to opt in to Markdown rendering.
Updates tribal plan legal text to use rich Markdown formatting. Adds a new Cotton
alert component with a `rich` mode for prose-formatted content.

### 🔴 Security

**1. `mark_safe` with no HTML sanitization**  
File: `form_manager/templatetags/form_manager_tags.py`

```python
@register.filter(name="markdown")
def markdown_filter(value: str) -> str:
    return mark_safe(
        markdown_lib.markdown(value or "", extensions=["sane_lists"]),
    )
```

The filter calls `mark_safe` on output from the `markdown` library. The `sane_lists`
extension only normalises list behaviour; it does **not** sanitize HTML. If Markdown
input contains raw HTML (e.g. `<script>alert(1)</script>`), it passes through
unchanged.

The comment says "do not point this filter at user input", but:
- The `markdown` boolean is a schema field that any author with admin access can set
  to `True`.
- There is no runtime enforcement preventing user-provided strings from being passed
  through the filter if the schema is configured incorrectly.

**Recommendation:** apply an HTML sanitization step (e.g. `bleach.clean`) after
`markdown_lib.markdown(...)` and before `mark_safe`, even for author-controlled
content. This provides defense-in-depth.

**2. `{{ slot|safe }}` in the Cotton alert component**  
File: `csfeer/templates/cotton/alert/index.html`

```html
<p class="usa-alert__text">
    {{ slot|safe }}
</p>
```

The slot content is unconditionally marked safe. This is correct for the current
callers (all render static strings or markdown-filtered content), but it makes the
component dangerous to reuse with any user-supplied slot content in the future.
A comment noting this constraint would prevent future misuse.

### 🟡 Code Quality

**3. Legal citation discrepancy: 676(b)(12) vs 676(b)(13)**  
File: `form_manager/schema/forms/tribal_plan/texts.py`

The old text cited `[per 676(b)(13)]` for the ROMA performance measurement assurance.
The new text cites `[per 676(b)(12)]`. If the authoritative CSBG Act citation is
`676(b)(13)`, this is a regression in a legal document. This should be verified
against the actual statute before merging.

**4. CSS class change on `TextBlock` heading**  
File: `form_manager/templates/form_manager/text_block.html`

```diff
-<h3 class="font-heading-lg margin-top-0 margin-bottom-2">{{ heading }}</h3>
+<h3 class="text-block__heading margin-top-0 margin-bottom-2">{{ heading }}</h3>
```

`font-heading-lg` is a USWDS utility class; `text-block__heading` is a custom class
defined in the SCSS. The visual result is different (the new SCSS uses
`font-size("heading", 8)` with `font-weight("normal")`). Any `TextBlock` with
a `heading` in forms other than tribal plan will be affected. This is a visual
regression risk with no associated test.

**5. `markdown` dependency has no upper bound**  
File: `pyproject.toml`

```toml
"markdown>=3.10.2",
```

The `python-markdown` library has had breaking API changes between major versions.
Consider pinning `>=3.10.2,<4` to prevent accidental breakage on a future major
release.

---

## PR #242 — Reduce E2E wait times {#pr-242}

**Branch:** `speed-up-e2e-tests` | **Draft** | **Author:** ryanbagwell

### What it does
Replaces fixed `page.wait_for_timeout(1000)` / `page.wait_for_timeout(2000)` calls
with `page.wait_for_load_state("networkidle")` in E2E tests. Reduces some 500ms
delays to 300ms. Adds `--durations=15` and `-s` flags to Makefile test targets.

### 🟡 Code Quality

**1. `networkidle` is unreliable for JavaScript-driven state changes**  
Files: `tests/e2e/test_integer_field_formatting.py`

```python
page.locator('input[name="employment__unknown"]').blur()
page.wait_for_load_state("networkidle")   # was: wait_for_timeout(1000)
```

`networkidle` waits for no active network connections for 500ms. After a `.blur()`,
the state change is driven by Alpine.js / JavaScript — no network request is fired.
`networkidle` may resolve immediately without waiting for the JS calculation to
complete. The original `wait_for_timeout(1000)` was more appropriate here (or a
specific locator assertion like `expect(total_field).to_have_value("...")`).

**2. `-s` flag added to `test-unit` in Makefile**  
File: `Makefile`

```makefile
docker compose run --rm app uv run pytest ${TEST:-tests/unit} -v -s --durations=15
```

`-s` disables pytest's output capturing, causing all `print()` statements and log
output to appear in CI logs. This will make CI output significantly noisier. Consider
removing `-s` from the default command or restricting it to local development.

**3. `networkidle` can be flaky in CI**  
`networkidle` is known to produce flaky results when apps make background requests
(health checks, polling). Event-based waits (`wait_for_selector`, `expect(...).to_be_visible()`)
are more deterministic. The approach is an improvement over arbitrary timeouts but
still carries flakiness risk.

---

## PR #214 — fix: block finalize when invalid {#pr-214}

**Branch:** `fix/form-finalize-validation` | **Ready for review** | **Author:** mikewolfd

### What it does
Validates the full form in `form_finalize` before marking a `FormEntry` as submitted.
On failure, redirects to the review page with a `#form-validation-summary` hash
fragment. Adds smooth-scroll JS to land the user on the error banner.

### 🟡 Code Quality

**1. `form.is_valid(use_default_if_excluded=True)` — non-standard argument**  
File: `form_manager/views/form_finalize.py`

```python
if not form.is_valid(use_default_if_excluded=True):
```

Django's `BaseForm.is_valid()` accepts no positional or keyword arguments. This
will raise `TypeError: is_valid() got an unexpected keyword argument` at runtime
unless the project's custom form class overrides `is_valid` with this signature.
This should be verified and, if the argument is needed, the custom signature should
be documented.

**2. `form = django_form_class(entry.data, initial=entry.data)`**  
File: `form_manager/views/form_finalize.py`

Passing `entry.data` as both `data` (first positional arg, bound form data) and
`initial` is unusual. Django treats `data` as the submitted POST data. Passing the
same dict for both is probably harmless here, but the intent — validating stored data
— is not obvious. A comment explaining why `initial` is also set would help.

**3. No HTTP method guard on `form_finalize`**  
File: `form_manager/views/form_finalize.py`

The view function does not check `request.method`. A GET request to the finalize
URL triggers the same validation-and-redirect or submit flow. If this should only
respond to POST, add:

```python
if request.method != "POST":
    raise Http404
```

**4. Inline script placement**  
File: `form_manager/templates/form_manager/review_and_submit.html`

The `<script>` block is inside the `{% if form.errors %}` block and placed above
the accordion content. This is intentional (scroll-to-error on load), and the double
`requestAnimationFrame` trick is a known pattern for post-render scroll. The
implementation is correct but tightly coupled to the `#form-validation-summary` ID —
worth a comment.

### 🟢 Positive notes

- Removing the dead commented-out `# if form.is_valid():` block is a clean improvement.
- ARIA attributes (`role="alert"`, `aria-live="polite"`, `tabindex="-1"`) on the
  error container are correct for accessibility.
- The regression test clearly validates the redirect URL, status code, and that the
  entry is not marked submitted.

---

## PR #213 — fix: prune steps with no pages {#pr-213}

**Branch:** `fix/form-prune-empty-steps` | **Ready for review** | **Author:** mikewolfd

### What it does
After `fields_to_exclude` processing, steps that have zero remaining pages now get
pruned. Raises `Http404` if all steps are removed. Adds `prune_steps_without_pages`
to `form_manager/schema/navigation.py`.

### 🟢 Low-severity notes

**1. Http404 message exposes internal logic**  
File: `form_manager/views/form_edit.py`

```python
raise Http404("No form sections remain visible for this entry.")
```

The HTTP 404 message string is visible to users in DEBUG mode. In production Django
suppresses it, but it is exposed in error logs and could leak business logic. Consider
a generic message or redirect to a user-friendly page.

**2. No test for the all-steps-pruned Http404 path**  
File: `tests/unit/form_manager/test_navigation.py`

The unit test for `prune_steps_without_pages` covers the function in isolation, but
there is no view-level test that exercises the `if not ui_components: raise Http404`
branch in `form_edit`. A view test with a form entry whose `fields_to_exclude` removes
every page would be a valuable addition.

### 🟢 Positive notes

- `prune_steps_without_pages` is clean, pure, and testable in isolation — good design.
- Replacing the TODO comment in `remove_nodes_with_excluded_fields` with accurate
  documentation is a nice housekeeping win.
- Resolves a real bug (`Http404` in `normalize_step_and_page`) without overengineering.

---

## Action Items by Priority

### Must fix before merge (🔴)

| PR | Issue |
|----|-------|
| #266 | `CoreUser \| None` return type annotation causes `NameError` at runtime |
| #266 | `case "_":` is a literal string match, not a catch-all — wrong default case |
| #266 | `login_error_source` missing from `HomePageView` context → alerts never shown |
| #262 | `mark_safe` without HTML sanitization — potential XSS if misused |

### Should fix before merge (🟡)

| PR | Issue |
|----|-------|
| #266 | `logger.warn` (deprecated) × 2; use `logger.warning` |
| #266 | `url += "&" + urlencode(...)` can produce malformed URL when no `?` present |
| #266 | `login_error_description` can serialize as the string `"None"` |
| #266 | Hardcoded contact email in template |
| #265 | `test_form_definition_unique_constraint` missing `empty_form_definitions` fixture |
| #264 | Default migration assigns all existing users to `RecipientUser` — verify intent |
| #264 | `cast("CoreUser", get_user_model())` pattern; prefer direct import |
| #262 | Legal citation 676(b)(12) vs 676(b)(13) — verify against statute |
| #262 | `font-heading-lg` → `text-block__heading` is a visual regression across all forms |
| #242 | `networkidle` after `.blur()` doesn't wait for JS — keep timeout there |
| #242 | `-s` flag in Makefile `test-unit` will produce very noisy CI logs |
| #214 | `form.is_valid(use_default_if_excluded=True)` — verify custom signature exists |
| #214 | No HTTP method guard on `form_finalize` |

### Nice to have (🟢)

| PR | Issue |
|----|-------|
| #265 | Agent skill file should be a separate PR / commit |
| #264 | MRO ordering deserves a comment |
| #264 | No admin registration for `RecipientUser` / `FederalStaffUser` |
| #262 | `markdown>=3.10.2` should have an upper bound (`<4`) |
| #262 | `{{ slot|safe }}` in alert component needs a hazard comment |
| #213 | Http404 message leaks internal logic |
| #213 | No view-level test for the all-steps-pruned path |
