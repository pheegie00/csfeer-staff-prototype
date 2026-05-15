# PR Code Review Report
Generated: 2026-05-15

---

## Summary Table

| PR   | Title                                        | Author        | Status    | Risk   |
|------|----------------------------------------------|---------------|-----------|--------|
| #267 | Update the ERDs diagram                      | ryanbagwell   | **Merged**| Low    |
| #266 | CORE-188 Auth error messaging (DRAFT)        | ryanbagwell   | Draft     | High   |
| #265 | core-23 Semantic versioning tests            | talebbits     | Open      | Low    |
| #264 | Typed user model (DRAFT)                     | ryanbagwell   | Draft     | Medium |
| #262 | CORE-185 Markdown formatting (DRAFT)         | LogvnR        | Draft     | Low    |
| #242 | Reduce E2E wait times (DRAFT)                | ryanbagwell   | Draft     | Low    |
| #214 | fix: block finalize when invalid             | mikewolfd     | Open      | Low    |
| #213 | fix: prune empty steps after field exclusion | mikewolfd     | Open      | Low    |

---

## PR #267 — Update the ERDs diagram (MERGED)
**Branch:** `update-erds` → `main` | Already merged.

### Changes
- Adds `"django_extensions"` to `INSTALLED_APPS` in `csfeer/settings.py`.
- Replaces `docs/app/erds/csfeer.png` (binary).

### Findings

**[Medium] `django_extensions` in production `INSTALLED_APPS`**
`django-extensions` ships powerful management commands (`shell_plus`, `runscript`,
`export_emails`, `graph_models`, etc.). Adding it unconditionally to `INSTALLED_APPS`
means these commands are available in every environment, including production.
Best practice is to guard it:
```python
if DEBUG:
    INSTALLED_APPS += ["django_extensions"]
```
or move it to a dev-only installed-apps list. This is already merged but worth
addressing in a follow-up.

---

## PR #266 — CORE-188 Auth Error Messaging (DRAFT)
**Branch:** `CORE-188/add-error-description` → `main`

### Changes
- New `csfeer/views.py` with `CoreAuthCallbackView` (overrides the OIDC library's
  `CallbackView`) and `HomePageView`.
- Overrides `authenticate_oauth2` in `EmailOIDCAuthenticationBackend` to block
  users with no org memberships.
- Replaces the dedicated `login-error/` page with inline error alerts on the home
  page, keyed by `login_error_source` query param.
- Deletes `csfeer/templates/login_error.html`.

### Findings

**[Critical Bug] `case "_":` is not a catch-all — `csfeer/views.py:44`**
```python
case "_":          # ← matches the literal string "_"
    login_error = None
    ...
```
In Python's `match` statement, a bare `_` (unquoted) is the wildcard. As written,
`"_"` is a string literal that only matches if `error_param == "_"`. Any unknown
`error_param` value will fall through without resetting `login_error*` variables.
Since they are initialized to `None` above the match block this particular bug is
non-fatal, but the intent is clearly a default case and the syntax is wrong.
**Fix:** `case _:` (no quotes).

**[Critical Bug] Malformed redirect URL — `csfeer/views.py:56-60`**
```python
url += "&" + urlencode({
    "login_error": login_error,
    ...
})
```
`get_redirect_url` from `CallbackView` typically returns a plain path like `/` or
`/forms/`. Appending `"&..."` to a URL that has no `?` produces an invalid URL
(e.g. `/?&login_error=...` is technically valid but unintended; a plain `/forms/`
would become `/forms/&login_error=...` which is broken). Use `urllib.parse` to
properly build query strings:
```python
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl
parsed = urlparse(url)
qs = dict(parse_qsl(parsed.query))
qs.update({"login_error": login_error, ...})
new_url = urlunparse(parsed._replace(query=urlencode(qs)))
```

**[Critical Bug] `login_error_source` never added to template context —
`csfeer/views.py:74-84` / `csfeer/templates/index.html:4-16`**
`HomePageView.get_context_data` adds `login_error` and `login_error_description`
but **not** `login_error_source`. The template conditions
`{% if login_error_source == "okta" %}` and `{% elif login_error_source == "app" %}`
will never be `True` (undefined template variables resolve to `""`), so neither
alert block will ever render.
**Fix:** add `"login_error_source": self.request.GET.get("login_error_source")` to
the context dict.

**[Medium] `logger.warn()` is deprecated — `csfeer/views.py:24` and
`csfeer/auth_backends/oidc_backend.py:83`**
`Logger.warn()` is a deprecated alias for `Logger.warning()`. Replace both calls.

**[Medium] Sensitive contact email hardcoded in template —
`csfeer/templates/index.html:10,18`**
`liane.peng@acf.hhs.gov` is a real person's government email address hardcoded
directly in a template. This creates maintenance burden and may be a privacy/policy
concern. Move it to a Django setting (e.g. `CORE_SUPPORT_EMAIL`) and reference it
via the template context.

**[Low] Missing `login_error_source` in `authenticate_oauth2` flow**
When `authenticate_oauth2` returns `None` due to no org memberships, the OIDC
library will pass `error=OIDC authent callback, no user error` to the callback.
`CoreAuthCallbackView.append_error_params` handles this case. However, the
authentication backend silently returns `None` — no session flag or structured
signal is set, so if the OIDC library's error string ever changes, the mapping
breaks silently. Consider a custom exception or a well-known sentinel to decouple
the two classes.

---

## PR #265 — core-23 Semantic Versioning Tests
**Branch:** `talebbits/core-23-test-coverage-for-template` → `main`

### Changes
- Adds `tests/unit/form_manager/test_form_versioning.py` (6 scenario tests).
- Adds `tests/unit/form_manager/test_semver_field.py` (5 unit tests for
  `SemVerField`).
- Extends `tests/unit/form_manager/test_management.py` with 4 new tests for
  `load_initial_forms`.
- Adds `empty_form_definitions` and `TestSchema_3_1` fixtures.
- Adds `__test__ = False` to Pydantic schema classes to stop pytest collecting them.
- Fixes typo `defintions` → `definitions` in `base.py`.
- Adds `.agents/skills/commit/SKILL.md` (custom agent skill).
- Updates `AGENTS.md` with Django docs reference rule.

### Findings

**[Low] Unrelated commit-skill file included in this PR —
`.agents/skills/commit/SKILL.md`**
This file is an agent configuration artifact unrelated to semantic versioning tests.
It inflates the PR scope and makes the diff harder to review. It should be in its
own PR (or omitted if it's auto-generated boilerplate).

**[Low] `test_semver_field_accepts_valid_versions` instantiates `FormDefinition()`
without `@pytest.mark.django_db`**
`FormDefinition()` is a Django model. If `FormDefinition.__init__` (or any
`__init_subclass__` logic) touches the database, these tests will fail with an
unclear error. The test currently passes only because the instantiation is
side-effect-free, but it is fragile. Consider passing `None` as the model argument
or constructing a mock, or explicitly marking with `@pytest.mark.django_db`.

**[Low] Fixture dependency clarity — `empty_form_definitions`**
The fixture deletes all `FormEntry` and `FormDefinition` rows in dependency order.
The docstring correctly explains the transaction rollback guarantee. No functional
issue, but the fixture should explicitly document that it requires the `db` fixture
(which it does via the argument) and be noted as unsafe for `transaction=True` tests.

**[Good]** `__test__ = False` on Pydantic classes is the correct fix for pytest
collection warnings. The `TestSchema_3_1` version-bumped sibling cleanly models the
real release pattern. Tests are well-scoped and non-overlapping.

---

## PR #264 — Typed User Model (DRAFT)
**Branch:** `typed-user-model` → `main`

### Changes
- Adds `django-typed-models>=0.16.0` dependency.
- Introduces `RecipientUser` and `FederalStaffUser` as `TypedModel` proxy subclasses
  of `CoreUser`.
- Adds static helper methods `get_recipient_user_model()` and
  `get_federal_staff_user_model()` on `CoreUser`.
- Migrations 0003 and 0004: add `type` discriminator column, create proxy models.
- Updates all test fixtures and `seed_test_users` to call
  `get_recipient_user_model().objects.create_user(...)` instead of
  `get_user_model().objects.create_user(...)`.
- Adds `type` and type filter to Django admin.

### Findings

**[Medium] Migration 0003 back-fills all existing users as `RecipientUser` —
`users/migrations/0003_recipientuser_coreuser_type.py:23-26`**
The `type` column is added with `default="users.recipientuser"` and
`preserve_default=False`, meaning every existing user row will be stamped with the
`RecipientUser` type. If there are any federal staff users already in production,
they will silently be re-typed as recipients. Verify that this is intentional (i.e.,
federal staff accounts don't exist yet in production), or add a data migration to
assign types based on group/role membership.

**[Medium] Complex MRO: `CoreUser(BaseModel, AbstractUser, TypedModel)` —
`users/models.py:14`**
The MRO places `BaseModel` before `AbstractUser` and `TypedModel`. `TypedModel`
uses a custom metaclass (`TypedModelMetaclass`); `AbstractUser` inherits from
Django's `Model`. Having three independent bases with their own metaclasses and
`Meta` classes is fragile. The `Meta` nesting `class Meta(BaseModel.Meta,
AbstractUser.Meta, TypedModel.Meta)` must be verified to resolve without conflicts.
If `TypedModel.Meta` introduces `abstract = True` or conflicting `ordering`, it
could silently change behavior. Test the migration and admin thoroughly.

**[Low] `get_recipient_user_model()` creates a forward reference in the class body**
```python
@staticmethod
def get_recipient_user_model() -> "type[RecipientUser]":
    return RecipientUser
```
`RecipientUser` is defined in the same file after `CoreUser`. At module load time,
by the time the static method is *called*, `RecipientUser` is defined — so this
works. However, it tightly couples the base class to its subclass, which is an
unusual design. A more conventional alternative is `apps.get_model("users",
"RecipientUser")` which avoids the coupling and is safer during migrations when the
model registry may not be fully populated. Worth noting for reviewers.

**[Low] Naming shadowing in `oidc_backend.py` — `csfeer/auth_backends/oidc_backend.py:69`**
```python
CoreUser = cast("CoreUser", get_user_model())
```
The local variable `CoreUser` shadows the `TYPE_CHECKING`-guarded import of
`CoreUser`. At runtime this is fine (cast is a no-op), but it is confusing to
readers who see `CoreUser` used as both a type and a runtime variable. Rename the
local to `User` or `UserModel` for clarity.

**[Good]** The admin additions (`type` column, `list_filter`) are clean. The
migration chain is straightforward.

---

## PR #262 — CORE-185 Form Card & Alert Markdown Formatting (DRAFT)
**Branch:** `logvnr/core-185_form-card-formatting` → `main`

### Changes
- New `<c-alert>` cotton component at `csfeer/templates/cotton/alert/index.html`.
- Adds `markdown` flag to `AlertBoxBlock` and `TextBlock` in `layout.py`.
- Adds `markdown_filter` template filter in `form_manager_tags.py`.
- Updates `alert.html` and `text_block.html` to render Markdown when the flag is set.
- Rewrites long-form legal text in `tribal_plan/texts.py` to use Markdown headings
  and nested lists.
- Adds SCSS for nested ordered-list numbering (decimal → alpha → roman) and
  `text-block__heading` styles.
- Adds `markdown>=3.10.2` dependency.

### Findings

**[Medium] `mark_safe` on markdown output — `form_manager/templatetags/form_manager_tags.py:14`**
```python
return mark_safe(markdown_lib.markdown(value or "", extensions=["sane_lists"]))
```
This is correctly guarded by comments ("author-controlled static content only").
However, there is no runtime check preventing the filter from being applied to
user-controlled data. If a developer in the future writes `{{ entry.data.field | markdown }}`
in a template, it would be a stored XSS vulnerability. Consider renaming the filter
to `static_markdown` or adding an assertion/raise if used in a context beyond
known-safe constants. At minimum, a prominent warning in the filter docstring
(already present) and a note in AGENTS.md.

**[Low] No tests for `markdown_filter`**
The templatetag is new logic. Basic tests (empty string, heading, nested list,
HTML-in-input stays escaped) would prevent regression. The `test_semver_field.py`
pattern in PR #265 shows the project already tests templatetag adjacents.

**[Low] Heading font style change — `form_manager/templates/form_manager/text_block.html:3`**
`font-heading-lg` is replaced with the custom `text-block__heading` class. The
new SCSS resets font-size, family, and weight to match body text rather than a
heading. This is a visual regression in non-markdown text blocks (those with
`markdown=False`), since the heading used to display as a large heading font but
will now display with body font weight/size. Verify that all existing usages of
`TextBlock` with a heading are intentionally reflowed.

**[Low] `{{ slot|safe }}` in the new `<c-alert>` component**
`csfeer/templates/cotton/alert/index.html` renders the slot with `|safe`. Cotton
slots are template-authored, so this is safe in practice. The comment in the filter
is the correct documentation.

**[Good]** The `sane_lists` markdown extension is the right choice for nested
ordered lists. The SCSS nested `ol` counter chain (decimal → lower-alpha →
lower-roman) precisely matches the legal text structure.

---

## PR #242 — Reduce E2E Wait Times (DRAFT)
**Branch:** `speed-up-e2e-tests` → `main`

### Changes
- Replaces `page.wait_for_timeout(1000)` / `wait_for_timeout(2000)` calls after
  navigation with `page.wait_for_load_state("networkidle")` across six E2E test
  files.
- Reduces some `wait_for_timeout(500)` calls to `wait_for_timeout(300)` for
  JS-only events (blur, Alpine.js updates).
- Adds `--durations=15` to all `pytest` invocations in `Makefile`.
- Adds `-s` (no output capture) to local test commands.

### Findings

**[Low] `wait_for_load_state("networkidle")` after a blur event may hang —
`tests/e2e/test_integer_field_formatting.py:237`**
```python
page.locator('input[name="employment__unknown"]').blur()
page.wait_for_load_state("networkidle")
```
Blurring an input triggers Alpine.js DOM updates but no network traffic. If the
app has any background polling or long-polling connection, `networkidle` will never
fire (Playwright defines it as no network connections for ≥500 ms). This specific
instance should stay as `wait_for_timeout(300)` or use `wait_for_function` to
check the computed total.

**[Low] Inconsistent timeout values for JS-event waits remain**
Some blur/JS-event waits were reduced to 300ms, others remain at 500ms
(e.g., `tests/e2e/test_form_error_states.py:75,220`). A project constant or fixture
helper would make these consistent.

**[Good]** Replacing `wait_for_timeout(1000)` after `expect_navigation` with
`wait_for_load_state("networkidle")` is the idiomatic Playwright pattern. The
change is mechanical and low-risk. `--durations=15` is a helpful CI addition.

---

## PR #214 — fix(form-manager): block finalize when invalid and scroll to banner
**Branch:** `fix/form-finalize-validation` → `main`

### Changes
- `form_finalize` now validates `entry.data` via the schema's form class before
  marking the entry submitted; on failure it redirects to the review page with the
  `#form-validation-summary` anchor.
- `review_and_submit.html` adds `id`, ARIA attributes, and a small inline script
  that smoothly scrolls to and focuses the error banner when the hash is present.
- Removes the unreachable dead-code error path (the old commented-out
  `if form.is_valid()` block and the `messages.error` redirect).
- Adds a regression test.

### Findings

**[Low] Inline `<script>` in a server-rendered template**
The `{% if form.errors %}...{% endif %}` guard ensures the script only appears on
error renders, which is correct. However, inline scripts can be tricky with
Content Security Policy headers. If CSP is ever tightened to disallow inline
scripts, this will silently stop working. Consider moving this to a small external
JS file or using a `nonce`-based CSP allowance.

**[Low] `form = django_form_class(entry.data, initial=entry.data)` —
`form_manager/views/form_finalize.py:36`**
Passing the same dict as both `data` and `initial` is unusual but not incorrect.
The form is bound (first arg is data), so `initial` has no effect on validation.
The `initial` kwarg is only used for unbound form rendering. Removing it would
simplify the call: `form = django_form_class(entry.data)`.

**[Good]** The fix correctly replaces the old unreachable `if form.is_valid():`
comment and the dead redirect. The double-`requestAnimationFrame` scroll pattern is
the correct cross-browser idiom. The regression test covers the redirect URL, the
status guard, and the audit trail non-creation.

---

## PR #213 — fix(form-manager): prune steps with no pages after field exclusion
**Branch:** `fix/form-prune-empty-steps` → `main`

### Changes
- Adds `prune_steps_without_pages(steps)` helper in `navigation.py`.
- Calls it in `form_edit.py` immediately after `remove_nodes_with_excluded_fields`.
- Raises `Http404` if the pruned list is empty.
- Removes the TODO comment that tracked this exact gap.
- Adds a unit test for `prune_steps_without_pages`.

### Findings

**[Low] No test for the Http404 path in `form_edit`**
The `prune_steps_without_pages` function is unit-tested, but the view-level behavior
(i.e., what happens when *all* steps are excluded and a 404 is raised) has no test.
A minimal integration test with a `fields_to_exclude` that drops everything would
complete the coverage.

**[Low] `prune_steps_without_pages` is not tested for steps with non-page children**
The existing test uses `children=[]`. A step could have non-`AbstractPageBlock`
children (e.g., section headers). Such a step would be pruned even if it had
non-page children. Confirm this is intentional — if headers can live in a step
without pages, they'd be silently dropped.

**[Good]** The function is simple, pure, and correctly placed in the call order
(after exclusion, before normalization). The removal of the TODO comment is
appropriate. The change is minimal and focused.

---

## Cross-cutting Observations

1. **`logger.warn()` deprecated** — appears in both `csfeer/views.py` and
   `csfeer/auth_backends/oidc_backend.py` (PR #266). Use `logger.warning()`.

2. **Inline imports** — `tests/unit/auth/test_form_permissions.py` still has
   `from faker import Faker` inside function bodies, violating the project's
   CLAUDE.md "No inline imports" rule. Not introduced by any current PR but
   worth a cleanup pass.

3. **PRs #213 and #214 are both from `mikewolfd` and both target the same stale
   base SHA** (`f34ff52672515f3a028c166cda76d841ac9b81a2`), which is several
   commits behind `main`. Both should be rebased before merge to avoid conflicts
   and to pick up the latest `form_edit.py` changes.

4. **DRAFT PRs (#266, #264, #262, #242)** are not ready for merge and are noted
   as works-in-progress. The findings above are intended to front-load feedback
   before the draft → ready transition.
