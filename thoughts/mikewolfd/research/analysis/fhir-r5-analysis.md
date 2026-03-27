# FHIR R5 Questionnaire / SDC — Deep Analysis for CSFEER

> What can we adapt from [HL7 FHIR R5](https://hl7.org/fhir/questionnaire.html) and [Structured Data Capture (SDC)](https://build.fhir.org/ig/HL7/sdc/)?
> Companion to: [form-engine-roadmap.md](form-engine-roadmap.md), [form-schema-landscape.md](form-schema-landscape.md), [simpler-grants-analysis.md](simpler-grants-analysis.md)

---

## What They Built

Two specifications, layered:

**[FHIR R5 Questionnaire](https://hl7.org/fhir/questionnaire.html)** — The core resource for structured data collection in healthcare. Defines how to describe forms (Questionnaire) and capture responses (QuestionnaireResponse). Part of the FHIR R5 standard (v5.0.0), maturity level 5 (Trial Use). Not healthcare-specific in design — the data model is generic enough for any structured data capture.

**[Structured Data Capture (SDC) IG](https://build.fhir.org/ig/HL7/sdc/)** — An implementation guide that layers advanced form capabilities on top of the base Questionnaire resource via FHIR extensions. Covers calculated fields, pre-population, extraction, advanced rendering, conditional logic, and modular form composition. Currently at v4.0.0-snapshot. This is where the interesting capabilities live.

### Architecture Overview

```
FHIR Questionnaire (core R5)
├── Form definition (items, types, constraints, enableWhen)
├── Versioning (canonical URL + semver + derivedFrom)
└── Response capture (QuestionnaireResponse)
    │
    ↓ extended by
    │
SDC Implementation Guide (extensions)
├── calculatedExpression — FHIRPath-based computed fields
├── initialExpression — pre-population from context
├── enableWhenExpression — advanced conditional logic
├── itemControl — widget type hints (radio, checkbox, slider, etc.)
├── Modular Forms — subQuestionnaire composition + assembly
├── $populate — pre-fill from external data
├── $extract — form data → structured resources
└── Advanced Rendering — styling, tables, collapsible sections
```

Unlike CommonGrants (which defines a protocol for grant data exchange), FHIR Questionnaire is a **form definition standard** — it describes the form itself, not just the data model behind it. This makes it more directly comparable to what CSFEER's form engine does.

---

## The Form Model (What Matters for Us)

### Questionnaire — Form Definition

```json
{
  "resourceType": "Questionnaire",
  "url": "http://acf.gov/questionnaire/tribal-annual-report",
  "version": "2.1.0",
  "versionAlgorithmCoding": { "code": "semver" },
  "name": "TribalAnnualReport",
  "title": "Tribal Annual Report",
  "status": "active",
  "derivedFrom": ["http://acf.gov/questionnaire/tribal-annual-report|2.0.0"],
  "subjectType": ["Organization"],
  "item": [
    {
      "linkId": "step-1",
      "text": "Organization Information",
      "type": "group",
      "item": [
        {
          "linkId": "org_name",
          "text": "Organization Name",
          "type": "string",
          "required": true,
          "maxLength": 200
        },
        {
          "linkId": "uei",
          "text": "Unique Entity Identifier (UEI)",
          "type": "string",
          "required": true
        },
        {
          "linkId": "has_variance",
          "text": "Does the budget have a variance from the approved amount?",
          "type": "boolean"
        },
        {
          "linkId": "variance_explanation",
          "text": "Explain the variance",
          "type": "text",
          "enableWhen": [
            {
              "question": "has_variance",
              "operator": "=",
              "answerBoolean": true
            }
          ]
        }
      ]
    }
  ]
}
```

**Key structural properties:**

- **Recursive item tree** — Items contain child items. `group` type items organize children without collecting data. This is FHIR's answer to Steps > Pages > Sections.
- **linkId** — Every item has a unique identifier within the questionnaire. Analogous to our `field_name`.
- **type** — Enum of: `group`, `display`, `boolean`, `decimal`, `integer`, `date`, `dateTime`, `time`, `string`, `text`, `url`, `coding`, `quantity`, `reference`, `attachment`. R5 changed `choice`/`open-choice` to `coding` with `answerConstraint`.
- **enableWhen** — Conditional visibility with operators: `exists`, `=`, `!=`, `>`, `<`, `>=`, `<=`. Multiple conditions combined via `enableBehavior` (`all` or `any`).
- **required, readOnly, maxLength, repeats** — Built-in constraints.
- **answerOption / answerValueSet** — Choice options inline or by reference.

### QuestionnaireResponse — Submission Data

```json
{
  "resourceType": "QuestionnaireResponse",
  "questionnaire": "http://acf.gov/questionnaire/tribal-annual-report|2.1.0",
  "status": "in-progress",
  "authored": "2026-01-15T10:30:00Z",
  "item": [
    {
      "linkId": "step-1",
      "item": [
        {
          "linkId": "org_name",
          "answer": [{ "valueString": "Example Tribal Organization" }]
        },
        {
          "linkId": "uei",
          "answer": [{ "valueString": "ABC123DEF456" }]
        }
      ]
    }
  ]
}
```

**Key properties:**

- **questionnaire** — Canonical URL reference, **version-pinned** (`|2.1.0`). This is what CSFEER needs — responses locked to the definition version they were created against.
- **status** — `in-progress | completed | amended | entered-in-error | stopped`. More states than CommonGrants' `notStarted | inProgress | complete`.
- **item structure mirrors Questionnaire** — Response items nest the same way as definition items. Each answer carries typed values (`valueString`, `valueDecimal`, `valueBoolean`, etc.).
- **Multiple answers per item** — When `repeats: true` on the Questionnaire item, the response can have multiple `answer` entries.

### R5-Specific Changes (vs R4)

R5 added several elements relevant to CSFEER:

| New in R5 | Purpose | CSFEER Relevance |
|---|---|---|
| `versionAlgorithmCoding` | Declares how versions are compared (supports `semver`) | Directly maps to our versioning needs |
| `answerConstraint` | Controls whether answers must come from answerOption/ValueSet only | Replaces R4's separate `choice` vs `open-choice` types |
| `disabledDisplay` | How disabled items render: `hidden` or `protected` (visible but uneditable) | Maps to our excluded-but-default-valued fields |
| `copyrightLabel` | Short copyright string for page footers | Minor — could use for federal form citations |

---

## SDC Extensions (The Advanced Features)

The base Questionnaire resource handles simple forms. SDC is where FHIR addresses the complexity CSFEER needs.

### calculatedExpression — Computed Fields (DIRECTLY RELEVANT)

```json
{
  "linkId": "total_costs",
  "text": "Total Costs",
  "type": "decimal",
  "readOnly": true,
  "extension": [
    {
      "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-calculatedExpression",
      "valueExpression": {
        "language": "text/fhirpath",
        "expression": "%resource.item.where(linkId='personnel').answer.value + %resource.item.where(linkId='equipment').answer.value + %resource.item.where(linkId='travel').answer.value"
      }
    }
  ]
}
```

The PHQ-9 example uses a more elegant aggregate:
```
%resource.answers().value.ordinal().sum()
```

**How this maps to CSFEER:**

CSFEER's `ACFCalculatedField` does the same thing — sums source fields. The FHIR approach uses FHIRPath expressions, which are more powerful (arbitrary computation) but also more verbose and require a FHIRPath evaluator. CSFEER's approach (list of source field names + implicit sum) is simpler for the specific use case.

**Key difference:** FHIRPath is a full expression language. CSFEER's calculated fields are currently sum-only. If we need other operations (average, percentage, prior-year delta), FHIRPath shows the pattern — but we'd want a simpler expression syntax than FHIRPath itself.

### initialExpression — Pre-Population (HIGH VALUE)

```json
{
  "linkId": "org_name",
  "text": "Organization Name",
  "type": "string",
  "extension": [
    {
      "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-initialExpression",
      "valueExpression": {
        "language": "text/fhirpath",
        "expression": "%subject.name"
      }
    }
  ]
}
```

**Why this matters for CSFEER:**

The PRD requires cross-form pre-population — Tribal Plan fields should pre-populate from prior Tribal AR data. FHIR's approach uses `launchContext` to inject external data into the form evaluation context, then `initialExpression` to extract values from that context.

The SDC `$populate` operation works as follows:
1. Client sends a `$populate` request with context parameters (e.g., prior submission, organization data)
2. Server evaluates `initialExpression` extensions against the context
3. Server returns a pre-filled QuestionnaireResponse

**Adaptation for CSFEER:**
- The `launchContext` concept (declaring what external data a form needs) maps to our pre-population sources
- The `initialExpression` concept (declarative extraction from context) is cleaner than CommonGrants' `MappingSchema` for same-system pre-population
- We'd replace FHIRPath with our simpler expression syntax: `"${prior_year.org_name}"` rather than `"%subject.name"`

### enableWhenExpression — Advanced Conditional Logic (USEFUL)

Base `enableWhen` handles simple comparisons. SDC adds `enableWhenExpression` for complex conditions:

```json
{
  "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-enableWhenExpression",
  "valueExpression": {
    "language": "text/fhirpath",
    "expression": "%resource.item.where(linkId='budget_total').answer.value > 500000"
  }
}
```

CSFEER currently uses `FieldFilterField` for conditional exclusion — a checkbox that controls which fields appear. This is simpler than FHIR's general expression-based approach but less flexible. For MVP, our `FieldFilterField` suffices. For Phase II (State/Territory forms with more complex conditional logic), the expression-based approach may be needed.

### itemControl — Widget Type Hints (CONCEPTUALLY USEFUL)

SDC defines a vocabulary for widget type hints:

| itemControl Code | Widget Type | CSFEER Equivalent |
|---|---|---|
| `drop-down` | Select dropdown | `Select` widget |
| `radio-button` | Radio button group | `RadioSelect` widget |
| `check-box` | Checkbox group | `CheckboxSelectMultiple` |
| `autocomplete` | Typeahead search | Not yet needed |
| `slider` | Numeric slider | Not yet needed |
| `text-box` | Multi-line text | `Textarea` widget |
| `help` | Help/info text display | `description` in `FieldMetadata` |
| `gtable` / `table` | Grid/table layout | Not yet needed |
| `collapsible` | Expandable section | Could use for long sections |

**Key insight:** FHIR separates **what** a field is (type: `coding`, choices: [...]) from **how** to render it (itemControl: `radio-button`). This is exactly the Layer 1 / Layer 4 separation in our roadmap. The field definition says "this is a choice from these options." The renderer decides whether to show it as a dropdown, radio buttons, or checkboxes.

Our current code fuses this — `RadioSelect` is both the type and the widget. The roadmap's Layer 1 `FieldDefinition.field_type: choice` + Layer 4 renderer deciding the widget is the FHIR-aligned approach.

### Modular Forms — subQuestionnaire + Assembly (FUTURE VALUE)

SDC supports composing forms from reusable modules:

```json
{
  "linkId": "contact-section",
  "type": "display",
  "text": "Contact information (fallback text if assembly fails)",
  "extension": [
    {
      "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-subQuestionnaire",
      "valueCanonical": "http://acf.gov/questionnaire/contact-info-module|1.0.0"
    }
  ]
}
```

Assembly process:
1. Author creates modular questionnaires with `assembleExpectation` flags
2. `$assemble` operation resolves `subQuestionnaire` references
3. Assembled questionnaire gets `assembledFrom` extensions tracking provenance
4. `linkIdPrefix` prevents ID collisions when reusing modules

**Why this matters for CSFEER:**

The PRD mentions long form and short form as variants. Currently, `TribalLongForm` and `TribalShortForm` are separate Python classes with duplicated field definitions. FHIR's modular approach suggests:
- Shared sections (org info, contact info, budget) as reusable modules
- Long form assembles all modules
- Short form assembles a subset
- `derivedFrom` links the short form to the long form

This is a Phase II consideration. For MVP, Python class inheritance achieves the same result. But the concept of **authored modular, assembled for use** is architecturally sound and worth designing for.

### $extract — Form Data to Structured Resources (INTERESTING PATTERN)

SDC defines three extraction mechanisms for transforming form responses into structured data:

1. **Definition-based extraction** — Field-level annotations map each item to a target resource property
2. **Observation-based extraction** — Each answer becomes a FHIR Observation resource
3. **StructureMap-based extraction** — Full transformation language for complex mappings

This parallels CommonGrants' `MappingSchema` but is more structured. CSFEER's equivalent need: extracting form data for federal reporting, CSV export, and cross-form pre-population.

**Key difference from CommonGrants:** FHIR extraction is **form → structured resources** (one-directional with separate population). CommonGrants' mapping is **bidirectional** (`mappingTo` + `mappingFrom`). CSFEER needs both directions:
- **Populate direction:** Prior year data → current form (like FHIR $populate)
- **Extract direction:** Form data → export format, reporting, cross-form sharing (like FHIR $extract)

### Advanced Rendering Extensions

| Extension | Purpose | CSFEER Relevance |
|---|---|---|
| `rendering-style` | CSS styling on labels (`color:red;`) | Low — we use USWDS classes |
| `rendering-xhtml` | Rich HTML in question text | Low — Django templates handle this |
| `displayCategory` | Categorizes display items (instructions, security) | Medium — maps to our section descriptions |
| `choiceOrientation` | Horizontal vs vertical for radio/checkbox | Low — USWDS handles this |
| `width` | Column width hints | Medium — could inform responsive layout |
| `collapsible` | Expandable/collapsible sections | Medium — useful for dense forms |
| `entryFormat` | Display format hint (e.g., "MM/DD/YYYY") | Medium — maps to input masks |

---

## What's Directly Adaptable

### 1. Versioning Model — Canonical URL + Semver + DerivedFrom (HIGHEST VALUE)

This is the most mature versioning model in the standards landscape. Already identified in the landscape doc as the best-in-class approach.

```python
# FHIR-inspired versioning for CSFEER
class FormIdentity(BaseModel):
    url: str                    # "acf.gov/forms/tribal-annual-report"
    version: str                # "2.1.0" (semver, explicit algorithm)
    derived_from: str | None    # "acf.gov/forms/tribal-annual-report|2.0.0"
    status: Literal["draft", "active", "retired"]
```

R5's addition of `versionAlgorithmCoding` (explicitly declaring `semver`) makes version comparison unambiguous. The `derivedFrom` field enables the long-form-to-short-form relationship.

**Response version pinning** is equally important:
```python
class FormEntry(Model):
    questionnaire_version: str  # "acf.gov/forms/tribal-annual-report|2.1.0"
    # Locked at creation time — form definition changes don't affect existing responses
```

This directly solves PRD requirement VC-01 (multiple simultaneous form definition versions).

### 2. enableWhen / enableWhenExpression — Conditional Logic Pattern (HIGH VALUE)

FHIR's two-tier conditional system maps well to CSFEER's needs:

**Tier 1 (simple, core spec):** `enableWhen` with operators (`=`, `!=`, `>`, `<`, `exists`)
```python
# CSFEER equivalent
class EnableCondition(BaseModel):
    field: str              # linkId of controlling field
    operator: str           # "=", "!=", ">", "<", "exists"
    value: Any              # comparison value
```

**Tier 2 (complex, SDC):** `enableWhenExpression` with full expression language
```python
class EnableExpression(BaseModel):
    expression: str         # "${budget_total} > 500000"
```

Our current `FieldFilterField` is a special case of Tier 1 enableWhen — a boolean checkbox that controls visibility. Generalizing to the enableWhen pattern adds support for:
- Show field X when field Y equals a specific value (not just checkbox)
- Show field X when field Y is greater than a threshold
- Combine multiple conditions with AND/OR

This is needed for State/Territory forms in Phase II where conditional logic is more complex than "which programs apply."

### 3. Definition/Response Separation with Version Pinning (VALIDATES APPROACH)

FHIR's Questionnaire/QuestionnaireResponse split is the same pattern as our FormDefinition/FormEntry split. The key refinement from FHIR R5:

- Response references definition by **canonical URL + version** (not just ID)
- This means changing the form definition creates a new version, existing responses stay pinned to the old version
- The `amended` status allows updating a response against its original definition version

This validates and strengthens the approach already proposed in the roadmap.

### 4. Recursive Item Tree for Layout (ARCHITECTURAL INSIGHT)

FHIR uses a **single recursive `item` type** for all structural levels:

```
item (type: group, linkId: "step-1")       → Step
  item (type: group, linkId: "page-1")     → Page
    item (type: group, linkId: "section-a") → Section
      item (type: decimal, linkId: "amount") → Field
      item (type: display, linkId: "help")   → Help text
```

CSFEER's roadmap uses **distinct types** per level: `Step > Page > Section > FieldRef`. This is more explicit and self-documenting, but less flexible. The FHIR approach means you can nest to arbitrary depth without new types.

**Recommendation:** Keep CSFEER's explicit types (they map directly to USWDS navigation patterns — step indicator, page, fieldset). But add a `children` pattern on each type so sections can contain sub-sections if needed in Phase II.

### 5. disabledDisplay — Hidden vs Protected (USEFUL DETAIL)

R5 added `disabledDisplay` with two values:
- `hidden` — disabled items are not shown at all
- `protected` — disabled items are shown but not editable

CSFEER currently uses `default_if_excluded` to set a value when a field is excluded. The `protected` concept adds a visual distinction: "this field exists and has a value, but you can't change it." This is useful for pre-populated fields from federal data (UEI, organization name) that should be visible but locked.

### 6. SDC Calculated Expression Pattern (CONCEPT, NOT SYNTAX)

The concept of declarative calculated expressions is directly applicable:

```python
# CSFEER adaptation (simpler than FHIRPath)
class CalculatedFieldDef(BaseModel):
    target_field: str                    # "total_costs"
    expression: str                      # "${personnel} + ${equipment} + ${travel}"
    language: Literal["simple"] = "simple"  # Our DSL, not FHIRPath
```

We don't want FHIRPath itself (verbose, requires a specialized evaluator, healthcare-oriented). But the **pattern** — a string expression evaluated at runtime against current field values — is exactly right. Combined with the ODK-style `${field_name}` syntax from the landscape doc, this gives us:

```python
# Calculated fields
"${personnel} + ${equipment} + ${travel}"

# Constraint validation
"${total} == ${sum_items}"

# Conditional enablement
"${budget_total} > 500000"
```

One expression syntax for three use cases (calculations, validations, conditions).

---

## What's NOT Adaptable (and Why)

### FHIRPath Expression Language

FHIRPath is powerful but wrong for CSFEER:

```
%resource.item.where(linkId='personnel').answer.value +
%resource.item.where(linkId='equipment').answer.value +
%resource.item.where(linkId='travel').answer.value
```

vs. what CSFEER needs:

```
${personnel} + ${equipment} + ${travel}
```

FHIRPath requires a dedicated evaluator library, navigates FHIR resource structures (not flat key-value forms), and is verbose for simple arithmetic. CSFEER should use a simpler DSL.

### No Hard Error vs Soft Warning Distinction

FHIR validation is binary — a response is valid or not. There is no built-in concept of severity levels on validation messages. The closest thing is `Questionnaire.item.required` (hard constraint) vs. optional fields, but there's no "this is wrong but you can submit anyway" pattern.

CSFEER needs:
- **Hard errors:** "Total of Sections A-C must equal your CSBG award amount" (blocks submission)
- **Warnings:** "This value differs significantly from last year — please verify" (informs only)

This gap exists in every standard surveyed. CSFEER must implement it natively.

### No Multi-Step Workflow States

QuestionnaireResponse status: `in-progress | completed | amended | entered-in-error | stopped`

CSFEER workflow: `draft → in-progress → review → submitted → federal-review → approved/revision-requested → finalized`

FHIR's status enum covers the respondent's lifecycle, not the organizational approval workflow. CSFEER needs the full workflow state machine that sits outside the form engine (in the application layer, not the schema layer).

### Healthcare-Centric Assumptions

- `subjectType` assumes FHIR resource types (`Patient`, `Practitioner`)
- `coding` type assumes a healthcare terminology system (LOINC, SNOMED)
- `quantity` type assumes clinical units
- `reference` type points to FHIR resources

These don't break anything — CSFEER would simply not use these healthcare-specific features — but they add conceptual overhead when reading the spec.

### No Financial Sum Checks in Core Spec

No native "line items must sum to total" validation. The SDC `calculatedExpression` can compute a sum, but there's no built-in way to say "field X must equal the calculatedExpression value of field Y." You'd need to combine calculatedExpression with a custom validation extension.

CSFEER's `ACFCalculatedField` already does this implicitly — the calculated field shows what the total should be, and the UI shows a mismatch. This is simpler than the FHIR approach.

### No Role-Based Field Visibility

No concept of "federal reviewer sees field X, grantee sees field Y." FHIR forms are authored for a single audience. Role-based visibility is an application concern, not a form definition concern.

### Verbose JSON Structure

A simple text field in FHIR:
```json
{
  "linkId": "org_name",
  "text": "Organization Name",
  "type": "string",
  "required": true,
  "maxLength": 200
}
```

vs. a simple text field in CSFEER's Pydantic model:
```python
org_name = ACFCharField(title="Organization Name", max_length=200, required=True)
```

FHIR's JSON is more verbose per field. For a 40+ field form like Tribal AR, this adds up. Pydantic's Python DSL is more compact for authoring. However, FHIR's JSON is better for non-programmer authoring (form builder UI).

---

## Comparison to Roadmap Layers

| Roadmap Layer | FHIR R5 Has | FHIR R5 Doesn't Have |
|---|---|---|
| **Layer 1: Field Definitions** | Item types (string, decimal, date, boolean, coding, quantity), constraints (required, maxLength, readOnly, repeats), metadata (text), enableWhen, answerOption/ValueSet | review_title, description metadata, field_type enum as clean as ours, financial-specific types (currency), calculated_from |
| **Layer 2: Validation Rules** | Required fields, enableWhen constraints, maxLength, SDC regex/minValue/maxValue | Hard vs soft errors, group-level sum checks, cross-form validation, prior-year comparison |
| **Layer 3: Layout** | Recursive item groups (arbitrary nesting), display items for instructions | Explicit Step/Page/Section types, progress indicators, field group descriptions, conditional page inclusion |
| **Layer 4: Renderers** | SDC itemControl (widget hints), rendering-style, rendering-xhtml, collapsible, width | Django template renderer, USWDS component mapping, PDF export, review page layout |
| **Cross-cutting: Mapping** | SDC $populate (initialExpression) + $extract (definition/observation/StructureMap) | Simple DSL mapping (CommonGrants-style), bidirectional field/switch/const |
| **Cross-cutting: Versioning** | Canonical URLs, semver (versionAlgorithmCoding), derivedFrom, status lifecycle, response version pinning | — (This is complete and best-in-class) |
| **Cross-cutting: Composition** | Modular forms (subQuestionnaire, $assemble, assembledFrom, linkIdPrefix) | — (More than we need for MVP, perfect for Phase II) |

---

## Comparison to CommonGrants Analysis

| Aspect | CommonGrants | FHIR R5 + SDC |
|---|---|---|
| **Form complexity** | Trivially simple (11 flat fields) | Medium complexity (PHQ-9 has calculated scores, conditional logic) |
| **Schema structure** | Opaque `Record<unknown>` for jsonSchema/uiSchema | Typed, recursive item model with defined types |
| **Calculated fields** | None | SDC calculatedExpression (FHIRPath) |
| **Conditional logic** | None | enableWhen (core) + enableWhenExpression (SDC) |
| **Pre-population** | MappingSchema (field/switch/const DSL) | SDC $populate + initialExpression + launchContext |
| **Data extraction** | MappingSchema (bidirectional) | SDC $extract (three mechanisms) |
| **Versioning** | `version?: string` (weak) | Canonical URL + semver + derivedFrom + status (excellent) |
| **Response version pinning** | formId only (no version) | Canonical URL with version suffix |
| **Modular composition** | None | subQuestionnaire + $assemble |
| **Widget hints** | None (defers to JSON Forms) | itemControl vocabulary |
| **Python SDK** | Pydantic models (compatible stack) | HAPI FHIR (Java), fhir.resources (Python — Pydantic-based) |

**Key takeaway:** CommonGrants' highest value is the `MappingSchema` DSL for data transformation. FHIR's highest value is the versioning model, conditional logic pattern, and the conceptual separation of definition/response/rendering. The two standards solve different problems and their adaptations are complementary.

---

## Recommendation

### Adopt These Concepts

1. **Versioning model** (HIGHEST PRIORITY) — Canonical URL + semver + derivedFrom + status lifecycle + response version pinning. This is the most mature approach in any standard surveyed. Already recommended in the landscape doc; FHIR R5's `versionAlgorithmCoding` adds explicit semver declaration.

2. **enableWhen conditional pattern** (HIGH VALUE) — Generalize `FieldFilterField` to a declarative conditional system. Start with the simple tier (field + operator + value), add expression-based tier later. This unblocks State/Territory forms.

3. **disabledDisplay: hidden vs protected** (MEDIUM VALUE) — Add a `display_when_disabled` property to `FieldDefinition`. Use `protected` for pre-populated fields (visible but locked), `hidden` for truly excluded fields.

4. **itemControl separation** (MEDIUM VALUE, VALIDATES ROADMAP) — Confirms Layer 1/Layer 4 separation. Field definitions say "this is a choice field with these options." Renderers decide radio vs dropdown vs checkbox based on option count, screen size, or explicit hint.

5. **Modular form composition concept** (FUTURE VALUE) — Design shared sections (org info, contact info, budget summary) as reusable modules. Long form assembles all modules; short form assembles a subset. Not MVP, but design field naming to enable it (use consistent linkIds across form variants).

6. **$populate / initialExpression pattern** (HIGH VALUE) — Declarative pre-population where each field declares its data source. Cleaner than imperative pre-population logic. Combine with CommonGrants' `MappingSchema` for cross-system data (use mapping for external data, initialExpression for same-system prior-year data).

### Don't Adopt

1. **FHIRPath** — Too verbose, healthcare-oriented, requires specialized evaluator. Use a simpler expression DSL (`${field_name}` syntax).

2. **Recursive item tree for layout** — Keep CSFEER's explicit Step > Page > Section > FieldRef hierarchy. It maps directly to USWDS navigation patterns and is more self-documenting.

3. **FHIR resource model** — Don't wrap form data in FHIR resource structures. CSFEER's Django ORM + Pydantic is the right persistence layer. Adopting FHIR's resource model would add massive overhead for no benefit.

4. **SDC profiles as-is** — SDC is an implementation guide for FHIR servers. CSFEER is a Django application. Adopt the concepts, not the extension URLs or profile conformance requirements.

5. **FHIR validation approach** — Binary valid/invalid is insufficient. Build the hard error / soft warning system natively as planned in the roadmap.

6. **`fhir.resources` Python library** — It's Pydantic-based but tightly coupled to the full FHIR resource model. Cherry-pick patterns (strict validation, JSON-mode dump) rather than taking the dependency.

### Potential Interoperability Point

FHIR Questionnaire is increasingly used beyond healthcare — clinical trials, research surveys, and government data collection. If CSFEER's form definitions can **export to FHIR Questionnaire format**, it opens interoperability with:
- NLM's [LHC-Forms](https://lhcforms.nlm.nih.gov/) — open-source form renderer supporting SDC
- HHS [FHIR infrastructure](https://clinicaltrials.gov/data-api/fhir) — ClinicalTrials.gov already uses FHIR
- CommonGrants protocol — which uses JSON Schema internally but could bridge to FHIR

This is a long-term consideration. The immediate design implication: CSFEER's Layer 1 `FieldDefinition` should include enough information to generate a FHIR Questionnaire item (linkId, type, constraints, enableWhen). If we design with this export path in mind, we don't foreclose it.

---

## Updated Roadmap Implications

FHIR R5 analysis reinforces and extends the landscape doc recommendations:

```
Layer 1: Field Definitions ──────────────────────────────
  + enableWhen conditional pattern (from FHIR)
  + disabledDisplay: hidden vs protected (from FHIR R5)
  + field type / widget type separation (validated by itemControl)

Layer 2: Validation Rules  ──────────────────────────────
  + expression-based validation (concept from SDC, syntax from ODK)
  + hard error vs soft warning (CSFEER-original, no standard has this)

Layer 3: Layout            ──────────────────────────────
  + keep explicit Step/Page/Section types (not recursive items)
  + collapsible sections (from SDC)

Layer M: Mapping (from CommonGrants analysis)
  + field/switch/const DSL for cross-system mapping
  + initialExpression pattern for same-system pre-population (from SDC)
  + $populate concept for declarative pre-fill

Layer V: Versioning (from FHIR R5)
  + canonical URL + semver + derivedFrom + status
  + response version pinning
  + modular composition for Phase II

Layer 4: Renderers         ──────────────────────────────
  + itemControl concept for widget hints (from SDC)
  + renderer decides widget type, definition declares field type
```

The Versioning layer is now a first-class cross-cutting concern alongside Mapping. Together, they handle:
- **Versioning:** How forms evolve over time (FHIR-inspired)
- **Mapping:** How data flows between forms and external systems (CommonGrants-inspired)
- **Composition:** How forms are assembled from modules (SDC-inspired, Phase II)

---

*Sources: [FHIR R5 Questionnaire](https://hl7.org/fhir/questionnaire.html), [FHIR R5 QuestionnaireResponse](https://www.hl7.org/fhir/questionnaireresponse.html), [FHIR SDC IG](https://build.fhir.org/ig/HL7/sdc/), [SDC Rendering](https://build.fhir.org/ig/HL7/sdc/rendering.html), [SDC Modular Forms](https://build.fhir.org/ig/HL7/sdc/en/modular.html), [SDC Calculated Expression](http://hl7.org/fhir/uv/sdc/STU3/StructureDefinition-sdc-questionnaire-calculatedExpression.html), [LHC-Forms (NLM)](https://lhcforms.nlm.nih.gov/), [FHIR R5 Item Types](http://hl7.org/fhir/valueset-item-type.html), [SDC PHQ-9 Example](https://hl7.org/fhir/uv/sdc/3.0.0-preview/Questionnaire-questionnaire-sdc-profile-example-PHQ9.json.html), [HAPI FHIR Questionnaire Renderer](https://hapifhir.io/hapi-fhir/apidocs/hapi-fhir-structures-r5/src-html/org/hl7/fhir/r5/renderers/QuestionnaireRenderer.html)*
