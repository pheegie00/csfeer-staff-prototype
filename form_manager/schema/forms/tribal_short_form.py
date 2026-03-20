"""The Tribal Short Form definition"""

from django import forms
from pydantic import ConfigDict, Field
from pydantic_extra_types.semantic_version import SemanticVersion

from form_manager.constants import AllFormNames, CSBGAnnualReportForms, FormFamilies
from form_manager.schema.fields import acf_fields
from form_manager.schema.forms.base import BaseFields, BaseFormSchema, UIDefinition
from form_manager.schema.layout import (
    AlertBoxBlock,
    FieldBlock,
    FieldGroupBlock,
    PageBlock,
    PageTitleBlock,
    PermanentPageBlock,
    ReviewSubheadingBlock,
    SectionBlock,
    StepBlock,
)


class TribalShortFormFields(BaseFields):
    # region Basic Information
    org_name = acf_fields.CharField(title="Name of Tribe or Tribal Organization", max_length=100)
    contact_name = acf_fields.CharField(title="Full name")
    contact_title = acf_fields.CharField(title="Title")
    phone = acf_fields.CharField(
        title="Primary phone number",
        widget=forms.TelInput,  # type: ignore for some reason the typechecker thinks TelInput doesn't exist
    )
    extension = acf_fields.CharField(
        title="Extension (Optional)",
        required=False,
    )
    email = acf_fields.CharField(title="Email address", widget=forms.EmailInput)
    fax = acf_fields.CharField(
        title="Fax number (Optional)",
        widget=forms.TelInput,  # type: ignore for some reason the typechecker thinks TelInput doesn't exist
        required=False,
    )

    # region Question Filters

    applicable_topics = acf_fields.FieldFilterField(
        is_presentational_only=True,
        choices=[
            (
                "employment_expenditure,employment_related_services_description",
                "Employment",
            ),
            (
                "childcare_expenditure,education_related_service_description",
                "Childcare, Early Childhood, Youth Development & Adult Education",
            ),
            (
                "asset_building_expenditure,income_services_description",
                "Income & Asset Building",
            ),
            (
                "housing_expenditure,housing_services_description",
                "Housing",
            ),
            (
                "health_expenditure,health_services_description",
                "Health & Nutrition",
            ),
            (
                "civic_expenditure,civic_services_description",
                "Civic Engagement & Community Involvement",
            ),
            ("transportation_expenditure,transportation_services_description", "Transportation"),
            (
                "partnerships_expenditure",
                "Partnerships, Linkages, and Coordination",
            ),
            ("other_expenditure", "Other"),
        ],
    )

    # region Expenditure Amounts
    employment_expenditure = acf_fields.CurrencyField(
        title="Employment", min_value=0, review_title="Employment expenses", default_if_excluded=0
    )
    childcare_expenditure = acf_fields.CurrencyField(
        title="Childcare, Early Childhood, Youth Development, and Adult Education",
        min_value=0,
        review_title="Childcare, Early Childhood, Youth Development, and Adult Education expenses",
        default_if_excluded=0,
    )

    asset_building_expenditure = acf_fields.CurrencyField(
        title="Income and Asset Building", min_value=0, default_if_excluded=0
    )
    housing_expenditure = acf_fields.CurrencyField(
        title="Housing", min_value=0, default_if_excluded=0
    )
    health_expenditure = acf_fields.CurrencyField(
        title="Health and Nutrition", min_value=0, default_if_excluded=0
    )
    civic_expenditure = acf_fields.CurrencyField(
        title="Civic Engagement and Community Involvement", min_value=0, default_if_excluded=0
    )
    transportation_expenditure = acf_fields.CurrencyField(
        title="Transportation", min_value=0, default_if_excluded=0
    )

    partnerships_expenditure = acf_fields.CurrencyField(
        title="Partnerships, Linkages, and Coordination", min_value=0, default_if_excluded=0
    )

    other_expenditure = acf_fields.CurrencyField(title="Other", min_value=0, default_if_excluded=0)

    total_expenditures = acf_fields.CalculatedCurrencyField(
        title="Total Expenditures",
        fields=[
            "employment_expenditure",
            "childcare_expenditure",
            "asset_building_expenditure",
            "housing_expenditure",
            "health_expenditure",
            "civic_expenditure",
            "transportation_expenditure",
            "partnerships_expenditure",
            "other_expenditure",
        ],
        review_title="Total Expenditures (auto-calculated)",
    )

    administration_expenditure = acf_fields.YesNoDisplayField(
        title="Did you use any funds toward Administration costs?",
        fields=[
            acf_fields.CurrencyField(
                title="Administration",
                review_title="Total administration costs",
                initial="",
                required=False,
            )
        ],
        validators=[],
    )

    # region Expenditure Descriptions

    employment_related_services_description = acf_fields.TextareaField(
        title="Description",
        review_title="Details about employment related services",
        default_if_excluded="N/A",
    )

    education_related_service_description = acf_fields.TextareaField(
        title="Description",
        review_title="Details about education related services",
        default_if_excluded="N/A",
    )

    income_services_description = acf_fields.TextareaField(
        title="Description",
        review_title="Details about income and asset services",
        default_if_excluded="N/A",
    )

    housing_services_description = acf_fields.TextareaField(
        title="Description",
        review_title="Details about housing services",
        default_if_excluded="N/A",
    )

    health_services_description = acf_fields.TextareaField(
        title="Description",
        review_title="Details about health services",
        default_if_excluded="N/A",
    )

    civic_services_description = acf_fields.TextareaField(
        title="Description",
        review_title="Details about civic services",
        default_if_excluded="N/A",
    )

    transportation_services_description = acf_fields.TextareaField(
        title="Description",
        review_title="Details about transportation services",
        default_if_excluded="N/A",
    )


class TribalShortForm(BaseFormSchema):
    family: FormFamilies = Field(FormFamilies.CSBG_ANNUAL_REPORT, frozen=True)
    name: AllFormNames = Field(CSBGAnnualReportForms.TRIBAL_ANNUAL_REPORT_3_0_SHORT, frozen=True)
    variant: SemanticVersion = Field(SemanticVersion(3, 0, 0), frozen=True)
    form_fields: TribalShortFormFields  # type: ignore  add typing.ReadOnly in python > 3.13 to fix this
    ui: UIDefinition = Field(
        frozen=True,
        default=[
            StepBlock(
                title="Basic Information",
                children=[
                    PermanentPageBlock(
                        title="Your basic information",
                        children=[
                            SectionBlock(
                                title="Tribal Organization",
                                children=[
                                    ReviewSubheadingBlock(title="Tribal Organization"),
                                    FieldBlock(field_name="org_name"),
                                ],
                            ),
                            SectionBlock(
                                title="CSBG Program Contact",
                                children=[
                                    ReviewSubheadingBlock(title="CSBG Program Contact"),
                                    FieldBlock(field_name="contact_name"),
                                    FieldBlock(field_name="contact_title"),
                                    FieldBlock(field_name="phone"),
                                    FieldBlock(field_name="extension"),
                                    FieldBlock(field_name="email"),
                                    FieldBlock(field_name="fax"),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            StepBlock(
                title="Expenditure categories",
                children=[
                    PermanentPageBlock(
                        children=[
                            AlertBoxBlock(
                                alert_type="info",
                                heading="How to select expenditure categories",
                                message="When you select a category, related questions will appear in the following pages. Be sure to save to ensure that all changes are preserved.",
                            ),
                            PageTitleBlock(title="Expenditure categories"),
                            FieldBlock(field_name="applicable_topics"),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Expenditure categories",
                        children=[
                            FieldGroupBlock(
                                description="Provide the amounts for each selected category.",
                                children=[
                                    FieldBlock(field_name="employment_expenditure"),
                                    FieldBlock(field_name="childcare_expenditure"),
                                    FieldBlock(field_name="asset_building_expenditure"),
                                    FieldBlock(field_name="housing_expenditure"),
                                    FieldBlock(field_name="health_expenditure"),
                                    FieldBlock(field_name="civic_expenditure"),
                                    FieldBlock(field_name="transportation_expenditure"),
                                    FieldBlock(field_name="partnerships_expenditure"),
                                    FieldBlock(field_name="other_expenditure"),
                                    FieldBlock(field_name="total_expenditures"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Administration costs",
                        subtitle=(
                            "To learn more about what qualifies as Administration costs, refer "
                            "to guidance IM37."
                        ),
                        children=[
                            FieldBlock(
                                field_name="administration_expenditure",
                                review_template_name="form_manager/forms/yes_no_display_review.html",
                            )
                        ],
                    ),
                ],
            ),
            StepBlock(
                title="Expenditure details",
                children=[
                    PageBlock(
                        title="Details on employment services",
                        subtitle=(
                            "Describe all employment related services, such as support for job "
                            "placement, vocational and skill training, job development and "
                            "elminiating barriers to work."
                        ),
                        children=[FieldBlock(field_name="employment_related_services_description")],
                    ),
                    PageBlock(
                        title="Details on education services",
                        subtitle=(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
                            "eiusmod tempor incididunt ut labore et dolore magna aliqua."
                        ),
                        children=[FieldBlock(field_name="education_related_service_description")],
                    ),
                    PageBlock(
                        title="Details on income services",
                        subtitle=(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
                            "eiusmod tempor incididunt ut labore et dolore magna aliqua."
                        ),
                        children=[FieldBlock(field_name="income_services_description")],
                    ),
                    PageBlock(
                        title="Details on housing services",
                        subtitle=(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
                            "eiusmod tempor incididunt ut labore et dolore magna aliqua."
                        ),
                        children=[FieldBlock(field_name="housing_services_description")],
                    ),
                    PageBlock(
                        title="Details on health services",
                        subtitle=(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
                            "eiusmod tempor incididunt ut labore et dolore magna aliqua."
                        ),
                        children=[FieldBlock(field_name="health_services_description")],
                    ),
                    PageBlock(
                        title="Details on civic services",
                        subtitle=(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
                            "eiusmod tempor incididunt ut labore et dolore magna aliqua."
                        ),
                        children=[FieldBlock(field_name="civic_services_description")],
                    ),
                    PageBlock(
                        title="Details on transportation services",
                        subtitle=(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
                            "eiusmod tempor incididunt ut labore et dolore magna aliqua."
                        ),
                        children=[FieldBlock(field_name="transportation_services_description")],
                    ),
                ],
            ),
        ],
    )

    model_config = ConfigDict(use_enum_values=True)
