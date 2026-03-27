# Simpler.Grants.Gov / CommonGrants Protocol — Analysis for CSFEER

> What can we adapt from [HHS/simpler-grants-gov](https://github.com/HHS/simpler-grants-gov) and [HHS/simpler-grants-protocol](https://github.com/HHS/simpler-grants-protocol)?
> Companion to: [form-engine-roadmap.md](form-engine-roadmap.md), [form-schema-landscape.md](form-schema-landscape.md)

---

## What They Built

Two repos, one protocol:

**[HHS/simpler-grants-gov](https://github.com/HHS/simpler-grants-gov)** — Monorepo with Flask/APIFlask backend + Next.js/React frontend. Covers grant opportunity search, application workflow, and forms rendering.

**[HHS/simpler-grants-protocol](https://github.com/HHS/simpler-grants-protocol)** — The **CommonGrants protocol**, an open standard for grant data exchange. This is the interesting part for us. Defined in TypeSpec, with generated Python SDK (Pydantic models) and TypeScript SDK.

### Architecture Overview

```
TypeSpec definitions (lib/core/src/)
    ↓ compiles to
OpenAPI spec + JSON Schema
    ↓ generates
Python SDK (Pydantic)          TypeScript SDK
    ↓                              ↓
Flask API backend           Next.js frontend
    ↓                              ↓
Form data storage          JSON Forms rendering
```

They chose **JSON Forms** over RJSF and Uniforms ([ADR 0020](https://commongrants.org/governance/adr/0020-form-library-framework/)) for:
- Fully serialized schema/UI config (no code in UI layout)
- Multi-framework portability (React, Angular, Vue)
- Per-field custom renderer mapping
- Tester/renderer architecture for complex components

---

## The Form Model (What Matters for Us)

### FormBase — Definition

```typescript
// lib/core/lib/core/models/form.tsp
model FormBase {
  id: uuid;
  name: string;
  description?: string;
  version?: string;                          // Added in v0.3
  instructions?: string | File[];
  jsonSchema?: FormJsonSchema;               // Validation rules (JSON Schema)
  uiSchema?: FormUISchema;                   // Rendering instructions (JSON Forms UI Schema)
  mappingToCommonGrants?: MappingSchema;      // Form fields → canonical model
  mappingFromCommonGrants?: MappingSchema;    // Canonical model → form fields
  customFields?: Record<CustomField>;
  ...SystemMetadata;                         // createdAt, lastModifiedAt
}
```

**Key insight:** They separate:
1. **jsonSchema** — what's valid (types, required, enums)
2. **uiSchema** — how to render (layout, grouping, controls)
3. **mappingTo/FromCommonGrants** — how to translate between form fields and canonical data

This three-schema approach adds something the landscape research didn't surface: a **declarative mapping layer** between form-specific field names and a shared data model.

### FormResponseBase — Submission

```typescript
model FormResponseBase {
  id: uuid;
  formId: uuid;                    // References the form, NOT a specific version
  response: Record<unknown>;       // Flat key-value data
  status: FormResponseStatus;      // notStarted | inProgress | complete
  validationErrors?: Array<unknown>;
  customFields?: Record<CustomField>;
  ...SystemMetadata;
}
```

### ApplicationBase — Workflow Container

```typescript
model ApplicationBase {
  id: uuid;
  competitionId: uuid;
  opportunityId: uuid;
  formResponses: Record<AppFormResponse>;  // Multiple forms per application
  status: AppStatus;                       // inProgress | submitted | accepted | rejected | custom
  submittedAt?: utcDateTime | null;
  validationErrors?: Array<unknown>;
  customFields?: Record<CustomField>;
  ...SystemMetadata;
}
```

The **Application** wraps multiple **FormResponses** — one application can contain responses to several forms. Status lives on the Application, not on individual form responses.

### API Routes

```
PUT /{appId}/forms/{formId}   — Set/update form response
GET /{appId}/forms/{formId}   — Get form response
```

Simple CRUD. No multi-step review workflow, no federal approval chain.

---

## What's Directly Adaptable

### 1. MappingSchema — Declarative Data Transformation (HIGH VALUE)

This is the most interesting piece for CSFEER. The `MappingSchema` provides a declarative DSL for bidirectional data transformation between form fields and a canonical model:

```python
# Three mapping functions:
# "field" — extract value by dot-path
# "switch" — map value through lookup table
# "const" — literal value

mapping = {
    "status": {"field": "summary.opportunity_status"},       # Path extraction
    "amount": {"field": "summary.opportunity_amount"},        # Path extraction
    "category": {
        "switch": {
            "field": "summary.opportunity_status",            # Switch on value
            "case": {"active": "open", "inactive": "closed"},
            "default": "custom"
        }
    },
    "source_id": {"const": "123"}                            # Constant
}
```

**Why this matters for CSFEER:**

The PRD requires cross-form pre-population — Tribal Plan pre-populates from Tribal AR data via shared field identifiers. Currently there's no mechanism for this. The `MappingSchema` pattern solves it:

```python
# Mapping: Tribal AR → Tribal Plan pre-population
tribal_plan_prepop = {
    "organization_name": {"field": "tribal_ar.org_name"},
    "uei": {"field": "tribal_ar.unique_entity_identifier"},
    "award_amount": {"field": "tribal_ar.csbg_award_amount"},
    "contact_name": {"field": "tribal_ar.authorized_official_name"},
}
```

Their Python implementation (`transformation.py`) is clean, ~100 lines, handles nested paths, switch/case, constants, and has recursion depth protection. The handler registry pattern (`DEFAULT_HANDLERS`) is extensible — we could add handlers like `"sum"`, `"format"`, `"coalesce"` for CSFEER's financial field needs.

**Adaptation plan:**
- Borrow the `transform_from_mapping()` function pattern
- Extend with CSFEER-specific handlers: `"sum"`, `"prior_year"`, `"default_if_null"`
- Store mapping definitions alongside form definitions in Layer 1
- Use for: prior-year pre-population, cross-form field sharing, UEI-based data import

### 2. Python SDK with Pydantic (COMPATIBLE STACK)

Their Python SDK uses the same stack as CSFEER:

```python
class CommonGrantsBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    def dump(self) -> dict:
        return self.model_dump(mode="json")

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls.model_validate(data)
```

Key patterns worth noting:
- `strict=True` on Pydantic config (catches type errors early)
- `mode="json"` in dump for JSON-serializable output
- `from_attributes=True` for ORM compatibility
- `dump_with_mapping()` integrates transformation at the model level

### 3. DecimalString + Money Types (DIRECTLY USABLE)

```python
# Decimal as string to avoid floating point issues
DecimalString = Annotated[str, BeforeValidator(validate_decimal_string)]

class Money(CommonGrantsBaseModel):
    amount: DecimalString   # "1000000", "500.00", "-100.50"
    currency: str           # "USD"
```

CSFEER's `CurrencyInput` widget already handles display formatting, but the underlying storage is a Python Decimal stored as a JSON number. The `DecimalString` pattern (store as string, validate format) is more robust for JSON serialization round-trips. Worth considering for Layer 1 field type definitions.

### 4. CustomField Extension Mechanism (FUTURE-PROOFING)

```python
class CustomField(CommonGrantsBaseModel):
    name: str
    field_type: CustomFieldType    # string | number | integer | boolean | object | array
    schema_url: HttpUrl | None     # Link to full JSON schema for this field
    value: Any
    description: str | None
```

With `with_custom_fields()` classmethod that dynamically creates extended model classes:
```python
ExtendedOpportunity = OpportunityBase.with_custom_fields(
    custom_fields=[CustomFieldSpec(key="tribal_org_type", field_type="string")],
    model_name="TribalOpportunity"
)
```

This pattern is useful for Phase II when CSFEER needs to support State/Territory forms with additional fields without modifying the core schema.

### 5. Form + Response Separation (VALIDATES OUR APPROACH)

Their `FormBase` / `FormResponseBase` split maps to our `FormDefinition` / `FormEntry` split. Confirms the industry pattern:
- Definition stores structure, validation, layout
- Response stores data, status, errors
- Response references definition by ID

---

## What's NOT Adaptable (and Why)

### Their Forms Are Trivially Simple

The CD511 example — their showcase form — has **11 flat fields with zero calculations, zero conditionals, zero multi-step navigation**:

```json
{
  "properties": {
    "OrganizationName": { "type": "string" },
    "Prefix": { "type": "string", "enum": ["Mr.", "Mrs.", ...] },
    "FirstName": { "type": "string" },
    "SubmittedDate": { "type": "string", "format": "date" }
  },
  "required": ["OrganizationName", "FirstName", "LastName", ...]
}
```

UI Schema is a flat `VerticalLayout` with 11 `Control` elements. No groups, no steps, no pages.

CSFEER's Tribal Annual Report has **40+ fields across multi-step pages with calculated sums, conditional field exclusion, and currency formatting**. Their form schema simply doesn't model this complexity.

### FormJsonSchema and FormUISchema Are Opaque Containers

```typescript
model FormJsonSchema { ...Record<unknown>; }   // Any JSON object
model FormUISchema { ...Record<unknown>; }      // Any JSON object
```

These are passthrough types — the protocol doesn't define what goes inside them. The actual structure comes from JSON Forms library conventions. This means there's no standardized schema-for-the-schema that CSFEER could adopt.

### No Calculated Fields

No `calculation`, `computed`, `derived`, or `formula` concept anywhere in the protocol. Their forms don't need `${personnel} + ${equipment} + ${travel}`.

### No Hard Error vs Soft Warning

`validationErrors` is `Array<unknown>` — an untyped list. No severity levels, no error codes, no structured messages. Their CD511 form has 6 required fields and that's the extent of validation.

### No Conditional Logic

No `enableWhen`, `relevant`, `if/then/else`, or any conditional visibility mechanism. Every field always shows.

### No Multi-Step Navigation

Their UI Schema is a single `VerticalLayout`. No `StepBlock`, `PageBlock`, or wizard pattern. CSFEER needs Steps > Pages > Sections > FieldGroups > Fields.

### No Version Pinning on Responses

`FormResponseBase.formId` references the form by ID, not by version. If the form definition changes, existing responses have no way to know which version they were created against. CSFEER needs `definition_version` pinning per the roadmap.

### Frontend Stack Mismatch

They use React + JSON Forms. CSFEER uses Django templates + django-cotton. The rendering approach doesn't transfer at all.

---

## Comparison to Roadmap Layers

| Roadmap Layer | CommonGrants Has | CommonGrants Doesn't Have |
|---|---|---|
| **Layer 1: Field Definitions** | Field types (string, enum, date), Money type, CustomField extension | Calculated fields, conditional fields, field metadata (review_title, description), field groups |
| **Layer 2: Validation Rules** | Required fields, enum constraints, format validation | Hard vs soft errors, group-level rules, cross-field validation, sum checks, prior-year comparison |
| **Layer 3: Layout** | VerticalLayout with Control elements | Steps, pages, sections, field groups, conditional inclusion, progress indicators |
| **Layer 4: Renderers** | JSON Forms React renderer | Django template renderer, PDF export, API serialization, review page |
| **Cross-cutting: Mapping** | MappingSchema with field/switch/const DSL | Sum handlers, prior-year handlers, coalesce/default handlers |
| **Cross-cutting: Versioning** | version field on FormBase (added v0.3) | Canonical URLs, semver enforcement, derivedFrom, version pinning on responses |

---

## Recommendation

### Adopt These Concepts

1. **MappingSchema pattern** — Borrow the declarative `field`/`switch`/`const` transformation DSL for cross-form pre-population. Extend with CSFEER-specific handlers (`sum`, `prior_year`, `coalesce`). This is the highest-value adaptation.

2. **DecimalString type** — Use string-serialized decimals for currency fields in Layer 1 to avoid JSON floating-point issues.

3. **CustomField extension mechanism** — Build form definitions with an extension point for program-specific fields. Useful when expanding from Tribal to State/Territory forms in Phase II.

4. **Three-schema separation** — Adopt the `jsonSchema` + `uiSchema` + `mapping` pattern as our `definitions` + `layout` + `mapping` in the form engine. This adds the mapping layer that the initial roadmap didn't explicitly include.

5. **Pydantic base model patterns** — `strict=True`, `mode="json"` dump, `from_attributes=True` for ORM compat.

### Don't Adopt

1. **Their form schema structure** — Too simple. Their `FormJsonSchema` and `FormUISchema` are opaque `Record<unknown>` types with no internal structure. We need typed, structured definitions.

2. **Their validation approach** — `Array<unknown>` for errors is inadequate. We need typed `ValidationMessage` with severity, code, message, context.

3. **Their versioning model** — Just a `version?: string` field. We need FHIR-style canonical URLs + semver + derivedFrom + response version pinning.

4. **JSON Forms library** — Wrong stack. We're Django templates, not React.

5. **TypeSpec as definition language** — Adds complexity without clear benefit for CSFEER. Pydantic models → JSON Schema export achieves the same goal with simpler tooling the team already knows.

### Potential Collaboration Point

CommonGrants is an **open standard** actively seeking adoption. CSFEER's reporting forms (post-award) are complementary to CommonGrants' application forms (pre-award). If CSFEER's form engine matures, the `MappingSchema` could bridge the two systems — a Tribal Plan application in CSFEER could map to CommonGrants' canonical model for cross-agency data exchange.

This is a long-term consideration, not an MVP concern, but worth keeping the door open architecturally.

---

## Updated Roadmap Implication

The MappingSchema pattern should be added to the roadmap as a cross-cutting concern:

```
Layer 1: Field Definitions ──────────────────────────────
Layer 2: Validation Rules  ──────────────────────────────
Layer 3: Layout            ──────────────────────────────
Layer M: Mapping (NEW)     ── cross-form pre-population,
                              prior-year data import,
                              UEI-based data linking,
                              future CommonGrants interop
Layer 4: Renderers         ──────────────────────────────
```

The Mapping layer sits alongside Layers 1-3 — it depends on field definitions (Layer 1) but is independent of validation and layout. It's how data flows BETWEEN forms, while Layers 1-3 describe what happens WITHIN a form.

---

*Sources: [HHS/simpler-grants-protocol](https://github.com/HHS/simpler-grants-protocol), [CommonGrants Protocol Spec](https://commongrants.org/protocol/specification/), [ADR 0020: Form Library Framework](https://commongrants.org/governance/adr/0020-form-library-framework/), [CD511 Form](https://commongrants.org/forms/cd511/), [Python SDK](https://github.com/HHS/simpler-grants-protocol/tree/main/lib/python-sdk)*
