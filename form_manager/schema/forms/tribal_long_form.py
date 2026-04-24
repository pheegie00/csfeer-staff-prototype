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


class TribalLongFormFields(BaseFields):
    # region Basic Information
    org_name = acf_fields.CharField(title="Name of Tribe or Tribal Organization", max_length=100)
    contact_name = acf_fields.CharField(title="Full name")
    contact_title = acf_fields.CharField(title="Role")
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
                required=False,
            )
        ],
    )

    # region Expenditure Descriptions

    employment_related_services_description = acf_fields.TextareaField(
        title="Description",
        review_title="Details about employment related services",
        max_length=1000,
        default_if_excluded="N/A",
    )

    education_related_service_description = acf_fields.TextareaField(
        title="Description",
        review_title="Details about education related services",
        max_length=1000,
        default_if_excluded="N/A",
    )

    income_services_description = acf_fields.TextareaField(
        title="Description",
        review_title="Details about income and asset services",
        max_length=1000,
        default_if_excluded="N/A",
    )

    housing_services_description = acf_fields.TextareaField(
        title="Description",
        review_title="Details about housing services",
        max_length=1000,
        default_if_excluded="N/A",
    )

    health_services_description = acf_fields.TextareaField(
        title="Description",
        review_title="Details about health services",
        max_length=1000,
        default_if_excluded="N/A",
    )

    civic_services_description = acf_fields.TextareaField(
        title="Description",
        review_title="Details about civic services",
        max_length=1000,
        default_if_excluded="N/A",
    )

    transportation_services_description = acf_fields.TextareaField(
        title="Description",
        review_title="Details about transportation services",
        max_length=1000,
        default_if_excluded="N/A",
    )

    # region Demographic Questions

    total_individuals_served = acf_fields.IntegerField(
        title="Total number of people", review_title="Total number of people served"
    )

    total_individuals_served_over_18 = acf_fields.IntegerField(
        title="Total number of people", review_title="Total served under 18"
    )

    male_individuals_served = acf_fields.IntegerField(title="Male")
    female_individuals_served = acf_fields.IntegerField(title="Female")
    total_individuals_served_by_sex = acf_fields.CalculatedIntegerField(
        title="Total",
        fields=["male_individuals_served", "female_individuals_served"],
        review_title="Total (auto-calculated)",
    )

    employment__full_time = acf_fields.IntegerField(title="Employed Full Time")
    employment__part_time = acf_fields.IntegerField(title="Employed Part Time")
    employment__migrant_seasonal = acf_fields.IntegerField(title="Migrant or seasonal farm worker")
    employment__unemployed_short_term = acf_fields.IntegerField(
        title="Unemployed (short term, 6 months or less)"
    )
    employment__unemployed_long_term = acf_fields.IntegerField(
        title="Unemployed (long term, more than 6 months)"
    )
    employment__permanently_unemployed = acf_fields.IntegerField(
        title="Unemployed (not in labor force)"
    )
    employment__retired = acf_fields.IntegerField(title="Retired")
    employment__unknown = acf_fields.IntegerField(title="Unknown or not reported")
    employment__total = acf_fields.CalculatedIntegerField(
        title="Total (auto-calculated)",
        fields=[
            "employment__full_time",
            "employment__part_time",
            "employment__migrant_seasonal",
            "employment__unemployed_short_term",
            "employment__unemployed_long_term",
            "employment__permanently_unemployed",
            "employment__retired",
            "employment__unknown",
        ],
        review_title="Total (auto-calculated)",
    )


class TribalLongForm(BaseFormSchema):
    family: FormFamilies = Field(FormFamilies.CSBG_ANNUAL_REPORT, frozen=True)
    name: AllFormNames = Field(CSBGAnnualReportForms.TRIBAL_ANNUAL_REPORT_3_0, frozen=True)
    variant: SemanticVersion = Field(SemanticVersion(3, 0, 4), frozen=True)
    form_fields: TribalLongFormFields  # type: ignore  add typing.ReadOnly in python > 3.13 to fix this
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
                                message=(
                                    "When you select a category, related questions will appear in "
                                    "following pages. Be sure to save to ensure that all changes "
                                    "are preserved."
                                ),
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
                disabled_reason=(
                    "Select applicable topics in Section 2 before completing this section."
                ),
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
            StepBlock(
                title="Demographic information",
                children=[
                    PageBlock(
                        title="Let's collect demographic details",
                        children=[
                            SectionBlock(
                                title="How many individuals did you serve in total?",
                                children=[FieldBlock(field_name="total_individuals_served")],
                            ),
                            SectionBlock(
                                title="How many individuals did you serve that are over 18?",
                                children=[
                                    FieldBlock(field_name="total_individuals_served_over_18")
                                ],
                            ),
                        ],
                    ),
                    PageBlock(
                        title="About the individuals served",
                        children=[
                            SectionBlock(
                                title="Sex of individuals served (Age 18 and older)",
                                children=[
                                    FieldGroupBlock(
                                        children=[
                                            ReviewSubheadingBlock(
                                                title="Sex of individuals served (Age 18 and older)"
                                            ),
                                            FieldBlock(field_name="male_individuals_served"),
                                            FieldBlock(field_name="female_individuals_served"),
                                            FieldBlock(
                                                field_name="total_individuals_served_by_sex"
                                            ),
                                        ]
                                    )
                                ],
                            ),
                        ],
                    ),
                    PageBlock(
                        title="About the individuals served",
                        children=[
                            SectionBlock(
                                title="Work status of adults served (age 18 and older)",
                                children=[
                                    FieldGroupBlock(
                                        children=[
                                            ReviewSubheadingBlock(
                                                title=(
                                                    "Work status of adults served (age 18 and older)"  # noqa: E501
                                                )
                                            ),
                                            FieldBlock(field_name="employment__full_time"),
                                            FieldBlock(field_name="employment__part_time"),
                                            FieldBlock(field_name="employment__migrant_seasonal"),
                                            FieldBlock(
                                                field_name="employment__unemployed_short_term"
                                            ),
                                            FieldBlock(
                                                field_name="employment__unemployed_long_term"
                                            ),
                                            FieldBlock(field_name="employment__retired"),
                                            FieldBlock(
                                                field_name="employment__permanently_unemployed"
                                            ),
                                            FieldBlock(field_name="employment__unknown"),
                                            FieldBlock(field_name="employment__total"),
                                        ]
                                    )
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    model_config = ConfigDict(use_enum_values=True)
