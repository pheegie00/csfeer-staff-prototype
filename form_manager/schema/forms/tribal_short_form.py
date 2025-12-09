"""The Tribal Short Form definition"""

from typing import Annotated, Optional

from pydantic import ConfigDict, Field
from pydantic_extra_types.semantic_version import SemanticVersion

from form_manager.schema.layout import FieldBlock, SectionBlock

from ...constants import AllFormNames, CSBGAnnualReportForms, FormFamilies
from ..fields import (
    CalculatedCurrencyField,
    CurrencyField,
    EmailField,
    PhoneNumberField,
    TextareaField,
    TextField,
)
from .base import BaseFormFields, BaseFormSchema


class TribalShortFormFields(BaseFormFields):

    org_name: Annotated[
        TextField, Field(title="A.1a.", description="Name of Tribe or Tribal Organization")
    ]
    contact_name: Annotated[TextField, Field(title="Name")]
    contact_title: Annotated[TextField, Field(title="Title")]
    phone: Annotated[
        PhoneNumberField,
        Field(title="A.1c", description="Work Telephone number and extension (if applicable)"),
    ]
    email: Annotated[EmailField, Field(title="A.1d", description="Email address")]
    employment_expenditure: Annotated[CurrencyField, Field(title="A.2a.", description="Employment")]
    childcare_expenditure: Annotated[
        CurrencyField,
        Field(
            title="A.2b",
            description="Childcare, Early Childhood, Youth Development, and Adult Education",
        ),
    ]
    asset_building_expenditure: Annotated[
        CurrencyField, Field(title="A.2c.", description="Income and Asset Building")
    ]
    housing_expenditure: Annotated[CurrencyField, Field(title="A.2d", description="Housing")]
    health_expenditure: Annotated[
        CurrencyField, Field(title="A.2e", description="Health and Nutrition")
    ]
    civic_expenditure: Annotated[
        CurrencyField,
        Field(title="A.2f.", description="Civic Engagement and Community Involvement"),
    ]
    transportation_expenditure: Annotated[
        CurrencyField, Field(title="A.2g.", description="Transportation")
    ]
    partnerships_expenditure: Annotated[
        CurrencyField, Field(title="A.2h", description="Partnerships, Linkages, and Coordination")
    ]
    other_expenditure: Annotated[CurrencyField, Field(title="A.2i.", description="Other")]
    administration_expenditure: Annotated[
        CurrencyField,
        Field(title="A.3.", description="Report the total amount used for Administration."),
    ]

    employment_related_services_description: Annotated[
        TextareaField,
        Field(
            title="SRV 1",
            description=(
                "Describe all employment related services, such as support for job "
                "placement, vocational and skills training, job development, and "
                "eliminating barriers to work. (If you did not provide this service, "
                "indicate “N/A” for not applicable.)"
            ),
        ),
    ]

    education_related_service_description: Annotated[
        TextareaField,
        Field(
            title="SRV 2",
            description=(
                "Describe all education related services, such as adult education, "
                "literacy programs, scholarships, Head Start enhancement, child development "
                "programs, and anti-drug education. Additionally, describe all youth "
                "development related activities, such as activities that address the needs "
                "of youth in communities with low income to include establishment of "
                "violence-free zones, intervention, and mediation programs, mentoring and "
                "life skills training, job creation, entrepreneurship programs, and after-school "
                "childcare programs. (If you did not provide this service, indicate “N/A” for not applicable.)"
            ),
        ),
    ]

    income_services_description: Annotated[
        TextareaField,
        Field(
            title="SRV 3",
            description=(
                "Describe all income management and asset building related services, such "
                "as budgeting assistance, tax preparation, tax credit education, medical "
                "benefits, claims assistance, and savings programs. (If you did not "
                "provide this service, indicate “N/A” for not applicable.)"
            ),
        ),
    ]

    housing_services_description: Annotated[
        TextareaField,
        Field(
            title="SRV 4",
            description=(
                "Describe all housing related services, such as homeownership "
                "counseling and loan assistance, landlord-tenant relations, "
                "housing assistance, homeless services, and home repair "
                "and rehabilitation. (If you did not provide this service, "
                'indicate "N/A" for not applicable.)'
            ),
        ),
    ]

    health_services_description: Annotated[
        TextareaField,
        Field(
            title="SRV 5",
            description=(
                "Describe all health and nutrition related services, such as "
                "food banks, public education, health counseling, transportation "
                "to health services, community garden programs, and production "
                "and delivery programs. (If you did not provide this service, "
                'indicate "N/A" for not applicable.)'
            ),
        ),
    ]

    civic_services_description: Annotated[
        TextareaField,
        Field(
            title="SRV 6",
            description=(
                "Describe all partnerships and community engagement related services, "
                "such as activities designed to help families and individuals with low "
                "incomes achieve greater participation in the aﬀairs of their communities, "
                "including partnerships with local law enforcement agencies, housing authorities, "
                "private foundations, and other public and private partners. "
                "CSBG funding also supports interagency partnerships and Tribal-State "
                'partnerships as well. (If you did not provide this service, indicate "N/A" for not applicable.)'
            ),
        ),
    ]

    transportation_services_description: Annotated[
        TextareaField,
        Field(
            title="SRV 7",
            description=(
                "Describe all transportation related activities such as "
                "transportation vouchers, public transit fare assistance, "
                "medical transportation services, community shuttle services, "
                "rideshare programs, volunteer driver programs, and child "
                "and youth transportation. (If you did not provide this service, indicate `N/A` for not applicable.)"
            ),
        ),
    ]

    poverty_coordination_description: Annotated[
        TextareaField,
        Field(
            title="SRV 8",
            description=(
                "Describe all linkages and coordination between anti-poverty programs, "
                "such as eligibility coordination to make more eﬀective use of related programs, "
                "including other public and private sources. Fill identified gaps in the services "
                "through the provision of information, referrals, eligibility coordination, "
                "case management, and follow-up consultations."
            ),
        ),
    ]

    total_expenditures: Annotated[
        CalculatedCurrencyField,
        Field(
            default=0,
            json_schema_extra={
                "fields": [
                    "asset_building_expenditure",
                    "housing_expenditure",
                    "health_expenditure",
                    "civic_expenditure",
                    "transportation_expenditure",
                    "partnerships_expenditure",
                    "other_expenditure",
                ]
            },
        ),
    ]


type UIDefinition = list[SectionBlock | FieldBlock]


class TribalShortForm(BaseFormSchema):

    family: FormFamilies = Field(FormFamilies.CSBG_ANNUAL_REPORT, frozen=True)
    name: AllFormNames = Field(CSBGAnnualReportForms.TRIBAL_ANNUAL_REPORT_3_0_SHORT, frozen=True)
    variant: SemanticVersion = Field(SemanticVersion(3, 0, 3), frozen=True)
    form_fields: TribalShortFormFields
    ui: UIDefinition = Field(
        frozen=True,
        default=[
            SectionBlock(
                title="A.1",
                description=(
                    "Provide the following information in relation to the tribe or "
                    "tribal organization designated to administer CSBG as required in "
                    "Sections 676 and 677 of the CSBG Act, the Human Services Reauthorization "
                    "Act of 1998 (P.L.105-285), and relevant federal policy guidance. "
                    "The following information should mirror the information provided on the "
                    "Application for Federal Assistance, SF-424M."
                ),
                children=[
                    FieldBlock(field_name="org_name"),
                    FieldBlock(field_name="contact_name"),
                    FieldBlock(field_name="contact_title"),
                    FieldBlock(field_name="phone"),
                    FieldBlock(field_name="email"),
                ],
            ),
            SectionBlock(
                title="Section A: Tribal CSBG Expenditures",
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
                    FieldBlock(field_name="administration_expenditure"),
                    FieldBlock(field_name="employment_related_services_description"),
                    FieldBlock(field_name="education_related_service_description"),
                    FieldBlock(field_name="income_services_description"),
                    FieldBlock(field_name="housing_services_description"),
                    FieldBlock(field_name="health_services_description"),
                    FieldBlock(field_name="civic_services_description"),
                    FieldBlock(field_name="health_services_description"),
                    FieldBlock(field_name="transportation_services_description"),
                    FieldBlock(field_name="poverty_coordination_description"),
                ],
            ),
        ],
    )

    model_config = ConfigDict(use_enum_values=True)
