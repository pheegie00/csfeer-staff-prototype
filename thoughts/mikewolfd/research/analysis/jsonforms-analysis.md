# JSON Forms (jsonforms.io) — Analysis for CSFEER

> What can we learn from [JSON Forms](https://jsonforms.io/) for CSFEER's form engine architecture?
> Companion to: [form-engine-roadmap.md](form-engine-roadmap.md), [form-schema-landscape.md](form-schema-landscape.md), [simpler-grants-analysis.md](simpler-grants-analysis.md)

---

## What They Built

**[JSON Forms](https://github.com/eclipsesource/jsonforms)** is a declarative, schema-driven form rendering framework maintained by [EclipseSource](https://eclipsesource.com/) (commercial company, MIT license). It separates data validation from UI presentation using two JSON documents, then dispatches rendering through a pluggable renderer registry.

### The Two-Schema Approach

```
JSON Schema (what's valid)          UI Schema (how it looks)
├── types, required, enums          ├── layouts (Vertical, Horizontal, Group)
├── min/max, pattern, format        ├── controls (scope → data binding)
├── if/then/else conditionals       ├── rules (SHOW/HIDE/ENABLE/DISABLE)
└── $ref for composition            └── categorization (tabs/stepper)
         ↓                                    ↓
    ┌────┴────────────────────────────────────┴────┐
    │         Renderer Registry (testers)           │
    │    tester(uischema, jsonschema) → priority     │
    │    highest-ranked renderer wins                │
    └──────────────────────────────────────────────┘
         ↓                    ↓                ↓
    React Material     React Vanilla     Angular Material
    Vue Vanilla        Vue Vuetify       Custom renderers
```

**Key architectural insight:** The renderer dispatch is priority-based. Each renderer registers a tester function that returns a numeric rank. When JSON Forms encounters a UI schema element, it evaluates all testers and picks the highest-scoring renderer. Default renderers use rank 2; custom renderers use rank 3+ to override. This lets you surgically replace individual controls without touching the rest of the form.

### Project Health (as of Feb 2026)

- **Latest release:** v3.7.0 (22 days ago)
- **License:** MIT
- **Maintainer:** EclipseSource (commercial company)
- **Funded by:** Gordon and Betty Moore Foundation, Crossref
- **Risk:** 51%+ of contributions from one org (EclipseSource). Small bus factor, but backed by commercial entity with long-term commitment.
- **Community:** Active Discourse forum, smaller than RJSF but professionally supported.

---

## The Form Model (What Matters for Us)

### JSON Schema — Data Validation

Standard JSON Schema Draft 2020-12 for field-level validation:

```json
{
  "type": "object",
  "properties": {
    "org_name": { "type": "string", "minLength": 1 },
    "award_amount": { "type": "number", "minimum": 0 },
    "report_status": {
      "type": "string",
      "enum": ["draft", "submitted", "approved"]
    },
    "submission_date": { "type": "string", "format": "date" }
  },
  "required": ["org_name", "award_amount"]
}
```

Conditional validation via JSON Schema `if/then/else`:

```json
{
  "if": {
    "properties": { "has_variance": { "const": true } }
  },
  "then": {
    "required": ["variance_explanation"]
  }
}
```

Validation powered by **AJV** (Another JSON Schema Validator) with three modes:
- `ValidateAndShow` (default) — validate and display errors
- `ValidateAndHide` — validate silently, errors available programmatically
- `NoValidation` — skip validation entirely

### UI Schema — Layout & Interaction

A separate JSON document describing how to render the form:

```json
{
  "type": "VerticalLayout",
  "elements": [
    {
      "type": "Group",
      "label": "Organization Information",
      "elements": [
        {
          "type": "Control",
          "scope": "#/properties/org_name",
          "label": "Organization Name"
        },
        {
          "type": "Control",
          "scope": "#/properties/award_amount",
          "options": { "format": "currency" }
        }
      ]
    },
    {
      "type": "Control",
      "scope": "#/properties/has_variance",
      "rule": {
        "effect": "SHOW",
        "condition": {
          "scope": "#/properties/report_status",
          "schema": { "const": "submitted" }
        }
      }
    }
  ]
}
```

**Layout types:**

| Type | Purpose | CSFEER Equivalent |
|------|---------|-------------------|
| `VerticalLayout` | Stack elements vertically | Default page flow |
| `HorizontalLayout` | Side-by-side, equal width (1/n) | No direct equivalent |
| `Group` | VerticalLayout with label/border | `SectionBlock` |
| `Categorization` | Tabs or stepper navigation | `StepBlock` |
| `Category` | Individual tab/step | `PageBlock` (roughly) |
| `Control` | Binds to a data field via `scope` | `FieldBlock` |

### Rule System — Conditional Logic

Rules attach to any UI schema element and control visibility or interactivity:

```json
{
  "type": "Control",
  "scope": "#/properties/variance_explanation",
  "rule": {
    "effect": "SHOW",
    "condition": {
      "scope": "#/properties/has_variance",
      "schema": { "const": true }
    }
  }
}
```

**Effects:** `SHOW`, `HIDE`, `ENABLE`, `DISABLE`

**Conditions use JSON Schema validation:** The `condition.schema` is validated against the data at `condition.scope`. If validation passes, the effect applies. This means anything expressible in JSON Schema can be a condition — `enum`, `minimum`, `not`, `anyOf`, `allOf`, `oneOf`, `contains`, `required`, `properties`.

**Priority cascade for enabled/disabled state:**
1. Form-wide `readonly` → all disabled
2. `ENABLE`/`DISABLE` rule on element
3. UI Schema `options.readonly`
4. JSON Schema `readOnly: true`
5. Parent element's state (inherited)

### Renderer Registry — Pluggable Output

```javascript
// Register a custom renderer with higher priority than defaults
const renderers = [
  ...materialRenderers,  // rank 2 (defaults)
  {
    tester: rankWith(3, scopeEndsWith('award_amount')),
    renderer: CurrencyControl  // custom component, rank 3 (overrides)
  }
];

<JsonForms
  schema={jsonSchema}
  uischema={uiSchema}
  data={formData}
  renderers={renderers}
  onChange={({ data, errors }) => handleChange(data, errors)}
/>
```

**Framework bindings:** React (Material + Vanilla), Angular (Material), Vue (Vanilla + Vuetify preview). No vanilla JS — must use a framework binding.

### Middleware — State Interception

Added in v3.2, middleware intercepts all state changes:

```javascript
const computedFieldMiddleware = (state, action, defaultReducer) => {
  const newState = defaultReducer(state, action);
  if (action.type === 'UPDATE_DATA') {
    // Calculate derived fields after any data change
    const total = (newState.data.personnel || 0)
                + (newState.data.equipment || 0)
                + (newState.data.travel || 0);
    return { ...newState, data: { ...newState.data, total_costs: total } };
  }
  return newState;
};
```

This is their answer to computed/calculated fields — no declarative syntax, but a clean interception point.

---

## What's Directly Adaptable

### 1. Rule System Architecture (HIGH VALUE — CONCEPT ONLY)

JSON Forms' rule system solves conditional logic elegantly: effects are a closed set (`SHOW`/`HIDE`/`ENABLE`/`DISABLE`), conditions use JSON Schema validation, and rules attach to any UI element.

**Why this matters for CSFEER:**

CSFEER's current conditional logic is `FieldFilterField` — a checkbox that controls which fields are included/excluded. This works for the current use case (select applicable topics → show/hide related fields) but doesn't generalize to:
- Show a text area only when a radio button is "Yes"
- Disable a field when another field exceeds a threshold
- Hide an entire section based on a combination of conditions

The rule concept maps cleanly to our Layer 3 (Layout):

```python
# Conceptual — not their code, adapted for CSFEER's Pydantic model
class Rule(BaseModel):
    effect: Literal["show", "hide", "enable", "disable"]
    condition: RuleCondition

class RuleCondition(BaseModel):
    field: str                    # field_name to evaluate (our scope equivalent)
    schema: dict                  # JSON Schema fragment for validation
    fail_when_undefined: bool = False

class FieldRef(BaseModel):
    field_name: str
    rule: Rule | None = None      # Optional conditional behavior
```

**What to borrow:** The mental model — effects as a small enum, conditions as schema validation against field data. **What NOT to borrow:** The JSON pointer scope syntax (`#/properties/...`) — our flat field namespace with string names is simpler and sufficient.

**Adaptation plan:**
- Add optional `rule` to `FieldRef` and layout nodes in Layer 3
- Implement conditions as Python functions initially (not JSON Schema validation — we don't use AJV server-side)
- This replaces `FieldFilterField` as a special field type with rules as a layout concern
- Decision D2 from the roadmap: "Both" — Layer 1 declares relationships, Layer 3 implements visibility via rules

### 2. Tester/Renderer Registry Pattern (HIGH VALUE)

The priority-ranked renderer dispatch is the most architecturally elegant piece. Instead of hardcoding which component renders each field type, you register (tester, renderer) pairs and the highest-scoring match wins.

**Why this matters for CSFEER:**

CSFEER currently has `FieldBlock.as_review_block()` which auto-discovers review templates by introspecting the field's widget class name (e.g., `CurrencyInput` → `currency_review.html`). This works but is implicit and one-dimensional — you can only vary by widget type, not by field name, context, or data state.

The tester pattern generalizes this:

```python
# Conceptual — adapted for Django templates
class RendererRegistry:
    """Priority-ranked renderer dispatch for form fields."""

    def __init__(self):
        self._renderers: list[tuple[Callable, str, int]] = []  # (tester, template, priority)

    def register(self, tester: Callable, template: str, priority: int = 2):
        self._renderers.append((tester, template, priority))
        self._renderers.sort(key=lambda r: r[2], reverse=True)

    def resolve(self, field_def: FieldDefinition, context: str) -> str:
        """Return the best-matching template path."""
        for tester, template, _ in self._renderers:
            if tester(field_def, context):
                return template
        return "form_manager/forms/field.html"  # fallback

# Usage:
registry = RendererRegistry()
registry.register(
    tester=lambda f, ctx: f.field_type == "currency" and ctx == "review",
    template="form_manager/forms/currency_review.html",
    priority=3
)
registry.register(
    tester=lambda f, ctx: f.field_type == "currency" and ctx == "edit",
    template="form_manager/forms/currency_edit.html",
    priority=3
)
```

**Adaptation plan:**
- Implement as part of Layer 4 (Renderers) in the roadmap
- Replaces the current widget-class-name-to-template introspection in `FieldBlock.as_review_block()`
- Supports multiple rendering contexts (edit, review, PDF, API) without modifying field definitions
- Start simple — register by field_type + context, extend to more complex predicates later

### 3. Two-Schema Separation Pattern (VALIDATES EXISTING DIRECTION)

JSON Forms' core insight — **validation rules should be independent of rendering** — directly validates CSFEER's roadmap Layer 1-4 architecture. Their JSON Schema handles what's valid; their UI Schema handles how it looks. Neither knows about the other.

This is the same principle as the roadmap's "dependency inversion" — Layers 1-2 (definitions + validation) never import from Layer 4 (renderers).

**What this confirms:**
- The current `BaseFormSchema.form_fields` (Django Form that fuses validation + rendering) is the right thing to decompose
- Layer 1 (field definitions) and Layer 2 (validation rules) should be pure data, never referencing templates or widgets
- Layout (their UI Schema, our Layer 3) references fields by identifier, not by type

### 4. Validation Mode Concept (MEDIUM VALUE)

JSON Forms' three validation modes map to a real CSFEER need:

| JSON Forms Mode | CSFEER Equivalent |
|----------------|-------------------|
| `ValidateAndShow` | Review page (show all errors) |
| `ValidateAndHide` | Edit page before review (validate silently for save-gating) |
| `NoValidation` | Auto-save / partial save (never block) |

Currently CSFEER manages this with session flags (`show_errors_{pk}`). A validation mode enum is cleaner:

```python
class ValidationMode(str, Enum):
    VALIDATE_AND_SHOW = "validate_and_show"
    VALIDATE_AND_HIDE = "validate_and_hide"
    NO_VALIDATION = "no_validation"
```

**Adaptation plan:**
- Add to `ValidationEngine.validate()` as a parameter
- Replace session-flag-based error display control
- `NO_VALIDATION` mode enables the PRD requirement: "Saving incomplete sections must NOT trigger blocking validation"

### 5. Additional Errors / External Validation (MEDIUM VALUE)

JSON Forms' `additionalErrors` prop injects backend validation errors alongside schema-derived errors. This is relevant for CSFEER's:
- UEI validation against SAM.gov
- Prior-year comparison warnings
- Cross-form consistency checks

The pattern: validation results from external sources are injected into the same error display pipeline as schema-derived errors. They're structurally identical but come from different sources.

```python
class ValidationResult:
    schema_errors: dict[str, list[ValidationMessage]]    # From field constraints
    external_errors: dict[str, list[ValidationMessage]]  # From external checks
    warnings: dict[str, list[ValidationMessage]]         # Soft (non-blocking)

    @property
    def all_errors(self) -> dict[str, list[ValidationMessage]]:
        return merge_dicts(self.schema_errors, self.external_errors)

    @property
    def is_valid(self) -> bool:
        return not self.all_errors  # Only hard errors block
```

---

## What's NOT Adaptable (and Why)

### Their Computed Fields Approach Is Imperative, Not Declarative

JSON Forms has **no declarative syntax** for computed/calculated fields. Their three approaches:

1. **onChange handler** — listen to data changes, calculate, update (risk of infinite loops)
2. **Middleware** — intercept `UPDATE_DATA` action, modify state (recommended but still imperative)
3. **Custom renderer** — component-level calculation logic

All require writing JavaScript code. None are serializable to JSON.

CSFEER needs: `"expression": "${personnel} + ${equipment} + ${travel}"` as a string in the field definition, evaluated server-side (Python) and client-side (JS) from the same source. JSON Forms doesn't model this.

### Their Rule Conditions Are JSON Schema, Not Expressions

JSON Forms conditions use JSON Schema validation:

```json
{
  "condition": {
    "scope": "#/properties/amount",
    "schema": { "minimum": 1000 }
  }
}
```

This is powerful for type-based checks but can't express:
- `${total} == ${sum_items}` (cross-field arithmetic comparison)
- `${current_year_amount} > ${prior_year_amount} * 1.1` (prior-year threshold)
- `${field_a} + ${field_b} + ${field_c} == ${field_d}` (sum check)

CSFEER needs an **expression language** for conditions and calculations, not JSON Schema predicates. ODK's `${field}` syntax or a simple DSL is more appropriate.

### No Hard Error vs Soft Warning Distinction

All AJV validation failures are errors. No severity levels, no warning concept. The `additionalErrors` prop could theoretically carry warnings, but there's no built-in rendering distinction.

CSFEER's PRD explicitly requires: "Hard errors (block submission)" vs "Warnings/notifications (inform only, do not block)." This must be built custom regardless.

### No Multi-Step Navigation Beyond Basic Tabs/Stepper

`Categorization` with `variant: "stepper"` provides basic tab/step switching. But:
- No validation gates between steps (can't prevent advancing to step 3 if step 2 has errors)
- No progress indicators beyond the stepper itself
- No concept of "permanent pages" that can't be excluded
- JSON Forms docs acknowledge stepper is "not fully fleshed out"

CSFEER needs: Steps > Pages > Sections > FieldGroups > Fields, with conditional page exclusion, permanent pages, and review-page-driven error display. This is fundamentally deeper than what Categorization provides.

### Frontend Stack Mismatch

JSON Forms requires React, Angular, or Vue. No vanilla JS binding exists. CSFEER uses Django templates + django-cotton + USWDS. The rendering layer doesn't transfer.

Even the "Vanilla" renderer sets (`@jsonforms/vanilla-renderers`) are React components that render plain HTML — they're still React.

### No Form-Level or Cross-Form Validation

JSON Schema validation is per-field. AJV validates the entire data object against the schema, but there's no concept of:
- Group-level validation ("these 5 fields must sum to this total")
- Cross-form validation ("this value must match what was entered in a different form")
- Prior-year comparison ("this value changed by more than 10% — explain why")

These require custom middleware or external validation, both of which are imperative, not declarative.

### No Version Pinning on Data

JSON Forms doesn't model form definitions or responses as persistent entities. There's no:
- Form version management
- Response-to-definition version pinning
- Definition lifecycle (draft → active → retired)
- Canonical URLs or semantic versioning

JSON Forms is a **rendering library**, not a form lifecycle management system.

---

## Comparison to Roadmap Layers

| Roadmap Layer | JSON Forms Has | JSON Forms Doesn't Have |
|---|---|---|
| **Layer 1: Field Definitions** | JSON Schema field types, `required`, `enum`, `format`, `readOnly` | Calculated fields (declarative), field metadata (review_title, description), field groups, `default_if_excluded`, currency type |
| **Layer 2: Validation Rules** | AJV validation, conditional `if/then/else`, format validators, `additionalErrors` for external validation | Hard vs soft errors, group-level sum checks, cross-field arithmetic, prior-year comparison, expression-based constraints |
| **Layer 3: Layout** | VerticalLayout, HorizontalLayout, Group, Categorization/Category, Control with scope binding | Steps > Pages > Sections > FieldGroups (depth), permanent pages, conditional page exclusion, `flatten_for_review()`, review subheadings |
| **Layer 3: Conditional Logic** | Rule system (SHOW/HIDE/ENABLE/DISABLE) with JSON Schema conditions | Expression-based conditions (`${a} + ${b} == ${c}`), FieldFilterField checkbox-to-exclusion pattern |
| **Layer 4: Renderers** | Priority-ranked renderer registry, custom renderers, multi-framework support | Django template rendering, PDF export, API serialization, review page, CSV export |
| **Cross-cutting: Versioning** | None | Version management, canonical URLs, semver, derivedFrom, response version pinning |
| **Cross-cutting: Mapping** | None | Cross-form pre-population, prior-year data import, MappingSchema DSL |
| **Cross-cutting: Workflow** | None | Draft/submitted/amended/archived lifecycle, multi-step review, submission gating |

---

## Comparison to RJSF

Since the landscape research mentioned both, and CommonGrants chose JSON Forms over RJSF:

| Aspect | JSON Forms | RJSF | CSFEER Relevance |
|--------|-----------|------|-------------------|
| **Schema approach** | Two schemas (data + UI) | Single schema with `ui:` hints | Two-schema validates our Layer 1-3 separation |
| **Layout control** | Full layout via UI Schema | Limited, hints only | JSON Forms' approach is closer to our `StepBlock > PageBlock > ...` |
| **Conditional logic** | Rule system (SHOW/HIDE/ENABLE/DISABLE) | `if/then/else` in JSON Schema only | Rule system is more expressive for UI behavior |
| **Renderer customization** | Tester/priority registry | Widget/template replacement | Tester registry is more composable |
| **Framework support** | React, Angular, Vue | React only | Neither helps — we're Django templates |
| **Community** | Smaller, corporate-backed | Larger, community-driven | Neither is a risk factor for concept borrowing |

**Verdict:** JSON Forms has the better *architecture* for our purposes (separation of concerns, renderer dispatch, rule system). RJSF has simpler ergonomics but less decomposition. Neither's rendering layer is usable for CSFEER — we're borrowing concepts, not code.

---

## Recommendation

### Adopt These Concepts

1. **Rule system architecture** — Borrow the effects-as-enum + conditions-evaluated-against-data model. Adapt conditions to use CSFEER's expression syntax instead of JSON Schema validation. Apply to Layer 3 layout nodes for conditional visibility and interactivity. This generalizes `FieldFilterField` from a special field type to a layout concern.

2. **Renderer registry with priority-ranked testers** — Implement in Layer 4 for template resolution. Replaces the current widget-class-name introspection in `FieldBlock.as_review_block()`. Supports multiple rendering contexts (edit, review, PDF, API) without modifying field definitions or layout.

3. **Validation mode enum** — Adopt the three-mode pattern (`validate_and_show`, `validate_and_hide`, `no_validation`) to replace session-flag-based error display control. Cleaner API, explicit behavior.

4. **External errors injection** — Model external validation results (SAM.gov UEI check, prior-year comparison) as structurally identical to schema-derived errors, injected into the same `ValidationResult`. Avoids separate error display pipelines.

5. **Two-schema separation** — Confirms the roadmap's Layer 1-4 architecture. JSON Forms' success with this pattern in production validates that separating validation from rendering is the right direction.

### Don't Adopt

1. **JSON Schema as condition language** — Too limited for arithmetic expressions. CSFEER needs `${a} + ${b} == ${c}`, not `{ "minimum": 1000 }`. Use a simple expression DSL instead.

2. **Middleware for computed fields** — Imperative, framework-specific, not serializable. CSFEER needs declarative `"expression": "${personnel} + ${equipment}"` that works both server-side (Python) and client-side (JS).

3. **Categorization for multi-step** — Too shallow. CSFEER needs 4 levels of nesting (Steps > Pages > Sections > FieldGroups), permanent pages, conditional exclusion, and review-page integration.

4. **AJV for validation** — Wrong runtime. CSFEER validates server-side in Python. JSON Schema validation via a Python library (like `jsonschema`) could complement the `ValidationEngine`, but AJV specifically is a JavaScript tool.

5. **Any rendering code** — Wrong stack entirely. Django templates + django-cotton + USWDS, not React/Angular/Vue.

6. **JSON pointer scope syntax** — `#/properties/address/properties/city` is verbose for flat field namespaces. CSFEER's string field names (`"org_name"`, `"award_amount"`) are simpler and sufficient. Only adopt JSON pointers if CSFEER moves to deeply nested data models.

---

## Updated Roadmap Implications

### Layer 3 Gets Richer

The rule system concept adds a new dimension to Layout. Currently Layer 3 is pure structure (what goes where). With rules, it also expresses **conditional behavior** (when things appear/disappear, enable/disable):

```
Layer 3: LAYOUT (structure + conditional behavior)
├── Steps, pages, sections, groups, field placement  ← existing
├── Conditional visibility via rules                  ← NEW from JSON Forms
└── Conditional interactivity via rules               ← NEW from JSON Forms
```

This moves conditional logic from Layer 1 (where `FieldFilterField` lives as a field type) to Layer 3 (where it belongs as a layout concern). Decision D2 from the roadmap resolves toward "Layer 3 implements visibility via rules."

### Layer 4 Gets a Registry

The renderer dispatch pattern adds structure to what was previously ad-hoc template resolution:

```
Layer 4: RENDERERS (adapters with registry)
├── RendererRegistry: (tester, template, priority) tuples   ← NEW from JSON Forms
├── DjangoFormRenderer: edit context
├── ReviewRenderer: review context
├── PDFRenderer: export context
└── APIRenderer: API context
```

Each context registers its own testers, so the same `FieldDefinition` can render differently in edit vs review vs PDF without the field knowing about rendering at all.

### No New Layers

Unlike the simpler-grants analysis (which added a Mapping layer), JSON Forms doesn't introduce new layers — it deepens existing ones. The conceptual model remains:

```
Layer 1: Field Definitions ──────────────────────────────
Layer 2: Validation Rules  ──────────────────────────────
Layer 3: Layout + Rules    ── conditional visibility/interactivity (enriched)
Layer M: Mapping           ── cross-form pre-population (from CommonGrants)
Layer 4: Renderers         ── priority-ranked registry (enriched)
```

---

*Sources: [JSON Forms Docs](https://jsonforms.io/docs/), [GitHub](https://github.com/eclipsesource/jsonforms), [Architecture](https://jsonforms.io/docs/architecture/), [Rules](https://jsonforms.io/docs/uischema/rules/), [Validation](https://jsonforms.io/docs/validation), [Middleware](https://jsonforms.io/docs/middleware/), [Custom Renderers](https://jsonforms.io/docs/tutorial/custom-renderers), [Renderer Sets](https://jsonforms.io/docs/renderer-sets/), [FAQ](https://jsonforms.io/faq/), [CommonGrants ADR 0020](https://commongrants.org/governance/adr/0020-form-library-framework/), [RJSF Comparison](https://jsonforms.discourse.group/t/compare-to-react-jsonschema-form/553)*
