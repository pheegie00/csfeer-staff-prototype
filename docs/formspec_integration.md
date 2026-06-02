# Formspec → CORE integration plan

Researched 2026-05-26. Source: https://github.com/focusconsulting/formspec

## TL;DR

**Formspec is exactly what `FormDefinition.schema` was waiting for.** It's a JSON-native form spec from Focus Consulting (same org as the csfeer upstream), with a pip-installable Python validator and a USWDS-themed web component for rendering. Federally compatible (Apache-2.0 runtime), and reuses the same Rust kernel on both client and server.

The smallest first step (~1 day) is loading a real Formspec doc into one existing FormDefinition row and adding a "View spec" button to Form Builder. After that, we can light up linting, real rendering, and server-side validation in 5-7 more days.

---

## What Formspec is

A JSON-native declarative form spec:

- Top-level: metadata envelope (`$formspec`, `version`, `status`, `title`, `optionSets`, `variables`, `items[]`)
- Fields, groups, displays, repeatables in a tree
- **FEL** (Formspec Expression Language) for computed fields + conditional visibility + cross-field validation
- Companion docs for theme (presentation), components (widget tree), mapping (response → CSV/XML)
- All 21 schemas under `schemas/` are Apache-2.0

## Python package — `formspec-py`

On PyPI as `0.1.0` (alpha, Python 3.12+, Apache-2.0). Built with maturin (Rust + PyO3) — wheels exist; falls back to building from source if no wheel matches the platform.

What we get out of the box:

| Capability | API | CORE use case |
|---|---|---|
| Lint a definition | `lint(definition, mode="authoring")` | Block publish on broken spec, surface diagnostics in Form Builder |
| Validate a response | `DefinitionEvaluator(definition).process(data)` | Defense-in-depth on `FormEntry.save()` |
| Evaluate FEL | `formspec.fel` | Computed fields, conditional visibility, cross-field rules |
| Bidirectional mapping | `execute_mapping` | Future-proof CSV/XML exports |
| Generate changelog | `generate_changelog(old, new, url)` | Auto-suggest semver bump on publish (currently manual) |
| Migrate response data | `apply_migrations_to_response_data` | Carry in-flight FormEntry drafts across version bumps |

**No Django integration ships in the package** — it's a plain library. We wire it through a thin service module.

## Rendering

**There is no server-side HTML renderer.** Runtime renderers are all JS:

- `@formspec-org/webcomponent` — `<formspec-render>` custom element
- `@formspec-org/react` — React renderer
- `@formspec-org/adapters` — includes a **USWDS adapter** (huge for us; matches our existing design language)
- `FormspecSwift` — iOS

Our path forward: **embed the web component** in a Django template. Load JS bundle + USWDS theme JSON, hand it the definition + saved partial response, POST the response JSON back to Django where `formspec-py` re-validates with the same Rust kernel.

## Licensing — green-light for the federal prototype

| Apache-2.0 (free use) | BSL 1.1 (source-available) |
|---|---|
| All schemas + specs | `@formspec-org/studio` (visual designer) |
| `formspec-py` | `@formspec-org/chat`, `@formspec-org/mcp`, `@formspec-org/assist` |
| `@formspec-org/webcomponent`, `react`, `adapters` (USWDS) | `formspec-changeset` |
| All Rust kernels | |

BSL permits internal use including federal/commercial — only blocks reselling form authoring to third parties. Auto-converts to Apache-2.0 on **2030-04-07**. **Form definitions you create are your data, not derivative works** — explicit in the license text.

Phases 1-3 below touch only Apache-2.0 code.

---

## Phased integration

### Phase 1a — Drop a real spec into one row (~1 day)

- Take `examples/grant-application/definition.json` from the formspec repo
- Save it as `FormDefinition.schema` on one existing FormDefinition row (e.g., the Tribal Plan)
- Add a "View spec" button to `form_builder_detail.html` that pretty-prints the JSON in a modal
- No new deps. Proves the model can hold a real spec and gives admins something to look at.

### Phase 1b — Lint definitions on save (~1 day)

- `pip install formspec-py` (verify wheel availability for `linux/amd64` Python 3.12 on Fly; add Rust to Docker if needed)
- New module `form_manager/services/formspec_service.py` exposing:
  - `lint_definition(schema_dict) → list[LintDiagnostic]`
  - `validate_response(schema_dict, data_dict) → ProcessingResult`
- On FormDefinition save: call `lint(schema, mode="authoring")`, surface diagnostics in detail page
- Block publish when severity is `error`

### Phase 2 — Render real forms on the recipient side (~3-5 days)

- Build JS bundle from `examples/uswds-grant` (Vite, ~50 lines) or vendor `@formspec-org/webcomponent` + `@formspec-org/adapters` via npm
- Stash bundle under `static/formspec/`
- New recipient view that loads `FormDefinition.schema` + any saved partial `FormEntry.data`, renders a Django template containing `<formspec-render>`
- Replace the hardcoded Tribal Plan template at `/forms/<id>/` with this
- Existing FormScoping + SubmissionWindow logic stays unchanged — only the render layer flips

### Phase 3 — Server-side response validation (~1 day)

- In `FormEntry.save()` or the submit view: call `validate_response(form_definition.schema, data)`
- If `not valid`, return errors to the renderer
- Persist `result.data` (post-NRB) rather than raw input

### Phase 3b — Bonus cheap wins

- Replace manual major/minor/patch picker in publish flow with `generate_changelog(old, new, url)` suggestion (closes part of Batch G's UX gap)
- Use `apply_migrations_to_response_data` when promoting drafts across version bumps

### Phase 4 — Visual editor (later, BSL-encumbered)

Two paths:
1. Embed `@formspec-org/studio` (BSL; fine for internal CORE staff use)
2. Build a Django-native field-list editor that emits Formspec JSON (Apache only)

Defer until Phases 1-3 prove the model.

---

## Risks

1. **Alpha version (0.1.0).** Pin it. Plan to track upstream.
2. **Build availability of the maturin wheel on our Fly.io image.** Verify before committing; if no wheel, we add Rust to the Docker build (adds ~200MB).
3. **Web component bundle size.** Need to measure; for federal accessibility we should also confirm the USWDS adapter ships ARIA + keyboard nav.

---

## How this maps to existing tickets

| Existing ticket | Formspec impact |
|---|---|
| **CORE-22** (FormScoping) | Unchanged — scope rules stay in `programs.FormScoping`, separate from form fields. |
| **CORE-23** (Publish new version) | Phase 3b replaces the manual semver picker with auto-suggest via `generate_changelog`. |
| **CORE-24** (Auto-close in-progress drafts) | `apply_migrations_to_response_data` lets us carry drafts across bumps instead of force-closing. |
| **CORE-25** (SubmissionWindow) | Unchanged. |
| **CORE-27** (Extensible form template schema) | Phase 1a is literally this ticket's acceptance criteria. |
| **CORE-28** (Document new form template pattern) | The "pattern" becomes: write a Formspec JSON doc and load it. Docs become a Formspec tutorial reference. |
| **CORE-46** (CSV exports) | Phase 3b: Formspec's `mapping` engine handles bidirectional response → CSV. |
| **STAFF-MP-13 (NEW)** | "Adopt Formspec as the form definition runtime" — file this. |

---

## Recommended next move

Start Phase 1a — drop the grant-application example into one row, add a View spec button. One hour of work, proves the path, and gives the team something concrete to react to before committing to the deps.
