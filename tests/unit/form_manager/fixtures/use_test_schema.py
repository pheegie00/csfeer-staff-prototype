from unittest.mock import patch

import pytest
from pydantic import ConfigDict, Field
from pydantic_extra_types.semantic_version import SemanticVersion

from form_manager.constants import AllFormNames, CSBGAnnualReportForms, FormFamilies
from form_manager.schema.fields import acf_fields
from form_manager.schema.forms.base import BaseFields, BaseFormSchema, UIDefinition
from form_manager.schema.layout import (
    FieldBlock,
    FieldGroupBlock,
    PageBlock,
    PermanentPageBlock,
    SectionBlock,
    StepBlock,
)


class TestSchemaForm(BaseFields):

    # region Basic Information
    first_name = acf_fields.CharField(title="First Name")
    last_name = acf_fields.CharField(title="Last Name")

    # region Question Filters

    applicable_topics = acf_fields.FieldFilterField(
        is_presentational_only=True,
        choices=[
            (
                "item1_cost",
                "Item 1 Cost",
            ),
            (
                "item2_cost",
                "Item 2 Cost",
            ),
            (
                "item3_cost",
                "Item 3 Cost",
            ),
        ],
    )

    item1_cost = acf_fields.CurrencyField(
        title="Item 1", min_value=0, review_title="The cost you entered for item 1 is:"
    )
    item2_cost = acf_fields.CurrencyField(
        title="Item 2",
        min_value=0,
        review_title="The cost you entered for item 2 is:",
    )

    item3_cost = acf_fields.CurrencyField(
        title="Item 3",
        min_value=0,
        review_title="The cost you entered for item 3 is:",
    )


class TestSchema(BaseFormSchema):

    family: FormFamilies = Field(FormFamilies.CSBG_ANNUAL_REPORT, frozen=True)
    name: AllFormNames = Field(CSBGAnnualReportForms.TRIBAL_ANNUAL_REPORT_3_0, frozen=True)
    variant: SemanticVersion = Field(SemanticVersion(3, 0, 4), frozen=True)
    form_fields: TestSchemaForm  # type: ignore  add typing.ReadOnly in python > 3.13 to fix this
    ui: UIDefinition = Field(
        frozen=True,
        default=[
            StepBlock(
                title="Basic Information",
                children=[
                    PageBlock(
                        title="Your basic information",
                        children=[
                            SectionBlock(
                                title="First Name",
                                children=[
                                    FieldBlock(field_name="first_name"),
                                ],
                            ),
                            SectionBlock(
                                title="Last Name",
                                children=[
                                    FieldBlock(field_name="last_name"),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            StepBlock(
                title="Costs",
                children=[
                    PermanentPageBlock(
                        title="Cost categories",
                        children=[FieldBlock(field_name="applicable_topics")],
                    ),
                    PageBlock(
                        title="Specific costs",
                        children=[
                            FieldGroupBlock(
                                description="Provide the amounts for each selected category.",
                                children=[
                                    FieldBlock(field_name="item1_cost"),
                                    FieldBlock(field_name="item2_cost"),
                                    FieldBlock(field_name="item3_cost"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    model_config = ConfigDict(use_enum_values=True)


@pytest.fixture
def use_test_schema():

    with (
        patch(
            "form_manager.management.commands.load_initial_forms.get_form_definitions"
        ) as get_form_defs,
        patch("form_manager.schema.forms.utils.import_string") as import_form_schema,
    ):
        get_form_defs.return_value = [TestSchema]
        import_form_schema.return_value = TestSchema

        yield TestSchema
