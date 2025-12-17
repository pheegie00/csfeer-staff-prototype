from enum import Enum
from typing import Annotated, Any, Optional
from unittest.mock import Base

from pydantic import Field
from pydantic_extra_types.semantic_version import SemanticVersion

from form_manager.constants import (
    AllFormNames,
    CSBGTribalPlanApplicationForms,
    FormFamilies,
)
from form_manager.schema.layout import FieldBlock, SectionBlock

from ..fields import ChoiceField, TextareaField, TextField
from .base import BaseFormFields, BaseFormSchema


class PlanCoverageChoices(str, ChoiceField):
    one = "One Year"
    two = "Two-Year"


class TribalPlanApplicationFields(BaseFormFields):

    plan_coverage: Annotated[
        PlanCoverageChoices,
        Field(
            title="1.1 Plan coverage",
            description=(
                "dentify whether this is a one-year or two-year plan. "
                "(Note: CSBG Tribal Plans covering a two-year period are strongly "
                "recommended to minimize administrative burden for grant recipients)"
            ),
        ),
    ]

    plan_coverage_year_one: Annotated[TextField, Field(title="Year One")]
    plan_coverage_year_two: Annotated[TextField, Field(title="Year Two")]

    recipient_name: Annotated[
        TextField,
        Field(
            title="1.2 Tribal Grant Recipient Name",
            description=(
                "Update the following information for the Tribal Lead Agency. "
                "The information entered should reflect theresponses in the "
                "Application for Federal Assistance, SF-424M."
            ),
        ),
    ]

    tribe_or_organization_name: Annotated[
        TextField,
        Field(
            title="1.2.a. Name of Tribe or Tribal Organization",
        ),
    ]

    other_organizations: Optional[
        Annotated[
            TextareaField,
            Field(
                title=(
                    "1.2.b. If a Tribe or Tribal Organization is representing more "
                    "than one Tribe, Village, Community, or Jurisdiction, please list "
                    "the names of all Tribes, Villages, Communities, and Jurisdictions."
                )
            ),
        ]
    ]

    tribal_official_name: Annotated[
        TextField,
        Field(
            title="1.3.a. Authorized Tribal Official Name",
        ),
    ]

    tribal_official_title: Annotated[
        TextField,
        Field(
            title="1.3.b. Authorized Tribal Official Title",
        ),
    ]

    tribal_official_street_address: Annotated[
        TextField,
        Field(
            title="1.3.c. Street Address",
        ),
    ]

    tribal_official_city: Annotated[
        TextField,
        Field(
            title="1.3.a. Authorized Tribal Official Name",
        ),
    ]

    tribal_official_state: Annotated[
        TextField,
        Field(
            title="1.3.d. City",
        ),
    ]

    tribal_official_zip: Annotated[
        TextField,
        Field(
            title="1.3.f. Zip Code",
        ),
    ]


class TribalPlanApplication(BaseFormSchema):
    family: FormFamilies = Field(FormFamilies.CSBG_TRIBAL_PLAN_APPLICATION, frozen=True)
    name: AllFormNames = Field(CSBGTribalPlanApplicationForms.CSBG_TRIBAL_PLAN, frozen=True)
    variant: Annotated[
        SemanticVersion, Field(description="The version of the form", default="1.0.0", frozen=True)
    ]
    form_fields: TribalPlanApplicationFields = Field(
        description="Form field definitions. This should be a class that inherits BaseFormFields."
    )
    ui: list[SectionBlock | FieldBlock] = Field(
        description="The Form UI definition",
        default=[
            SectionBlock(
                title="1.1 Plan coverage",
                children=[
                    FieldBlock(field_name="plan_coverage"),
                    FieldBlock(field_name="plan_coverage_year_one"),
                    FieldBlock(field_name="plan_coverage_year_two"),
                ],
            ),
            SectionBlock(
                title="1.2 Tribal Grant Recipient Name",
                children=[
                    FieldBlock(field_name="recipient_name"),
                    FieldBlock(field_name="tribe_or_organization_name"),
                ],
            ),
            SectionBlock(
                title="1.3 Authorized Tribal Official",
                children=[
                    FieldBlock(field_name="tribal_official_city"),
                    FieldBlock(field_name="tribal_official_street_address"),
                    FieldBlock(field_name="tribal_official_state"),
                    FieldBlock(field_name="tribal_official_zip"),
                ],
            ),
        ],
    )
