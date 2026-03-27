# SHACL (Shapes Constraint Language) — Analysis for CSFEER

> What can we adapt from [W3C SHACL](https://www.w3.org/TR/shacl/) and its form-generation ecosystem?
> Companion to: [form-engine-roadmap.md](form-engine-roadmap.md), [form-schema-landscape.md](form-schema-landscape.md)

---

## What SHACL Is

SHACL is a W3C Recommendation (2017) for validating RDF graph data. It defines **shapes** — sets of constraints — that RDF data must conform to. Think of it as "JSON Schema for knowledge graphs."

Two specs, layered:

**[SHACL Core](https://www.w3.org/TR/shacl/)** — W3C Recommendation. NodeShapes, PropertyShapes, 30+ built-in constraint types, three severity levels, structured validation reports.

**[SHACL Advanced Features (SHACL-AF)](https://w3c.github.io/shacl/shacl-af/)** — W3C Working Group Note. SPARQL-based constraints, custom constraint components, expression constraints, inference rules (TripleRules, SPARQLRules).

A third vocabulary extends SHACL for UI:

**[DASH (Data Shapes)](https://datashapes.org/dash)** — TopQuadrant-maintained vocabulary. Adds `dash:editor` and `dash:viewer` properties for form field widget selection, plus a scoring system for automatic widget matching.

### Architecture Overview

```
SHACL NodeShapes + PropertyShapes (Turtle/RDF)
    ↓ interpreted by
SHACL Validator (pySHACL, rdf-validate-shacl)
    ↓ produces
Validation Report (sh:conforms, sh:ValidationResult[])
    ↓ consumed by
Application logic

SHACL Shapes + DASH vocabulary
    ↓ interpreted by
Form Generator (shacl-form, TopBraid EDG)
    ↓ renders
HTML form with inline validation
    ↓ produces
RDF data (Turtle, JSON-LD, N-Triples)
```

The fundamental data model is **RDF** (subject-predicate-object triples), not JSON key-value pairs. This is the single most important architectural difference from every other standard analyzed.

---

## The Form Model (What Matters for Us)

### PropertyShape — Field Definition

```turtle
:PersonShape a sh:NodeShape ;
    sh:targetClass schema:Person ;
    sh:property [
        sh:path schema:givenName ;       # Field identifier (predicate)
        sh:name "First Name" ;            # Display label
        sh:description "Legal first name" ; # Help text
        sh:datatype xsd:string ;          # Data type
        sh:minCount 1 ;                   # Required
        sh:maxLength 100 ;               # Max length
        sh:order 1 ;                      # Display order
        sh:group :PersonalInfoGroup ;     # Section grouping
    ] ;
    sh:property [
        sh:path schema:email ;
        sh:name "Email Address" ;
        sh:datatype xsd:string ;
        sh:pattern "^[^@]+@[^@]+$" ;     # Regex validation
        sh:minCount 1 ;
        sh:resultSeverity sh:Violation ;  # Hard error
    ] ;
    sh:property [
        sh:path :phoneNumber ;
        sh:name "Phone Number" ;
        sh:datatype xsd:string ;
        sh:minCount 0 ;                   # Optional
        sh:resultSeverity sh:Warning ;    # Soft warning if missing
    ] .
```

**Key insight:** SHACL's PropertyShape combines field definition, validation, and basic UI hints in a single declaration. This is similar to XForms' `<bind>` element — one place defines type, constraints, and relevance. But SHACL adds severity levels natively, which XForms lacks.

### Property Groups — Section Organization

```turtle
:PersonalInfoGroup a sh:PropertyGroup ;
    rdfs:label "Personal Information" ;
    sh:order 1 .

:AddressGroup a sh:PropertyGroup ;
    rdfs:label "Address" ;
    sh:order 2 .
```

Properties reference groups via `sh:group`. Groups provide ordering and labeling. Form generators render groups as accordion sections or fieldsets.

**Limitation:** Groups are flat — no nesting. No `sh:PropertyGroup` within another `sh:PropertyGroup`. CSFEER needs Steps > Pages > Sections > FieldGroups > Fields.

### DASH — UI Widget Hints

```turtle
:PersonShape sh:property [
    sh:path :biography ;
    sh:name "Biography" ;
    sh:datatype xsd:string ;
    dash:editor dash:TextAreaEditor ;     # Multi-line text
    dash:singleLine false ;
] ;
sh:property [
    sh:path :country ;
    sh:name "Country" ;
    sh:in ("US" "CA" "UK" "AU") ;         # Enum values
    dash:editor dash:EnumSelectEditor ;   # Dropdown widget
] ;
sh:property [
    sh:path :birthDate ;
    sh:datatype xsd:date ;
    dash:editor dash:DatePickerEditor ;   # Calendar widget
] .
```

DASH provides 14 editor widgets and 10 viewer widgets. A scoring system (0-100) lets widgets self-evaluate their suitability based on constraints — `xsd:dateTime` automatically scores high for `DateTimePickerEditor` without explicit declaration.

### Validation Report — Structured Error Output

```turtle
[ a sh:ValidationReport ;
    sh:conforms false ;
    sh:result [
        a sh:ValidationResult ;
        sh:resultSeverity sh:Violation ;          # Hard error
        sh:focusNode ex:Person123 ;               # Which record
        sh:resultPath schema:email ;              # Which field
        sh:value "invalid-email" ;                # The bad value
        sh:resultMessage "Must match email format" ; # Human message
        sh:sourceConstraintComponent sh:PatternConstraintComponent ;
        sh:sourceShape :EmailPropertyShape ;
    ] ;
    sh:result [
        a sh:ValidationResult ;
        sh:resultSeverity sh:Warning ;            # Soft warning
        sh:focusNode ex:Person123 ;
        sh:resultPath :phoneNumber ;
        sh:resultMessage "Phone number recommended" ;
    ] ;
] .
```

**This is SHACL's strongest feature for CSFEER.** The validation report gives:
- `sh:resultSeverity` — three built-in levels: `sh:Violation`, `sh:Warning`, `sh:Info` (plus custom)
- `sh:resultPath` — which field failed (supports property paths for nested data)
- `sh:resultMessage` — human-readable error text
- `sh:sourceConstraintComponent` — which constraint type failed (programmatic handling)
- `sh:value` — the specific invalid value

This maps directly to the PRD requirement for **hard errors vs. warnings/notifications** with clear visual distinction.

---

## What's Directly Adaptable

### 1. Three-Level Severity Model (HIGH VALUE)

SHACL's `sh:Violation` / `sh:Warning` / `sh:Info` is the only standard in our survey that natively supports the hard error vs. soft warning distinction the PRD requires:

```python
# SHACL severity → CSFEER validation severity
SEVERITY_MAP = {
    "sh:Violation": "error",     # Blocks submission
    "sh:Warning": "warning",     # Inform only, do not block
    "sh:Info": "info",           # FYI (e.g., "this changed from last year")
}
```

No other analyzed standard has this:
- **XForms** — binary valid/invalid on `<constraint>`
- **FHIR R5** — constraints are all-or-nothing; severity is in `OperationOutcome`, not the questionnaire
- **JSON Schema** — pass/fail only
- **CommonGrants** — `Array<unknown>` for errors

**Adaptation plan:**
- Adopt the three-level severity concept for Layer 2 validation rules
- Each validation rule in CSFEER's form definitions should declare its severity
- Validation engine returns structured results with severity, field path, message, and constraint type
- UI renders differently per severity: red error borders (violation), yellow warning icons (warning), blue info tooltips (info)

### 2. Structured Validation Reports (HIGH VALUE)

SHACL's `ValidationResult` structure is more disciplined than any other standard's error reporting:

```python
# Inspired by SHACL's ValidationResult
@dataclass
class ValidationMessage:
    severity: Literal["error", "warning", "info"]
    field_path: str                  # e.g., "step2.page1.personnel_costs"
    message: str                     # Human-readable
    constraint_type: str             # e.g., "required", "sum_check", "pattern"
    actual_value: Any | None = None  # The offending value
    source_rule: str | None = None   # Which rule generated this
```

The `sourceConstraintComponent` concept is particularly useful — it tells the UI *what kind* of constraint failed, enabling different error rendering strategies per constraint type (e.g., sum mismatch shows a calculation breakdown, pattern mismatch shows the expected format).

**Adaptation plan:**
- Model `ValidationMessage` after SHACL's `ValidationResult`
- Include constraint type for programmatic error handling
- Include actual value for debugging and admin views
- Include source rule reference for traceability

### 3. Constraint Composition (MODERATE VALUE)

SHACL supports logical composition of constraints:

```turtle
# sh:and — all must pass
sh:and (
    [ sh:minInclusive 0 ]
    [ sh:maxInclusive 100 ]
)

# sh:or — at least one must pass
sh:or (
    [ sh:datatype xsd:string ]
    [ sh:datatype xsd:integer ]
)

# sh:not — must NOT match
sh:not [ sh:hasValue "N/A" ]

# sh:xone — exactly one must pass (exclusive or)
sh:xone (
    [ sh:pattern "^\\d{5}$" ]         # 5-digit zip
    [ sh:pattern "^\\d{5}-\\d{4}$" ]  # zip+4
)
```

CSFEER's validation rules will need "either A or B must be provided" and "if A is provided, B must also be provided" patterns. SHACL's `sh:or`, `sh:and`, `sh:xone`, and `sh:not` operators provide a clean vocabulary for expressing these.

**Adaptation plan:**
- Adopt the `and`/`or`/`not`/`xone` composition vocabulary for cross-field validation rules
- These become operators in the validation rule DSL, not direct SHACL imports

### 4. Property Path Expressions (MODERATE VALUE)

SHACL supports complex property paths for validating nested/related data:

```turtle
# Multi-hop: validate postal code through address
sh:path ( schema:address schema:postalCode )

# Inverse: validate from child's perspective
sh:path [ sh:inversePath schema:parent ]

# Alternative: either email or phone must exist
sh:path [ sh:alternativePath ( schema:email schema:telephone ) ]
```

For CSFEER's cross-field dependencies (e.g., "total of sections A-C must equal award amount"), property paths could express field references more precisely than flat string identifiers.

**Adaptation plan:**
- Consider dot-path syntax inspired by SHACL property paths for cross-field references
- e.g., `step2.page1.personnel_costs` rather than flat `personnel_costs` field names
- Useful when the same field name appears in different sections

### 5. Widget Scoring Pattern (LOW VALUE)

DASH's widget scoring system — where widgets self-report their suitability for a given constraint set — is an elegant pattern for renderer selection:

```python
# DASH-inspired widget scoring
def score_widget(widget_class, field_def) -> int:
    """Widget self-evaluates suitability for this field definition."""
    if field_def.data_type == "date" and widget_class == DatePicker:
        return 90
    if field_def.data_type == "string" and field_def.max_length > 500:
        return 70  # TextArea scores high for long strings
    if field_def.choices and widget_class == SelectDropdown:
        return 80
    return 0  # Not suitable
```

This is interesting but CSFEER's django-cotton components are more explicit — each field type maps to a known component. The scoring pattern would add indirection without clear benefit in a template-driven rendering approach.

---

## What's NOT Adaptable (and Why)

### RDF Data Model (Fundamental Mismatch)

SHACL validates RDF graphs (subject-predicate-object triples). CSFEER's form data is JSON key-value pairs stored in Django models. This is not a superficial difference:

```
SHACL expects:
  ex:Person123  schema:givenName  "John" .
  ex:Person123  schema:email      "john@example.com" .

CSFEER produces:
  {"givenName": "John", "email": "john@example.com"}
```

Using SHACL would require:
1. Converting form submissions to RDF (JSON-LD context or manual mapping)
2. Running pySHACL on the RDF graph
3. Converting validation results back to field-level errors
4. Maintaining RDF/Turtle shape definitions alongside Pydantic schemas

This adds a serialization round-trip and a conceptual layer (RDF, Turtle syntax, ontologies) that the team doesn't need.

### No Calculated Fields (Standard Only)

SHACL-AF's `sh:values` can infer derived values, but:
- Requires defining SHACL Functions in SPARQL or external code
- Standard SHACL has no equivalent to `${personnel} + ${equipment} + ${travel}`
- TopBraid's ADS (Active Data Shapes) adds JavaScript expressions, but that's proprietary

Compare with XForms' `calculate="instance('budget')/personnel + instance('budget')/equipment"` — far simpler for the same use case.

### No Conditional Visibility

SHACL's `sh:condition` controls **when rules execute**, not field visibility. There's no standard mechanism for "show this field only when marital status is 'married'." Form generators must implement this outside SHACL.

Compare with XForms' `relevant="status = 'married'"` or FHIR's `enableWhen` — both provide declarative conditional visibility that SHACL lacks.

### No Multi-Step Navigation

SHACL has no concept of steps, pages, or wizards. `sh:PropertyGroup` provides single-level grouping for accordion-style layouts, but:
- No step ordering or progression
- No conditional step visibility
- No step-level validation (validate each step independently)
- No progress indicators

CSFEER needs Steps > Pages > Sections > FieldGroups > Fields. SHACL offers only the FieldGroups level.

### Immature Form Generation Tooling

The open-source SHACL form ecosystem:

| Project | Language | Stars | Status | Django Integration |
|---------|----------|-------|--------|--------------------|
| [ULB shacl-form](https://github.com/ULB-Darmstadt/shacl-form) | TypeScript web component | ~50 | Most mature OSS | None |
| [CSIRO shacl-form](https://github.com/CSIRO-enviro-informatics/shacl-form) | Python/Jinja2 | ~20 | Archived | Standalone only |
| [Schímatos](https://github.com/schimatos/schimatos.org) | JavaScript | ~15 | Academic prototype | None |
| [zazuko/shacl-forms](https://github.com/zazuko/shacl-forms) | JavaScript | ~7 | Experimental | None |
| [vue-shacl-form](https://github.com/Babibubebon/vue-shacl-form) | Vue.js | ~8 | Limited | None |
| **TopBraid EDG** | Commercial | N/A | Production | None |

No Django integration exists. The only Python option (CSIRO) is archived and generates standalone HTML, not Django template components. Production-quality form generation requires TopBraid EDG (commercial license).

### Steep Learning Curve

SHACL requires understanding:
- RDF data model (triples, graphs, named graphs)
- Turtle serialization syntax
- URI/IRI identifiers for everything
- Open-world assumption (absence ≠ falsity)
- SPARQL for advanced features
- Ontology concepts (classes, properties, domains, ranges)

This is a significant training cost for a team working in Django/Python/JSON.

### No Version Pinning on Responses

Like CommonGrants, SHACL has no built-in versioning mechanism. Shapes are RDF resources identified by IRIs — changing a shape changes it everywhere. Workarounds exist (URI versioning, named graphs, custom metadata) but nothing approaches FHIR's canonical URL + semver + derivedFrom model.

---

## Comparison to Roadmap Layers

| Roadmap Layer | SHACL Has | SHACL Doesn't Have |
|---|---|---|
| **Layer 1: Field Definitions** | Data types (`sh:datatype`), cardinality (`sh:minCount`/`sh:maxCount`), enums (`sh:in`), patterns (`sh:pattern`), default values (`sh:defaultValue`), labels (`sh:name`), help text (`sh:description`), ordering (`sh:order`) | Calculated fields, field metadata (review_title), currency formatting, file attachment types |
| **Layer 2: Validation Rules** | Three severity levels (Violation/Warning/Info), logical composition (`sh:and`/`sh:or`/`sh:not`/`sh:xone`), cross-field comparison (`sh:equals`/`sh:lessThan`/`sh:disjoint`), regex patterns, value ranges, structured validation reports | Sum checks, prior-year comparison, formula-based rules, inline explanatory messages, partial-save-safe validation |
| **Layer 3: Layout** | Single-level property groups (`sh:PropertyGroup`), ordering (`sh:order`), DASH widget hints (`dash:editor`) | Steps, pages, sections, nested groups, conditional inclusion, progress indicators, responsive layout |
| **Layer 4: Renderers** | DASH editor/viewer widgets (14 editors, 10 viewers), automatic widget scoring | Django template renderer, PDF export, API serialization, review page, USWDS components |
| **Cross-cutting: Mapping** | None (RDF has its own mapping via ontology alignment, but not the DSL-style mapping CommonGrants provides) | Cross-form pre-population, prior-year data import, UEI-based data linking |
| **Cross-cutting: Versioning** | None built-in; ad hoc workarounds (URI versioning, named graphs) | Canonical URLs, semver enforcement, derivedFrom, version pinning on responses |

---

## Comparison to Other Analyzed Standards

| Capability | XForms | FHIR R5 | CommonGrants | JSON Forms | SHACL |
|---|---|---|---|---|---|
| **Calculated fields** | `calculate` bind | `calculatedExpression` | None | None | SHACL-AF rules (SPARQL, verbose) |
| **Conditional visibility** | `relevant` bind | `enableWhen`/`enableWhenExpression` | None | `rule` with effect | None standard; custom only |
| **Hard/soft validation** | No (binary) | No (binary) | No (untyped) | No (binary) | **Yes** — three levels |
| **Structured error reports** | No | `OperationOutcome` (separate) | `Array<unknown>` | AJV errors | **Yes** — `ValidationResult` |
| **Multi-step forms** | No (but composable) | Nested items | No | UI schema categories | No |
| **Data mapping DSL** | No | `definition-based extraction` | **Yes** — MappingSchema | No | Ontology alignment (different paradigm) |
| **Widget hints** | UI controls | `itemControl` extension | None | UI schema | **Yes** — DASH editors/viewers |
| **Versioning** | No | **Best** — canonical URL + semver | Basic (`version?: string`) | No | None built-in |
| **Python ecosystem** | None modern | fhir.resources (Pydantic) | SDK (Pydantic) | None (JS-only) | **pySHACL** (production-ready) |
| **Django integration** | None | None | None | None | None |

**SHACL uniquely contributes:** severity levels and structured validation reports. Everything else is either missing or better served by another standard.

---

## Recommendation

### Adopt These Concepts

1. **Three-level severity model** — Borrow `Violation`/`Warning`/`Info` as `error`/`warning`/`info` severity levels for Layer 2 validation rules. This is the highest-value adaptation. No other standard in the survey provides this natively.

2. **Structured validation result pattern** — Model CSFEER's `ValidationMessage` after SHACL's `ValidationResult`: severity, field path, message, constraint type, actual value, source rule. This gives the UI enough information to render errors appropriately and gives admins enough information to debug validation issues.

3. **Constraint composition operators** — Adopt the `and`/`or`/`not`/`xone` vocabulary for expressing complex validation rules. These become operators in the validation DSL, keeping the rule definitions declarative and composable.

4. **Dot-path field references** — Inspired by SHACL property paths, use structured paths like `step2.page1.personnel_costs` for cross-field references in validation rules and calculated expressions.

### Don't Adopt

1. **RDF data model** — Wrong paradigm. CSFEER's data is JSON stored in Django models. RDF adds a serialization layer and conceptual overhead (triples, ontologies, SPARQL) without clear benefit. The team knows Python/JSON/Django, not RDF/Turtle/SPARQL.

2. **SHACL shapes as form definitions** — SHACL shapes lack calculated fields, conditional visibility, multi-step layout, and version management. Layer 1 should remain Pydantic-based with XForms-inspired bind semantics.

3. **DASH widget vocabulary** — Interesting pattern, but CSFEER uses django-cotton components for USWDS markup. The renderer layer is template-driven, not vocabulary-driven. Widget selection is explicit by field type, not scored.

4. **pySHACL as validation engine** — Production-ready for RDF validation, but requires converting JSON form data to RDF, running validation, and converting results back. The serialization round-trip adds latency and complexity. Pydantic validators operating on JSON data directly will be faster and simpler.

5. **SHACL form generator libraries** — No Django integration. The most mature option (ULB shacl-form) is a TypeScript web component. The only Python option (CSIRO) is archived. TopBraid EDG requires a commercial license. None render USWDS components.

6. **SHACL-AF for calculated fields** — Requires defining calculations in SPARQL, which is verbose and unfamiliar. XForms-style `calculate` expressions adapted to Python (as proposed in the roadmap) are far more natural for the team.

---

## Summary

SHACL is a powerful and well-designed constraint language, but it solves a different problem than CSFEER's. Its strengths — semantic interoperability, knowledge graph validation, open-world reasoning — serve government data portals and enterprise knowledge management. Its weaknesses — no calculated fields, no conditional visibility, no multi-step forms, RDF-only data model, immature form tooling — make it a poor fit as a form engine foundation.

However, SHACL's **validation report model is best-in-class**. The three-level severity system and structured `ValidationResult` output are concepts worth adopting wholesale. These fill a gap that no other analyzed standard addresses — the PRD's requirement for distinct hard errors and soft warnings with clear visual differentiation.

**The bottom line:** Borrow SHACL's validation concepts (severity levels, structured error reports, constraint composition). Leave everything else.

---

*Sources: [W3C SHACL 1.0](https://www.w3.org/TR/shacl/), [SHACL Advanced Features](https://w3c.github.io/shacl/shacl-af/), [DASH Data Shapes](https://datashapes.org/dash), [datashapes.org Form Generation](https://datashapes.org/forms.html), [pySHACL](https://github.com/RDFLib/pySHACL), [ULB shacl-form](https://github.com/ULB-Darmstadt/shacl-form), [CSIRO shacl-form](https://github.com/CSIRO-enviro-informatics/shacl-form), [Schímatos (ISWC 2020)](https://link.springer.com/chapter/10.1007/978-3-030-62466-8_5), [SHACL and ShEx in the Wild (WebConf 2022)](https://people.cs.aau.dk/~matteo/pdf/WebConf22-SHACL-Survey.pdf), [TopBraid EDG](https://www.topquadrant.com/doc/latest/introduction/index.html), [Kurt Cagle: SHACL for User Interfaces](https://ontologist.substack.com/p/shacl-for-user-interfaces)*
