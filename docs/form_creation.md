
# Defining a new form

Creating a new form requires three things: a fields class, a schema class, and registration.

## Step 1: Define the fields class

Create a Django form class that inherits from `BaseFields`. Use `acf_fields` to define fields:

```python
# form_manager/schema/forms/my_form.py

from django import forms
from form_manager.schema.fields import acf_fields
from form_manager.schema.forms.base import BaseFields


class MyFormFields(BaseFields):

    # Basic text field
    org_name = acf_fields.CharField(
        title="Organization Name",
        max_length=100,
    )

    # Currency input with $ formatting and comma separators
    total_budget = acf_fields.CurrencyField(
        title="Total Budget",
        min_value=0,
        review_title="Your total budget amount",
    )

    # Conditional field filter — controls which fields appear
    applicable_categories = acf_fields.FieldFilterField(
        is_presentational_only=True,
        choices=[
            ("staff_costs,staff_description", "Staffing"),
            ("travel_costs,travel_description", "Travel"),
        ],
    )

    # These fields are conditionally shown based on the filter above
    staff_costs = acf_fields.CurrencyField(
        title="Staff Costs",
        min_value=0,
        default_if_excluded=0,  # Used when field is excluded during validation
    )

    staff_description = acf_fields.TextareaField(
        title="Describe staffing expenses",
        default_if_excluded="N/A",
    )

    travel_costs = acf_fields.CurrencyField(
        title="Travel Costs",
        min_value=0,
        default_if_excluded=0,
    )

    travel_description = acf_fields.TextareaField(
        title="Describe travel expenses",
        default_if_excluded="N/A",
    )

    # Auto-calculated sum of other fields
    total_costs = acf_fields.CalculatedCurrencyField(
        title="Total Costs",
        fields=["staff_costs", "travel_costs"],
        review_title="Total costs (auto-calculated)",
    )

    # Yes/No question with conditional sub-field
    has_other_funding = acf_fields.YesNoDisplayField(
        title="Do you have other funding sources?",
        fields=[
            acf_fields.CurrencyField(
                title="Other funding amount",
                required=False,
            ),
        ],
    )
```

## Step 2: Define the schema class

```python
from pydantic import ConfigDict, Field
from pydantic_extra_types.semantic_version import SemanticVersion

from form_manager.constants import FormFamilies, CSBGAnnualReportForms
from form_manager.schema.forms.base import BaseFormSchema, UIDefinition
from form_manager.schema.layout import (
    FieldBlock,
    FieldGroupBlock,
    PageBlock,
    PermanentPageBlock,
    SectionBlock,
    StepBlock,
)


class MyForm(BaseFormSchema):

    family: FormFamilies = Field(FormFamilies.CSBG_ANNUAL_REPORT, frozen=True)
    name: AllFormNames = Field(CSBGAnnualReportForms.MY_FORM_NAME, frozen=True)
    variant: SemanticVersion = Field(SemanticVersion(1, 0, 0), frozen=True)
    form_fields: MyFormFields  # type: ignore
    ui: UIDefinition = Field(
        frozen=True,
        default=[
            StepBlock(
                title="Basic Information",
                children=[
                    PermanentPageBlock(
                        title="Organization details",
                        children=[
                            SectionBlock(
                                title="Organization",
                                children=[
                                    FieldBlock(field_name="org_name"),
                                    FieldBlock(field_name="total_budget"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            StepBlock(
                title="Expense Categories",
                children=[
                    PermanentPageBlock(
                        title="Select applicable categories",
                        children=[
                            FieldBlock(field_name="applicable_categories"),
                        ],
                    ),
                    PageBlock(
                        title="Staff expenses",
                        children=[
                            FieldBlock(field_name="staff_costs"),
                            FieldBlock(field_name="staff_description"),
                        ],
                    ),
                    PageBlock(
                        title="Travel expenses",
                        children=[
                            FieldBlock(field_name="travel_costs"),
                            FieldBlock(field_name="travel_description"),
                        ],
                    ),
                ],
            ),
            StepBlock(
                title="Summary",
                children=[
                    PermanentPageBlock(
                        title="Cost summary",
                        children=[
                            FieldGroupBlock(
                                description="Review your totals",
                                children=[
                                    FieldBlock(field_name="total_costs"),
                                    FieldBlock(field_name="has_other_funding"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    model_config = ConfigDict(use_enum_values=True)
```

## Step 3: Register the schema

1. Add the form name to the appropriate enum in `form_manager/constants.py`.

2. Add the import to `form_manager/schema/forms/__init__.py`:
   ```python
   from form_manager.schema.forms.my_form import MyForm

   ALL_FORM_SCHEMAS = [TribalLongForm, TribalShortForm, MyForm]
   ```

3. Run the management command:
   ```bash
   python manage.py load_initial_forms
   ```

This creates a `FormDefinition` record with `schema_class="MyForm"`. At runtime, the views dynamically import and instantiate the schema via `import_form_schema()`.

---
