# UI component definitions

The UI is defined as a tree of layout blocks. Each block type maps to a Django template and serves a specific role in the form structure.

## Block hierarchy

```
StepBlock                    → Step in the progress indicator
└── PageBlock                → A single page the user sees (removable by filters)
└── PermanentPageBlock       → A page that's never removed by filters
    └── SectionBlock         → Visual grouping with a heading
    └── FieldGroupBlock      → Bordered group with a description
        └── FieldBlock       → Renders a specific form field (leaf node)
        └── ReviewSubheadingBlock → Heading shown only on the review page (leaf node)
```

## StepBlock

Represents a step in the USWDS step indicator. Top-level container in the UI definition.

```python
StepBlock(
    title="Basic Information",
    children=[
        PageBlock(...),
        PageBlock(...),
    ],
)
```

| Attribute | Type | Description |
|---|---|---|
| `title` | `str` | Step name shown in the step indicator |
| `children` | `list` | `PageBlock`, `PermanentPageBlock`, or `SectionBlock` children |

## PageBlock

Represents a single page within a step. Users see one page at a time and navigate with Back/Continue buttons.

```python
PageBlock(
    title="Expense Details",
    subtitle="Enter the amounts for each category.",
    children=[
        FieldBlock(field_name="staff_costs"),
        FieldBlock(field_name="travel_costs"),
    ],
)
```

| Attribute | Type | Description |
|---|---|---|
| `title` | `str` | Page heading (`<h1>`) |
| `subtitle` | `str` | Subheading text below the title |
| `children` | `list` | `FieldBlock`, `SectionBlock`, `FieldGroupBlock`, or nested `PageBlock` |
| `template_name` | `str` | Default: `form_manager/page.html` |

**Key behavior:** When all `FieldBlock` descendants of a `PageBlock` are excluded by a `FieldFilterField`, the entire page is removed from navigation. This is how conditional pages work.

## PermanentPageBlock

Identical to `PageBlock` but **never removed** by the field filtering mechanism, even if all its field blocks are excluded.

```python
PermanentPageBlock(
    title="Select applicable categories",
    children=[
        FieldBlock(field_name="applicable_categories"),
    ],
)
```

Use this for pages that must always appear, such as those containing the `FieldFilterField` itself.

## SectionBlock

A semantic grouping of content within a page. Renders with a heading.

```python
SectionBlock(
    title="Contact Information",
    description="Provide your primary contact details.",
    children=[
        FieldBlock(field_name="contact_name"),
        FieldBlock(field_name="contact_email"),
    ],
)
```

| Attribute | Type | Description |
|---|---|---|
| `title` | `str` | Section heading (`<h2>`) |
| `description` | `str` | Descriptive text |
| `children` | `list` | `FieldBlock`, `FieldGroupBlock`, `ReviewSubheadingBlock`, or nested `SectionBlock` |
| `template_name` | `str` | Default: `form_manager/section.html` |

## FieldGroupBlock

A bordered container for related fields with an optional description. Renders inside a `usa-card__container`.

```python
FieldGroupBlock(
    description="Enter the amounts for each expenditure category.",
    children=[
        FieldBlock(field_name="staff_costs"),
        FieldBlock(field_name="travel_costs"),
        FieldBlock(field_name="total_costs"),
    ],
)
```

| Attribute | Type | Description |
|---|---|---|
| `description` | `str` | Explanatory text above the field group |
| `children` | `list` | `FieldBlock`, `ReviewSubheadingBlock`, or nested `FieldGroupBlock` |
| `template_name` | `str` | Default: `form_manager/field_group.html` |

## FieldBlock

The leaf node that renders a specific form field. References a field by name from the fields class.

```python
FieldBlock(field_name="org_name")
```

| Attribute | Type | Description |
|---|---|---|
| `field_name` | `str` | Name of the field in the `BaseFields` subclass |
| `template_name` | `str` | Default: `form_manager/forms/field.html` |
| `review_template_name` | `str` | Default: `form_manager/forms/field_review.html` |

**Review template auto-discovery:** On the review page, `FieldBlock` automatically searches for a field-type-specific review template. For example, `ACFCurrencyField` maps to `currency_review.html`. If no match is found, the default `field_review.html` is used.

**Computed properties** (available in templates via `component`):
- `component.field` — the Django `BoundField` instance
- `component.value` — current field value
- `component.errors` — validation errors
- `component.title` — field title
- `component.display_title` — `review_title` if set, otherwise `title`

## ReviewSubheadingBlock

A heading that only renders on the review page. Useful for adding structure to the review accordion without affecting the form editing UI.

```python
ReviewSubheadingBlock(title="Tribal Organization")
```

| Attribute | Type | Description |
|---|---|---|
| `title` | `str` | Heading text (`<h4>`) |
| `description` | `str` | Optional description |
| `template_name` | `str` | Default: `form_manager/review_subheading.html` |

## How navigation works

The step/page structure drives automatic navigation:

1. The step indicator shows all `StepBlock` titles plus a "Review and Submit" step
2. Within each step, pages are displayed one at a time
3. "Save & Continue" advances to the next page, or next step's first page, or the review page
4. "Back" goes to the previous page, or previous step's last page
5. After field filtering removes pages, navigation indices are recalculated against the filtered tree

## How field exclusion works

1. User makes selections in a `FieldFilterField` (checkbox group)
2. `BaseFields.fields_to_exclude` aggregates excluded field names from all filter fields
3. `remove_nodes_with_excluded_fields()` walks the UI tree:
   - Removes `FieldBlock` nodes whose `field_name` is in the exclusion list
   - Removes `PageBlock` nodes that have no remaining `FieldBlock` descendants
   - `PermanentPageBlock` nodes are never removed
4. Navigation is recalculated against the filtered tree
5. During validation with `use_default_if_excluded=True`, excluded fields use their `default_if_excluded` value

## Context injection

The `set_extra_context()` method recursively injects runtime variables into the component tree. Views call this to provide:

- `form` — the bound Django form instance (used by `FieldBlock` to look up `BoundField`)
- `prev_url` — URL for the Back button
- `is_last_page` — changes "Save & Continue" to "Save & Begin Final Review"
- `current_step_number` / `current_page_number` — for step indicator state

These variables are available in all descendant block templates.