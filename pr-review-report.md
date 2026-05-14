# Open PR Code Review Report
Generated: 2026-05-14

---

## PR #263 — make auth config compatible with okta locally
**Branch:** `okta-compat` → `main` | **Author:** ryanbagwell | **Status:** Open (non-draft)
**URL:** https://github.com/focusconsulting/csfeer/pull/263

### Summary
Two-file change: removes the `roles` scope from the default OIDC config, and adds
docker-compose environment overrides so local dev can point at an Okta IdP without
editing the code.

### Findings

**Medium — Hardcoded secret in version control**
`docker-compose-local.yml` sets `OIDC_CONFIG__client_secret` to the string literal
`shhhhhhhh` as the fallback default. Even though this is local-dev-only, committing
a default credential to version control is a bad habit and could be copied verbatim
into other environments. Prefer an empty-string fallback and document the expected
`.env` key in `.env.example` (or equivalent).

**Medium — Removed `roles` scope may break RBAC**
The `roles` scope was dropped from `OIDCConfig.scopes` with no explanation in the PR
body or commit message. If the app depends on the OIDC provider including role claims
in the token (common in Keycloak), removing this scope will cause those claims to be
absent at runtime. No corresponding change to role-claim handling or tests is present.
The scope removal should be explicitly justified or gated behind an env override rather
than changing the shared default.

**Minor — PR metadata doesn't meet project conventions**
- Title doesn't follow the `<type>(<scope>): [FE-<issue>] <description>` format.
- No Jira link in the PR body (required by CLAUDE.md).
- No PR description explaining why `roles` was removed or what Okta compatibility
  required.

---

## PR #262 — [CORE-185] Form Card Markdown formatting
**Branch:** `logvnr/core-185_form-card-formatting` → `main` | **Author:** LogvnR | **Status:** Draft
**URL:** https://github.com/focusconsulting/csfeer/pull/262

### Summary
Adds a `markdown` flag to `TextBlock`, a corresponding Django template filter, nested
ordered-list CSS, converts `_CSBG_ASSURANCES_NARRATIVE` to Markdown, and promotes
`markdown` to a direct dependency.

### Findings

**Medium — `mark_safe` on a generic, reusable field is an XSS footgun**
The `markdown` filter calls `mark_safe()` unconditionally. The flag is documented as
"for author-controlled static content only," but `TextBlock.markdown` is a regular
Pydantic field that any developer can set to `True` on any text value. There is no
runtime enforcement. If a future developer passes user-supplied text to a `TextBlock`
with `markdown=True`, the result will be rendered as raw HTML — a stored XSS
vulnerability. Consider a stricter design: either make the filter private/internal,
remove the `markdown` field from the public schema entirely (render-time logic instead),
or add a runtime assertion that the content is one of the known static constants.

**Minor — Markdown library passes raw HTML through by default**
`markdown.markdown()` does not strip embedded HTML tags by default. If the static
constant ever accidentally contains an HTML tag (e.g., a stray `<br>`), it will render
as-is. This is low risk for static constants but worth noting.

**Minor — Global CSS override for `.usa-prose ol` affects all ordered lists**
The new SCSS nesting (`decimal` → `lower-alpha` → `lower-roman`) applies to every
`ol` inside `.usa-prose`, not just markdown-rendered content. Any existing numbered
list in a prose area will now be re-styled by depth. If there are other ordered lists
on the form rendered via Django template (not Markdown), their nesting style will
silently change. Consider scoping to a class like `.usa-prose--markdown ol` or checking
that no other `ol` nesting currently exists in prose areas.

**Minor — No unit tests for the new `markdown` filter or `TextBlock.markdown` field**
The template tag and the `TextBlock` field desertion have no unit tests. A basic test
confirming Markdown output is rendered and `mark_safe` is returned would guard against
regressions.

**Minor — Markdown auto-numbering replaces explicit letter/roman sub-lists**
The original text had explicit `a.`, `b.`, `c.` and `i.`, `ii.`, `iii.` list items.
These are now all `1.` in the source, relying on CSS `lower-alpha`/`lower-roman` to
visually differentiate levels. This is fine if the CSS always loads, but the semantic
numbering is lost if CSS is unavailable (print, screen readers). Whether that matters
for accessibility/compliance is worth confirming.

---

## PR #242 — reduce wait times
**Branch:** `speed-up-e2e-tests` → `main` | **Author:** ryanbagwell | **Status:** Draft
**URL:** https://github.com/focusconsulting/csfeer/pull/242

### Summary
Replaces many `page.wait_for_timeout(1000)` / `wait_for_timeout(500)` calls in e2e
tests with `page.wait_for_load_state("networkidle")`, and reduces the remaining
arbitrary timeouts. Adds `--durations=15` and `-s` to pytest invocations.

### Findings

**Positive — Good use of event-driven waits**
Replacing fixed `sleep`-style timeouts with `wait_for_load_state("networkidle")` is
the right direction: tests become faster on fast machines and more reliable on slow
ones.

**Minor — `wait_for_load_state("networkidle")` can be fragile with Alpine.js**
`networkidle` fires when no network requests have been in-flight for 500 ms. Alpine.js
and HTMX-style apps that trigger XHR on input blur could restart the clock
unpredictably. If the e2e suite becomes flaky after this PR lands, the
`wait_for_load_state("domcontentloaded")` or an explicit element-visible assertion
may be more stable.

**Minor — `-s` (no stdout capture) added to local unit test run (`test-unit` target)**
This leaks all `print()` / logging output to the terminal during regular local unit
test runs, which can be noisy and obscure test failures. It is absent from the
`test-unit-ci` target (correct), but may be unintentional for local Docker runs.

**Minor — A few arbitrary timeouts remain without explanation**
Several `wait_for_timeout(300)` and `wait_for_timeout(500)` calls remain in places
that were not converted (e.g., `test_integer_field_formatting.py` line ~65 and ~96).
Adding a brief comment explaining why a fixed pause is still needed (e.g., "wait for
Alpine.js to process the change event") would make the intent clear.

---

## PR #214 — fix(form-manager): block finalize when invalid and scroll to banner
**Branch:** `fix/form-finalize-validation` → `main` | **Author:** mikewolfd | **Status:** Open (non-draft)
**URL:** https://github.com/focusconsulting/csfeer/pull/214

### Summary
Adds server-side validation in `form_finalize` before marking an entry submitted;
redirects to review page with `#form-validation-summary` hash on failure. Adds ARIA
attributes and a smooth-scroll script to the review page. Removes dead code from the
old (never-executed) error path.

### Findings

**Medium — `django_form_class(entry.data, initial=entry.data)` — unusual form binding**
Django forms expect their first positional argument (`data`) to be a `QueryDict` (from
`request.POST`), not a plain `dict`. Passing a plain dict will bind the form but
Django's multivalue handling and `_raw_value()` may behave differently. The `initial`
keyword is also typically for pre-populating an *unbound* form, not a bound one.
Depending on how `get_form_fields_class()` constructs the form, this could cause
`is_valid()` to behave unexpectedly (e.g., treating missing keys as blank submissions
vs. unchanged values). Needs a test covering a *valid* entry to confirm `is_valid()`
returns `True` and the finalize succeeds.

**Minor — `is_valid(use_default_if_excluded=True)` is a non-standard signature**
This custom kwarg implies a project-specific `is_valid` override. Confirm it is
documented and that it interacts correctly with the new `initial=entry.data` argument
above — the interaction between custom kwargs and bound-form initialization is easy
to get wrong.

**Minor — Inline `<script>` tag in a Django template**
The scroll/focus script is inlined directly in the HTML. This is functional but
bypasses any Content Security Policy that restricts `script-src 'self'` without
`'unsafe-inline'`. Check that the project's CSP (if any) allows inline scripts, or
move the logic to a JS module.

**Minor — No Jira link in PR body**
Per CLAUDE.md, PR bodies must include a Jira link at the bottom. This PR (and #213
below) has "Made with Cursor" but no Jira reference.

**Positive — Dead code cleanly removed**
The old commented-out `if form.is_valid():` and unreachable `messages.error()` block
are properly cleaned up. The new code path is straightforward.

**Positive — ARIA attributes are correct**
`role="alert"` + `aria-live="polite"` on the error container is appropriate for
dynamic error injection.

---

## PR #213 — fix(form-manager): prune steps with no pages after field exclusion
**Branch:** `fix/form-prune-empty-steps` → `main` | **Author:** mikewolfd | **Status:** Open (non-draft), reviewer: ryanbagwell
**URL:** https://github.com/focusconsulting/csfeer/pull/213

### Summary
Introduces `prune_steps_without_pages` in `navigation.py` and calls it in `form_edit`
after field-exclusion processing, resolving a `Http404` that occurred when all pages
in a step were excluded.

### Findings

**Positive — Clean, minimal implementation**
The function is a one-liner list comprehension that directly addresses the bug. The
TODO comment in the old docstring is correctly resolved and removed.

**Positive — Good unit test**
`test_prune_steps_without_pages_removes_steps_with_no_pages` covers the core case
(kept, dropped, kept) with clear assertions.

**Minor — Edge case: step with only non-page children**
`prune_steps_without_pages` relies on `get_step_pages`, which filters for
`AbstractPageBlock` instances. A step containing only non-page children (e.g., a
`SectionBlock` at the step level, if that's ever possible) would be correctly dropped.
Worth confirming via the schema that step children are always pages or always
mixed-type, so the pruning behavior matches all real-world configurations.

**Minor — No Jira link in PR body**
Same as #214 — "Made with Cursor" but no Jira link per project conventions.

**Minor — `Http404` message exposes internal state**
`raise Http404("No form sections remain visible for this entry.")` includes the phrase
"for this entry" which, combined with the entry PK in the URL, leaks information about
the entry's existence and visibility. Consider a more generic message or no message
for `Http404`.

---

## Cross-cutting Observations

1. **PRs #213 and #214 are production-ready** (non-draft, tested, clean diffs).
   PR #213 has a requested reviewer. Both are missing Jira links per CLAUDE.md policy.

2. **PRs #262 and #242 are still drafts** — likely not ready for full review, but the
   findings above apply when they're promoted.

3. **PR #263** is newly opened with no description and needs clarification on the
   `roles` scope removal before merging.

4. **`mark_safe` in PR #262** is the highest-severity finding across all PRs and
   deserves explicit team discussion before the draft is promoted.
