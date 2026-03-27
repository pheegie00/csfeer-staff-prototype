# Greenfield Comparative Analysis: Form Definition & Validation Engines

> Evaluating tools for Layer 1 (Field Definitions) and Layer 2 (Validation Rules) against [FRAMEWORK_REQUIREMENTS.md](prd/FRAMEWORK_REQUIREMENTS.md).
> Companion to: [form-engine-roadmap.md](form-engine-roadmap.md), [fhir-r5-analysis.md](fhir-r5-analysis.md), [simpler-grants-analysis.md](simpler-grants-analysis.md), [jsonforms-analysis.md](jsonforms-analysis.md), [shacl-analysis.md](shacl-analysis.md)

---

## Scope: What Are We Evaluating?

From the [form engine roadmap](form-engine-roadmap.md), the bottom two layers are:

- **Layer 1 — Field Definitions:** Pure descriptions of form fields — names, types, constraints, metadata, calculated-from references, conditional visibility. No rendering, no behavior. Serializable to JSON.
- **Layer 2 — Validation Rules:** A rules engine that operates on field values and produces typed results (errors, warnings) without any knowledge of how those results will be displayed.

Layout (Layer 3) and rendering (Layer 4) are out of scope. We're asking: **if we were starting fresh, which tool best handles field definition and validation for complex government financial forms?**

### The Four Stress Points

From FRAMEWORK_REQUIREMENTS.md, the hardest problems for any tool:

1. **Auto-calculated fields** with cross-field formulas (e.g., `personnel + equipment + travel = total`)
2. **Dual severity validation** — hard errors block submission, warnings inform only, partial saves never blocked
3. **Multi-version form definitions** with submission pinning (responses locked to the version they were created with)
4. **Real-time validation with prior-year comparison** and external data integration (SAM.gov UEI checks)

---

## Tools Evaluated

| Tool | Category | License | Language |
|---|---|---|---|
| **Orbeon Forms / XForms** | Full-stack form platform (XML) | CE: open-source; PE: $1,300–$6,300/server/year | Java/XForms XML |
| **ODK XLSForm / pyxform** | Form compiler + mobile data collection | Apache 2.0 | Python (compiler), Java/JS (runtime) |
| **FHIR Questionnaire + SDC** | Healthcare data collection standard | Open standard | Spec only; Python libs exist |
| **Form.io / formio.js** | JSON-based form platform | Renderer: MIT; Server: OSL-v3 | JavaScript/Node.js |
| **SurveyJS** | Commercial form/survey library | Free (essential) to $2,399+ (enterprise) | JavaScript (core is framework-agnostic) |
| **JSON Forms** (EclipseSource) | Dual-schema renderer | MIT | JavaScript (React/Angular/Vue) |
| **Pydantic + custom engine** | Build from scratch in Python | MIT | Python |
| **formio-data** (Python) | Server-side Form.io schema processor | MIT | Python |

---

## Tool-by-Tool Assessment

### 1. Orbeon Forms / W3C XForms

**What it is:** The most complete XForms implementation. Server-side Java runtime with visual Form Builder and Form Runner. 15+ year government deployments (Swiss insurance, City of Brussels, VA TRM-listed).

**Layer 1 — Field Definitions:**
XForms' `bind` concept is the most complete declarative field model ever produced. A single bind declaration per field carries `calculate`, `constraint`, `relevant` (conditional visibility), `required`, and `readonly` — all as reactive XPath expressions. Repeatable sections (`xforms:repeat`) are first-class. Non-relevant fields are excluded from submitted data, not just hidden.

**Layer 2 — Validation:**
`constraint` expressions with `alert` messages provide field-level and cross-field validation. Validation is reactive — recomputed when dependencies change. However, all validation is binary (valid/invalid). **No severity levels.** No warning concept.

**Stress point coverage:**
- Calculated fields: **Full** — `calculate` bind with XPath expressions, reactive dependency graph
- Dual severity: **None** — binary valid/invalid only
- Versioning: **None** — no native version management
- Prior-year/external: **Partial** — secondary instances can hold external data, but no structured pattern

**Showstoppers for CSFEER:**
- XML-only. Forms defined in XForms XML, data exchanged as XML. JSON conversion exists but is a boundary translation, not native.
- Requires JVM runtime (Orbeon runs on Tomcat/WildFly). Cannot run inside Django.
- PE pricing ($4,200+/server/year for production) adds recurring cost with no Python integration.
- No headless validation mode — forms require the server-side Form Runner UI runtime to function.
- XPath expressions are verbose for financial arithmetic (`../personnel + ../equipment` vs `${personnel} + ${equipment}`).

**Verdict:** The *model* is excellent — the unified bind concept is the right abstraction. The *implementation* is wrong for our stack. **Borrow the concepts, don't adopt the tool.**

---

### 2. ODK XLSForm / pyxform

**What it is:** A spreadsheet-based form authoring tool that compiles to XForms XML. Battle-tested by WHO, UNICEF, World Bank for field data collection. pyxform is the Python compiler.

**Layer 1 — Field Definitions:**
Three-column architecture (`type | name | label`) with `calculation`, `constraint`, `relevant` columns. The `${field_name}` reference syntax is cleaner than XPath. Supports repeatable groups, cascading selects, and conditional logic.

**Layer 2 — Validation:**
`constraint` + `constraint_message` columns provide inline validation. `calculation` column for computed fields. Same binary valid/invalid as XForms — no severity levels.

**Stress point coverage:**
- Calculated fields: **Full** — `${item_a} + ${item_b} + ${item_c}` syntax, clean and readable
- Dual severity: **None** — binary only
- Versioning: **Weak** — free-text `version` string, no semver, no response pinning
- Prior-year/external: **None** — no structured cross-form data pattern

**Showstoppers for CSFEER:**
- **pyxform is a compiler, not an evaluator.** It converts XLSForm → XForms XML. It cannot evaluate expressions, run validation, or compute calculated fields. There is no Python library that evaluates ODK expressions against JSON data.
- Runtime evaluation happens in ODK Collect (Android/JavaRosa) or Enketo (JavaScript/browser). Neither runs server-side in Python.
- Mobile-first design assumptions (offline collection, GPS, barcodes) don't match desktop government form entry.

**Verdict:** The `${field_name}` expression syntax is the right choice for our DSL. The tool itself is unusable — it's a compiler with no server-side evaluation engine. **Borrow the syntax, not the tool.**

---

### 3. FHIR Questionnaire + SDC

**What it is:** HL7's healthcare data collection standard. FHIR R5 Questionnaire defines form structure; SDC (Structured Data Capture) IG adds calculated fields, pre-population, extraction, and modular composition.

**Layer 1 — Field Definitions:**
Rich item types (text, decimal, choice, date, etc.). `enableWhen` provides declarative conditional logic (tier 1: field comparisons with operators). `enableWhenExpression` (SDC) handles complex conditions via FHIRPath (tier 2). `item.repeats` for repeatable sections (boolean flag — less powerful than XForms' `repeat`). `disabledDisplay` distinguishes `hidden` vs `protected` (visible but locked).

**Layer 2 — Validation:**
Basic required/maxLength in core spec. SDC adds `calculatedExpression` for computed fields and `constraint` extensions. Validation is binary — **no severity levels.** FHIRPath expressions are verbose for financial arithmetic (`%resource.item.where(linkId='x').answer.value` vs `${x}`).

**Best-in-class versioning:**
```
canonical URL + semver + versionAlgorithmCoding + derivedFrom + response version pinning
```
This is the most mature versioning model in any standard surveyed. Responses pin to a specific definition version via canonical URL with version suffix (`|2.1.0`).

**Stress point coverage:**
- Calculated fields: **Full** — `calculatedExpression` with FHIRPath, but syntax is verbose for financial math
- Dual severity: **None** — binary valid/invalid
- Versioning: **Full** — best-in-class canonical URL + semver + derivedFrom + response pinning
- Prior-year/external: **Partial** — `initialExpression` + `launchContext` for pre-population; `$populate` operation

**Showstoppers for CSFEER:**
- **No Python evaluation engine.** Python FHIR libraries (`fhir.resources`, `fhirclient`) validate FHIR resource *structure* — they don't evaluate `enableWhen` conditions, `calculatedExpression` formulas, or `constraint` rules against response data. You'd build the entire evaluation engine yourself.
- FHIRPath is verbose and healthcare-centric. `%resource.item.where(linkId='budget_total').answer.value` vs `${budget_total}`.
- Healthcare assumptions throughout (subjectType, coding terminology, FHIR resource references).
- No confirmed non-healthcare production deployments found.

**Verdict:** The versioning model is best-in-class and should be adopted wholesale. The conditional logic tiers (simple declarative + complex expression) are a good pattern. But the spec is a definition format, not a runnable engine — and no Python engine exists. **Borrow versioning + conditional tiers, not the format.**

---

### 4. Form.io / formio.js

**What it is:** A JSON-based form platform. formio.js (MIT) is the client-side renderer/validator. Form.io (OSL-v3) is the server platform. v5.9.x as of mid-2025, actively maintained.

**Layer 1 — Field Definitions:**
JSON schemas define forms with typed components (textfield, number, select, datetime, currency, etc.). Supports calculated values via JavaScript expressions or JSON Logic. Conditional logic via Simple Conditions and a Logic feature (rules engine for field settings, schema modifications, data values, custom events). Nested structures (panels, datagrid, editgrid).

**Layer 2 — Validation:**
Custom validation via JavaScript or JSON Logic. Required, min/max, unique, pattern, custom validators. **No severity levels** — validation is binary (returns true or error message string). No warning concept.

**Python integration via formio-data:**
[formio-data](https://github.com/novacode-nl/python-formio-data) is a third-party Python package that processes Form.io JSON schemas server-side:
- `Builder(schema_json)` → parses form definition
- `Form(builder, submission_data)` → binds data to schema
- `form.validation_errors()` → server-side validation, no frontend needed
- Conditional logic via [json-logic-qubit](https://pypi.org/project/json-logic-qubit/)
- Typed components (TextField, DateTime, Select, etc.)
- Nested structures supported

**Stress point coverage:**
- Calculated fields: **Full** — JavaScript expressions or JSON Logic, but expressions run in JS, not Python natively
- Dual severity: **None** — binary valid/invalid
- Versioning: **None** — rendering library, not lifecycle management
- Prior-year/external: **None** — no structured pattern

**Showstoppers for CSFEER:**
- Calculated field expressions are JavaScript. formio-data doesn't evaluate JavaScript expressions server-side — it processes schema structure and basic validation.
- formio.js depends on the DOM (browser environment). Server-side Node.js usage requires jsdom workarounds. No official headless validation package.
- OSL-v3 license on the server component (copyleft, requires attribution) adds compliance considerations.
- No warning vs error distinction at the framework level.

**Verdict:** formio-data demonstrates the right *pattern* — JSON schema parsed server-side with validation independent of rendering. But the JavaScript expression dependency and missing severity levels are significant gaps. **The pattern is good; the execution is incomplete for our needs.**

---

### 5. SurveyJS

**What it is:** Commercial form/survey library. `survey-core` is framework-agnostic JavaScript. PEG.js-based expression engine with dependency tracking and cached evaluation.

**Layer 1 — Field Definitions:**
JSON-defined questions with types, validators, conditional logic (`visibleIf`, `requiredIf`), calculated values (`calculatedValues` array), and expression syntax. Clean separation — validation runs independently of rendering.

**Layer 2 — Validation:**
**Only tool surveyed with three severity levels:**
1. **Error** (highest priority) — blocks form submission
2. **Warning** — appears after errors resolved
3. **Note/Informational** — appears only when no errors/warnings

`ExpressionValidator` supports formula-based validation. Custom async validators with caching. `requiredIf` for conditional requirements. Server-side validation via `onServerValidateQuestions` event.

**Stress point coverage:**
- Calculated fields: **Full** — expression syntax with dependency tracking, cached evaluation
- Dual severity: **Full** — the only tool with error/warning/info distinction
- Versioning: **None** — no version management
- Prior-year/external: **Partial** — server-side validation events can integrate external checks

**Showstoppers for CSFEER:**
- **No Python SDK or evaluation engine.** The expression engine, dependency tracker, and validation logic are all JavaScript. A [Python Flask demo](https://github.com/surveyjs/surveyjs-python-flask) exists but doesn't evaluate validation rules server-side.
- Commercial licensing: Essential (free) has limited features. PRO ($1,079/developer) or Enterprise ($2,399+) for full validation features. Per-developer perpetual license with annual renewal for updates.
- Maintaining parallel validation logic in Python and JavaScript doubles the maintenance burden.
- Survey-oriented design assumptions (pages as "panels", completion triggers, scoring) vs government form entry patterns.

**Verdict:** SurveyJS is the only tool that natively has the severity model we need. Its expression engine architecture (PEG.js parser → AST → dependency graph → cached evaluation) is the right design for client-side performance. But there's no way to run it server-side in Python. **Borrow the severity model and expression engine architecture. The implementation must be Python-native.**

---

### 6. JSON Forms (EclipseSource)

**What it is:** MIT-licensed dual-schema (JSON Schema + UI Schema) form renderer. v3.7.0, actively maintained. React/Angular/Vue.

**Layer 1 — Field Definitions:**
JSON Schema defines field types and constraints. UI Schema defines layout and rendering hints. Rule system provides conditional effects (`SHOW`/`HIDE`/`ENABLE`/`DISABLE`) with JSON Schema conditions. Clean separation of validation schema from presentation schema.

**Layer 2 — Validation:**
Uses AJV (framework-agnostic JSON Schema validator) under the hood. Validation modes: `ValidateAndShow` (review page), `ValidateAndHide` (silent for save-gating), `NoValidation` (auto-save). External errors injection via `additionalErrors` prop. **No severity levels** — all AJV failures are errors.

**Stress point coverage:**
- Calculated fields: **None** — requires imperative middleware or custom renderers. No declarative expression support.
- Dual severity: **None** — binary valid/invalid (AJV)
- Versioning: **None** — rendering library only
- Prior-year/external: **Partial** — `additionalErrors` prop injects backend validation alongside schema-derived errors

**Showstoppers for CSFEER:**
- No server-side story. React/Angular/Vue only — even "Vanilla" renderers are React components.
- No calculated fields at the schema level. Financial forms need `${a} + ${b} + ${c} = ${total}` as a first-class concept.
- Stepper/wizard is "not fully fleshed out" per their own docs.

**What's worth borrowing:**
- **Validation modes** (ValidateAndShow / ValidateAndHide / NoValidation) — cleaner than our session-flag approach
- **External errors injection** — same display pipeline for schema-derived and backend-injected errors
- **Dual-schema separation** — validates our Layer 1 / Layer 3 split

**Verdict:** Not a candidate as a tool. **Borrow validation modes and external error injection patterns.**

---

### 7. Pydantic + Custom Engine (Build Our Own)

**What it is:** Use Pydantic models as the field definition layer. Build a custom validation engine on top. This is what the current codebase already partially does.

**Layer 1 — Field Definitions:**
Pydantic models with typed fields, `Field()` constraints (min, max, pattern, etc.), and `model_json_schema()` for JSON serialization. `@computed_field` for derived values (serialization-only — not validated). Django-Pydantic integration via `django-pydantic-field` (latest release: Feb 2026).

**Layer 2 — Validation:**
`@field_validator` for single-field rules. `@model_validator` for cross-field validation. Fields validated in definition order — later validators can access earlier validated fields. Four validator modes: `before`, `after`, `plain`, `wrap`.

**What's missing and must be built:**
- **No severity levels.** All Pydantic validation failures are exceptions. Hard errors vs warnings must be implemented as a custom layer around Pydantic, not within it.
- **No expression engine.** Calculated fields like `${a} + ${b}` require a custom DSL parser, dependency tracker, and evaluator. Pydantic's `@computed_field` is read-only at serialization time, not evaluated during validation.
- **No reactive dependency graph.** When field A changes and field B's calculation depends on A, Pydantic doesn't know to recompute B. [Reaktiv](https://github.com/buiapp/reaktiv) (Python signals library) provides this pattern but is a state management tool, not a form validation library.
- **No conditional visibility.** `relevant` / `visibleIf` logic must be built from scratch.
- **No versioning.** Schema evolution, response pinning, and derivedFrom must be modeled explicitly.

**Stress point coverage:**
- Calculated fields: **Partial** — `@computed_field` exists but can't trigger validation; expression engine must be built
- Dual severity: **None** — must be built as custom wrapper
- Versioning: **None** — must be modeled explicitly
- Prior-year/external: **None** — must be built

**Advantages:**
- Full control. Every design decision is ours.
- Python-native. No JavaScript evaluation, no JVM runtime, no external services.
- JSON-serializable by default via `model_json_schema()`.
- Already in our stack — `BaseFormSchema` is Pydantic, `BaseFields` could migrate incrementally.
- Type-safe with pyright/mypy. Strict validation mode available.

**Verdict:** Building on Pydantic means building more ourselves, but we control every decision and avoid every tool's showstoppers. The question is whether the build cost is justified by the fit.

---

## Comparison Matrix

### Layer 1: Field Definitions

| Capability | Orbeon/XForms | ODK/pyxform | FHIR SDC | Form.io | SurveyJS | JSON Forms | Pydantic |
|---|---|---|---|---|---|---|---|
| **Typed fields** (text, number, date, choice) | Full | Full | Full | Full | Full | Full | Full |
| **Calculated fields** (formula expressions) | Full (XPath) | Full (`${x}` syntax) | Full (FHIRPath) | Full (JS) | Full (PEG.js) | None | Partial (`@computed_field`) |
| **Conditional visibility** (relevant/enableWhen) | Full (bind) | Full (relevant) | Full (2-tier) | Full (JSON Logic) | Full (visibleIf) | Full (rules) | None (build it) |
| **Repeatable sections** (one-to-many) | Full (repeat) | Full (repeat) | Partial (boolean flag) | Full (datagrid) | Partial | Partial | None (build it) |
| **Field metadata** (title, description, help) | Full | Full | Full | Full | Full | Full | Full (Field()) |
| **Pre-populated + locked fields** | Full (readonly bind) | Full (readonly) | Full (disabledDisplay) | Partial | Partial | Partial (rules) | None (build it) |
| **JSON-serializable definitions** | No (XML) | No (XML output) | Yes (JSON) | Yes (JSON) | Yes (JSON) | Yes (JSON) | Yes (model_json_schema) |
| **Python-native** | No (Java) | Partial (compiler only) | No (spec only) | No (JS) | No (JS) | No (JS) | **Yes** |

### Layer 2: Validation Rules

| Capability | Orbeon/XForms | ODK/pyxform | FHIR SDC | Form.io | SurveyJS | JSON Forms | Pydantic |
|---|---|---|---|---|---|---|---|
| **Field-level validation** | Full | Full | Full | Full | Full | Full (AJV) | Full |
| **Cross-field validation** (group sum checks) | Full (constraint) | Full (constraint) | Partial | Full (JS) | Full (expressions) | None | Full (model_validator) |
| **Hard errors vs warnings** | None | None | None | None | **Full (3 levels)** | None | None |
| **Inline error messages** | Full (alert) | Full (constraint_message) | Full | Full | Full | Full | Partial |
| **Formula-based rules** | Full (XPath) | Full (`${x}`) | Full (FHIRPath) | Full (JS/JSON Logic) | Full (PEG.js) | None | None (build it) |
| **Partial save without validation** | None (app concern) | None | None | None | None | Full (NoValidation mode) | None (build it) |
| **External error injection** | None | None | None | None | Partial (server events) | Full (additionalErrors) | None (build it) |
| **Server-side Python evaluation** | No | No | No | No | No | No | **Yes** |

### Versioning & Identity

| Capability | Orbeon/XForms | ODK/pyxform | FHIR SDC | Form.io | SurveyJS | JSON Forms | Pydantic |
|---|---|---|---|---|---|---|---|
| **Semantic versioning** | None | Weak (free text) | **Full** (semver + algorithm) | None | None | None | None (build it) |
| **Response version pinning** | None | None | **Full** (canonical URL\|version) | None | None | None | None (build it) |
| **Form variant inheritance** | None | None | **Full** (derivedFrom) | None | None | None | None (build it) |
| **Definition lifecycle** (draft/active/retired) | None | None | **Full** (status field) | None | None | None | None (build it) |

---

## The Gap That Defines Our Decision

No tool covers all four stress points:

| Stress Point | Best Coverage | Runner Up | Gap |
|---|---|---|---|
| **Calculated fields** | XForms bind / ODK syntax | SurveyJS expressions | No tool has Python-native evaluation |
| **Dual severity** | **SurveyJS** (only option) | Nobody else | SurveyJS is JS-only; must reimplement in Python |
| **Versioning** | **FHIR R5** (only mature option) | Nobody else | FHIR is a spec, not a runnable engine |
| **Prior-year/external** | FHIR SDC (initialExpression) | JSON Forms (additionalErrors) | Application-level concern everywhere |

**The critical finding:** Every tool that has the features we need (XForms' bind model, SurveyJS's severity levels, FHIR's versioning) runs in a language we can't use server-side. Every tool that runs in Python (Pydantic, formio-data) is missing the features we need.

This isn't a "pick one" decision. It's a "build one, informed by the best" decision.

---

## Recommendation: Pydantic Core + Borrowed Concepts

Build on Pydantic. Adopt concepts from the tools that got specific things right. Accept that we're building the expression engine and severity system ourselves — no existing tool provides both in Python.

### What to build (custom):

| Component | Inspired By | What We Build |
|---|---|---|
| **FieldBind** (unified per-field declaration) | XForms bind (calculate/constraint/relevant/required/readonly) | Pydantic model with expression strings for each property |
| **Expression engine** (`${field}` syntax) | ODK reference syntax + SurveyJS dependency tracking architecture | Python parser + evaluator with dependency graph and cached recomputation |
| **Validation severity** (error/warning/info) | SHACL (Violation/Warning/Info) + SurveyJS (3 levels) | Custom `ValidationResult` with typed severity enum, separate error/warning collections |
| **Validation modes** | JSON Forms (ValidateAndShow/ValidateAndHide/NoValidation) | Enum that controls whether validation runs and whether results surface to UI |
| **External error injection** | JSON Forms (additionalErrors) | Same `ValidationMessage` type for schema-derived and backend-injected errors |
| **Non-relevant data exclusion** | XForms (relevant → excluded from submission) | Serializer that omits fields where `relevant` evaluates to `false` |

### What to adopt (from standards):

| Component | Source | What We Adopt |
|---|---|---|
| **Versioning model** | FHIR R5 | Canonical URL + semver + `versionAlgorithmCoding` + `derivedFrom` + response version pinning |
| **Two-tier conditionals** | FHIR SDC | Tier 1: declarative field comparisons (80% of cases). Tier 2: expression-based (20%) |
| **disabledDisplay** | FHIR R5 | `hidden` (field removed) vs `protected` (field visible but locked) for pre-populated fields |
| **Definition/response separation** | FHIR Questionnaire/QuestionnaireResponse | FormDefinition (schema) and FormEntry (submission) as separate resources, entry pinned to definition version |

### What NOT to build:

- **Full XForms runtime** — we want the bind *model*, not an XML processor
- **FHIRPath evaluator** — too verbose for financial arithmetic; use `${field}` syntax
- **JSON Logic evaluator** — too limited for cross-field formulas; our expression engine subsumes it
- **JavaScript bridge** — running Node.js alongside Django for SurveyJS/formio.js evaluation adds operational complexity that outweighs the feature benefit

### The resulting architecture:

```
FieldBind (per field)                    ValidationEngine
├── field_name: str                      ├── validate(values, binds) → ValidationResult
├── calculate: "${a} + ${b}"             │
├── constraint: "${total} == ${award}"   ├── ExpressionEngine
├── constraint_message: str              │   ├── parse("${a} + ${b}") → AST
├── constraint_severity: error|warning   │   ├── evaluate(ast, values) → value
├── relevant: "${has_items} == True"     │   └── dependency_graph: dict[field, set[field]]
├── required: bool | str (expression)    │
├── readonly: bool | str (expression)    ├── ValidationResult
└── disabled_display: hidden|protected   │   ├── is_valid: bool (true if zero errors)
                                         │   ├── errors: dict[field, list[ValidationMessage]]
FormIdentity                             │   ├── warnings: dict[field, list[ValidationMessage]]
├── url: str (canonical)                 │   └── infos: dict[field, list[ValidationMessage]]
├── version: str (semver)                │
├── derived_from: str | None             └── ValidationMessage
├── status: draft|active|retired             ├── severity: error|warning|info
└── version_algorithm: "semver"              ├── code: str (REQUIRED, SUM_MISMATCH, etc.)
                                             ├── message: str (human-readable)
ValidationMode (from JSON Forms)             └── context: dict (expected, actual, related fields)
├── VALIDATE_AND_SHOW
├── VALIDATE_AND_HIDE
└── NO_VALIDATION
```

### Why this beats adopting any single tool:

1. **Python-native server-side validation.** No JVM, no Node.js, no DOM simulation. `ValidationEngine.validate(entry.data)` returns a plain data object.
2. **Severity levels from day one.** No other Python-compatible option has this. It's the PRD's #2 stress point.
3. **Expression syntax works in both Python and JavaScript.** `${personnel} + ${equipment}` parses identically on both sides. Same semantics, two implementations. (The client-side engine is a future Phase II concern.)
4. **Versioning is modeled, not afterthought.** FHIR R5's model is adopted structurally — canonical URLs, semver, derivedFrom, response pinning — without the FHIR data model overhead.
5. **Incremental migration.** Pydantic is already in the stack (`BaseFormSchema`, `BaseFields`). Layer 1 and 2 can be built alongside the existing Django Form mechanism and migrated incrementally per the [roadmap's strangle-not-rewrite principle](form-engine-roadmap.md#guiding-principle-strangle-dont-rewrite).

---

## Build Cost Assessment

What "build our own" actually means — scoped to Layer 1 + Layer 2 only:

| Component | Complexity | Notes |
|---|---|---|
| `FieldBind` Pydantic model | Low | ~50 lines. Typed model with optional expression strings. |
| `FormIdentity` versioning model | Low | ~30 lines. Adopts FHIR R5 pattern structurally. |
| `ValidationResult` + `ValidationMessage` | Low | ~60 lines. Typed data classes with severity enum. |
| `ValidationMode` enum | Trivial | 3-value enum. |
| Expression parser (`${field}` → AST) | Medium | PEG parser or regex-based tokenizer. ~200 lines for arithmetic + comparison + boolean. |
| Expression evaluator (AST + values → result) | Medium | Tree-walk evaluator. ~150 lines. Safe eval with no arbitrary code execution. |
| Dependency graph builder | Medium | Static analysis of expression ASTs to build `field → set[dependent_fields]` map. ~100 lines. |
| `ValidationEngine.validate()` | Medium | Topological sort of dependency graph, evaluate binds in order, collect results. ~200 lines. |
| Non-relevant data exclusion | Low | Filter serialized data through `relevant` expression evaluation. ~30 lines. |
| Auto-derived rules from FieldBind constraints | Low | Required, min/max, choices → FieldRule objects. ~100 lines. |

**Estimated total: ~900 lines of Python** for a complete Layer 1 + Layer 2 engine. This is comparable to the current `fields.py` (340 lines) + `forms/base.py` (146 lines) + form-specific field declarations, but produces a dramatically more capable system.

For comparison, formio-data (the closest Python equivalent) is ~2,000 lines and doesn't support calculated field evaluation, severity levels, or versioning.

---

*Research sources: [Orbeon Forms 2025.1](https://doc.orbeon.com/release-notes/orbeon-forms-2025.1), [Orbeon Pricing](https://www.orbeon.com/pricing), [Orbeon JSON Support](https://doc.orbeon.com/xforms/submission/submission-json), [pyxform](https://github.com/XLSForm/pyxform), [ODK XForms Spec](https://getodk.github.io/xforms-spec/), [FHIR R5 Questionnaire](https://hl7.org/fhir/questionnaire.html), [FHIR SDC IG](https://build.fhir.org/ig/HL7/sdc/), [fhir.resources](https://pypi.org/project/fhir.resources/), [formio.js v5.9](https://github.com/formio/formio.js/releases), [formio-data](https://github.com/novacode-nl/python-formio-data), [Form.io License (OSL-v3)](https://github.com/formio/formio/issues/950), [SurveyJS Pricing](https://surveyjs.io/pricing), [SurveyJS Validation](https://surveyjs.io/form-library/documentation/data-validation), [SurveyJS Python Flask Demo](https://github.com/surveyjs/surveyjs-python-flask), [JSON Forms v3.7](https://jsonforms.io/), [JSON Forms Validation](https://jsonforms.io/docs/validation), [Pydantic Validators](https://docs.pydantic.dev/latest/concepts/validators/), [Pydantic Computed Fields](https://docs.pydantic.dev/latest/concepts/fields/), [django-pydantic-field](https://pypi.org/project/django-pydantic-field/), [Reaktiv](https://github.com/buiapp/reaktiv), [json-logic-qubit](https://pypi.org/project/json-logic-qubit/), [W3C XForms 1.1](https://www.w3.org/TR/xforms11/), [W3C SHACL](https://www.w3.org/TR/shacl/), [RJSF v6](https://github.com/rjsf-team/react-jsonschema-form), [jsonschema (Python)](https://pypi.org/project/jsonschema/), [cexprtk](https://pypi.org/project/cexprtk/)*
