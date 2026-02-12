# Available form fields

All fields are accessed through the `acf_fields` object, which wraps standard Django form fields with the `ACFFieldMixin` and provides custom field types.

## Common parameters (all fields)

These parameters are added by `ACFFieldMixin` and available on every field type:

| Parameter | Type | Description |
|---|---|---|
| `title` | `str` | Short label displayed on the form and review page |
| `review_title` | `str` | Alternative title shown on the review page |
| `description` | `str` | Help text displayed below the field (maps to Django's `help_text`) |
| `is_presentational_only` | `bool` | If `True`, field value is not persisted. Default: `False` |
| `default_if_excluded` | `any` | Default value used when field is excluded by a `FieldFilterField` during validation |

Standard Django field parameters (`required`, `initial`, `widget`, `validators`, `disabled`, `label`, etc.) are also supported.

## Standard Django fields

All standard Django form fields are available with the ACF mixin applied:

```python
acf_fields.CharField(title="Name", max_length=100)
acf_fields.IntegerField(title="Count", min_value=0)
acf_fields.DecimalField(title="Amount", decimal_places=2)
acf_fields.EmailField(title="Email")  # Renamed to use forms.EmailInput widget
acf_fields.BooleanField(title="Agree to terms")
acf_fields.ChoiceField(title="Status", choices=[("a", "Active"), ("i", "Inactive")])
acf_fields.DateField(title="Start date")
# ... all other Django field types
```

## CurrencyField

A decimal field with currency formatting, comma separators, and Alpine.js input masking.

```python
acf_fields.CurrencyField(
    title="Employment Expenses",
    min_value=0,
    review_title="Total employment expenses",
    default_if_excluded=0,
)
```

**Behavior:**
- Renders with `$` prefix via the `<c-currency-input>` web component
- Forces 2 decimal places and locale-aware formatting
- Alpine.js mask: `x-mask:dynamic="$money($input, '.', ',')"` for live formatting
- Review page displays as `$1,234.56`

## CalculatedField

A read-only field whose value is the sum of other specified fields.

```python
acf_fields.CalculatedField(
    title="Total Served",
    fields=["male_served", "female_served", "other_served"],
    review_title="Total people served (auto-calculated)",
)
```

**Behavior:**
- Always `disabled=True` and `required=False`
- Calculates value server-side by summing the listed fields
- Skips fields that are in `fields_to_exclude` (from `FieldFilterField`)
- JavaScript updates the value live on the client via `data-source-fields` attribute
- CSS class: `calculated-field`

## CalculatedCurrencyField

Combines `CalculatedField` logic with `CurrencyField` formatting.

```python
acf_fields.CalculatedCurrencyField(
    title="Total Expenditures",
    fields=["staff_costs", "travel_costs", "other_costs"],
    review_title="Total expenditures (auto-calculated)",
)
```

**Behavior:**
- Same calculation logic as `CalculatedField`
- Renders with currency formatting (`$` prefix, comma separators, 2 decimal places)
- CSS class: `calculated-currency-field`

### TextareaField

A multi-line text input.

```python
acf_fields.TextareaField(
    title="Description of services",
    review_title="Services description",
    default_if_excluded="N/A",
)
```

**Behavior:**
- Renders as `<textarea>` with default `rows=20`, `cols=100`

## FieldFilterField

A checkbox group that controls which subsequent fields are shown or hidden. This is the mechanism for conditional form sections.

```python
acf_fields.FieldFilterField(
    is_presentational_only=True,
    choices=[
        ("field_a,field_b", "Category A"),
        ("field_c", "Category B"),
        ("field_d,field_e", "Category C"),
    ],
)
```

**Choice format:** Each choice value is a comma-separated string of field names that should be **included** when selected.

**Exclusion logic:**
- If user selects "Category A" and "Category B": `field_d` and `field_e` are excluded
- If user selects nothing: all listed fields (`field_a` through `field_e`) are excluded
- Excluded fields are removed from the UI tree, and their `PageBlock` containers are removed if empty

**Important:** Always set `is_presentational_only=True` since the filter field itself doesn't need to be persisted. Fields controlled by the filter should have `default_if_excluded` set so validation passes when they're excluded.

## YesNoDisplayField

A compound field: yes/no radio buttons that conditionally reveal additional fields.

```python
acf_fields.YesNoDisplayField(
    title="Did you use any funds for administration?",
    fields=[
        acf_fields.CurrencyField(
            title="Administration amount",
            required=False,
            initial="",
        ),
    ],
    validators=[],
)
```

**Behavior:**
- Renders tile-style radio buttons (Yes/No) with Alpine.js conditional display
- Sub-fields only appear when "Yes" is selected
- Data is stored as a dash-delimited string: `"yes-1500.00"` or `"no-"`
- Form data uses indexed names: `field_name_0` (radio), `field_name_1` (first sub-field), etc.