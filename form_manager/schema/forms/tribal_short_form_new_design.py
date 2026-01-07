"""The Tribal Short Form definition"""

from django import forms
from pydantic import ConfigDict, Field
from pydantic_extra_types.semantic_version import SemanticVersion

from form_manager.schema.fields import acf_fields
from form_manager.schema.layout import (
    FieldBlock,
    FieldGroupBlock,
    PageBlock,
    SectionBlock,
    StepBlock,
)

from ...constants import AllFormNames, CSBGAnnualReportForms, FormFamilies
from .base import BaseFields, BaseFormSchema, UIDefinition


class TribalShortFormFieldsNew(BaseFields):

    org_name = acf_fields.CharField(title="Name of Tribe or Tribal Organization", max_length=100)
    contact_name = acf_fields.CharField(title="Full name")
    contact_title = acf_fields.CharField(title="Role")
    phone = acf_fields.CharField(
        title="Primary phone number",
        widget=forms.TelInput,  # type: ignore for some reason the typechecker thinks TelInput doesn't exist
    )
    email = acf_fields.CharField(title="Email address", widget=forms.EmailInput)
    employment_expenditure = acf_fields.CharField(title="Employment")
    childcare_expenditure = acf_fields.CurrencyField(
        title="Childcare, Early Childhood, Youth Development, and Adult Education"
    )

    asset_building_expenditure = acf_fields.CurrencyField(title="Income and Asset Building")
    housing_expenditure = acf_fields.CurrencyField(title="Housing")
    health_expenditure = acf_fields.CurrencyField(title="Health and Nutrition")
    civic_expenditure = acf_fields.CurrencyField(title="Civic Engagement and Community Involvement")
    transportation_expenditure = acf_fields.CurrencyField(title="Transportation")

    partnerships_expenditure = acf_fields.CurrencyField(
        title="Partnerships, Linkages, and Coordination"
    )

    other_expenditure = acf_fields.CurrencyField(title="Other")

    administration_expenditure = acf_fields.CurrencyField(title="Administration")

    employment_related_services_description = acf_fields.TextareaField(
        title="Description",
    )

    education_related_service_description = acf_fields.TextareaField(title="Description")

    income_services_description = acf_fields.TextareaField(
        title="Description",
    )

    housing_services_description = acf_fields.TextareaField(
        title="Description",
    )

    health_services_description = acf_fields.TextareaField(title="Description")

    civic_services_description = acf_fields.TextareaField(title="Description")

    transportation_services_description = acf_fields.TextareaField(
        title="Description",
    )

    poverty_coordination_description = acf_fields.TextareaField(
        title="Description",
    )

    total_expenditures = acf_fields.CalculatedCurrencyField(
        fields=[
            "asset_building_expenditure",
            "housing_expenditure",
            "health_expenditure",
            "civic_expenditure",
            "transportation_expenditure",
            "partnerships_expenditure",
            "other_expenditure",
        ]
    )

    total_individuals_served = acf_fields.IntegerField(title="Total number of people")

    total_individuals_served_over_18 = acf_fields.IntegerField(title="Total number of people")


class TribalShortFormNewDesign(BaseFormSchema):

    family: FormFamilies = Field(FormFamilies.CSBG_ANNUAL_REPORT, frozen=True)
    name: AllFormNames = Field(CSBGAnnualReportForms.TRIBAL_ANNUAL_REPORT_3_0_SHORT, frozen=True)
    variant: SemanticVersion = Field(SemanticVersion(3, 0, 4), frozen=True)
    form_fields: TribalShortFormFieldsNew  # type: ignore  add typing.ReadOnly in python > 3.13 to fix this
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
                                title="Tribal Organization",
                                children=[
                                    FieldBlock(field_name="org_name"),
                                ],
                            ),
                            SectionBlock(
                                title="CSBG Program Contact",
                                children=[
                                    FieldBlock(field_name="contact_name"),
                                    FieldBlock(field_name="contact_title"),
                                    FieldBlock(field_name="phone"),
                                    FieldBlock(field_name="email"),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            StepBlock(
                title="Expenditure categories",
                children=[
                    PageBlock(
                        title="Expenditure categories",
                        children=[
                            FieldGroupBlock(
                                description="Provide the amounts for each selected category.",
                                children=[
                                    FieldBlock(field_name="employment_expenditure"),
                                    FieldBlock(field_name="childcare_expenditure"),
                                    FieldBlock(field_name="housing_expenditure"),
                                    FieldBlock(field_name="civic_expenditure"),
                                    FieldBlock(field_name="transportation_expenditure"),
                                    FieldBlock(field_name="partnerships_expenditure"),
                                    FieldBlock(field_name="other_expenditure"),
                                    FieldBlock(field_name="total_expenditures"),
                                ],
                            ),
                        ],
                    ),
                    PageBlock(
                        title="Administration costs",
                        subtitle="To learn more about what qualifies as Administration costs, refer to guidance IM37.",
                        children=[FieldBlock(field_name="administration_expenditure")],
                    ),
                ],
            ),
            StepBlock(
                title="Expenditure details",
                children=[
                    PageBlock(
                        title="Details on employment services",
                        subtitle=(
                            "Describe all employment related services, such as support for job placement, "
                            "vocational and skill training, job development and elminiating barriers to work."
                        ),
                        children=[FieldBlock(field_name="employment_related_services_description")],
                    ),
                    PageBlock(
                        title="Details on education services",
                        subtitle=(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                        ),
                        children=[FieldBlock(field_name="education_related_service_description")],
                    ),
                    PageBlock(
                        title="Details on income services",
                        subtitle=(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                        ),
                        children=[FieldBlock(field_name="income_services_description")],
                    ),
                    PageBlock(
                        title="Details on housing services",
                        subtitle=(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                        ),
                        children=[FieldBlock(field_name="housing_services_description")],
                    ),
                    PageBlock(
                        title="Details on health services",
                        subtitle=(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                        ),
                        children=[FieldBlock(field_name="health_services_description")],
                    ),
                    PageBlock(
                        title="Details on civic services",
                        subtitle=(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                        ),
                        children=[FieldBlock(field_name="civic_services_description")],
                    ),
                    PageBlock(
                        title="Details on transportation services",
                        subtitle=(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                        ),
                        children=[FieldBlock(field_name="transportation_services_description")],
                    ),
                    PageBlock(
                        title="Details on poverty coordination services",
                        subtitle=(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                        ),
                        children=[FieldBlock(field_name="poverty_coordination_description")],
                    ),
                ],
            ),
            StepBlock(
                title="Demographic details",
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
                    )
                ],
            ),
            StepBlock(title="Review and submit"),
        ],
    )

    model_config = ConfigDict(use_enum_values=True)
