"""The CSBG Tribal Plan and Application form definition."""

from datetime import date
from decimal import Decimal

from django import forms
from pydantic import ConfigDict, Field
from pydantic_extra_types.semantic_version import SemanticVersion

from form_manager.constants import AllFormNames, CSBGTribalPlanApplicationForms, FormFamilies
from form_manager.schema.choices import US_STATES
from form_manager.schema.fields import acf_fields
from form_manager.schema.forms.base import BaseFields, BaseFormSchema, UIDefinition
from .texts import (
    _ASSURANCES_NARRATIVE_TOPICS,
    _CSBG_ASSURANCES_NARRATIVE,
    _DEBARMENT_CERTIFICATION_TEXT,
    _DEBARMENT_LOWER_TIER_INSTRUCTIONS_TEXT,
    _DEBARMENT_PRIMARY_INSTRUCTIONS_TEXT,
    _DRUG_FREE_WORKPLACE_CERTIFICATION_TEXT,
    _LOBBYING_CERTIFICATION_TEXT,
    _TOBACCO_SMOKE_CERTIFICATION_TEXT,
)
from form_manager.schema.layout import (
    AccordionBlock,
    AccordionItem,
    AlertBoxBlock,
    FieldBlock,
    FieldGroupBlock,
    PermanentPageBlock,
    ReviewSubheadingBlock,
    SectionBlock,
    StepBlock,
    TextBlock,
)


def _fiscal_year_choices() -> list[tuple[str, str]]:
    """Return the upcoming 3 fiscal year choices from the current date.

    The fiscal year runs October 1 – September 30. This list is computed once at
    module load time. Kayla confirmed "next 2 fiscal years continuously" is the
    desired range; 3 are included here as a small buffer.
    """
    today = date.today()
    # Before October: the current calendar year is the ending year of the current FY.
    start_fy = today.year + 1 if today.month >= 10 else today.year
    choices: list[tuple[str, str]] = [("", "Select a fiscal year")]
    for i in range(3):
        fy = start_fy + i
        choices.append((f"fy_{fy}", f"FY {fy} (October 1, {fy - 1} – September 30, {fy})"))
    return choices


_FISCAL_YEAR_CHOICES = _fiscal_year_choices()

_Y1_ALLOCATION_FIELDS = [
    "alloc_admin_y1",
    "alloc_employment_y1",
    "alloc_education_y1",
    "alloc_income_y1",
    "alloc_housing_y1",
    "alloc_health_y1",
    "alloc_civic_y1",
    "alloc_transportation_y1",
    "alloc_partnerships_y1",
]

_Y2_ALLOCATION_FIELDS = [
    "alloc_admin_y2",
    "alloc_employment_y2",
    "alloc_education_y2",
    "alloc_income_y2",
    "alloc_housing_y2",
    "alloc_health_y2",
    "alloc_civic_y2",
    "alloc_transportation_y2",
    "alloc_partnerships_y2",
]


class TribalPlanFormFields(BaseFields):

    # region Section 1 — CSBG Tribal Administrative Information

    # 1.1 Plan Coverage
    plan_coverage = acf_fields.ChoiceField(
        title="Plan Coverage",
        choices=[("one_year", "One year"), ("two_year", "Two year")],
        widget=forms.RadioSelect(attrs={"radio_type": "tile"}),
    )

    # 1.1a Fiscal Years
    fiscal_year_y1 = acf_fields.ChoiceField(
        title="Fiscal Year (Year One)",
        choices=_FISCAL_YEAR_CHOICES,
    )
    fiscal_year_y2 = acf_fields.ChoiceField(
        title="Fiscal Year (Year Two)",
        description="Required only if a two-year plan is selected above.",
        choices=_FISCAL_YEAR_CHOICES,
        required=False,
    )

    # Tribal Organization
    tribal_lead_agency_name = acf_fields.CharField(
        title="Name of Tribal Lead Agency",
        max_length=200,
    )

    # 1.2a
    org_name = acf_fields.CharField(
        title="Name of Tribe or Tribal Organization",
        max_length=200,
    )

    # 1.2b Multi-tribe representation
    is_multi_tribe = acf_fields.ChoiceField(
        title="Are you representing more than one Tribe, Village, Community or Jurisdiction?",
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.RadioSelect(attrs={"radio_type": "tile"}),
    )
    multi_tribe_names = acf_fields.TextareaField(
        title="Names of all Tribes/Villages/Communities/Jurisdictions represented",
        description="Required if representing more than one tribe. Maximum 1,000 characters.",
        max_length=1000,
        required=False,
    )
    # NOTE: Per CSV decisions (3/24 PO Notes), tribal resolution upload was moved here
    # from Section 2.1 to be adjacent to the multi-tribe question at 1.2b.
    # TODO: Final allowed file types and max size pending confirmation from ACF.
    tribal_resolution_upload = acf_fields.FileField(
        title="Tribal Resolution(s)",
        description=(
            "Upload tribal resolution documentation. Required if representing more than one tribe. "
            "Allowed types: PDF, PNG, JPG, JPEG. Maximum size: 10 MB."
        ),
        required=False,
    )

    # 1.3 Authorized Tribal Official
    authorized_official_name = acf_fields.CharField(title="Full name", max_length=200)
    authorized_official_title = acf_fields.CharField(title="Title", max_length=200)
    authorized_official_street = acf_fields.CharField(title="Street address", max_length=200)
    authorized_official_city = acf_fields.CharField(title="City", max_length=100)
    authorized_official_state = acf_fields.ChoiceField(title="State", choices=US_STATES)
    authorized_official_zip = acf_fields.CharField(
        title="ZIP code",
        max_length=5,
        min_length=5,
    )
    authorized_official_phone = acf_fields.CharField(
        title="Phone number",
        widget=forms.TelInput,  # type: ignore
    )
    authorized_official_extension = acf_fields.CharField(
        title="Extension (Optional)",
        required=False,
        max_length=10,
    )
    authorized_official_fax = acf_fields.CharField(
        title="Fax number (Optional)",
        widget=forms.TelInput,  # type: ignore
        required=False,
    )
    authorized_official_email = acf_fields.CharField(
        title="Email address",
        widget=forms.EmailInput,
    )
    authorized_official_website = acf_fields.CharField(
        title="Website (Optional)",
        required=False,
        max_length=200,
    )

    # 1.4 Tribal CSBG Point of Contact
    contact_name = acf_fields.CharField(title="Full name", max_length=200)
    contact_title = acf_fields.CharField(title="Title", max_length=200)
    contact_street = acf_fields.CharField(title="Street address", max_length=200)
    contact_city = acf_fields.CharField(title="City", max_length=100)
    contact_state = acf_fields.ChoiceField(title="State", choices=US_STATES)
    contact_zip = acf_fields.CharField(title="ZIP code", max_length=5, min_length=5)
    contact_phone = acf_fields.CharField(
        title="Phone number",
        widget=forms.TelInput,  # type: ignore
    )
    contact_extension = acf_fields.CharField(
        title="Extension (Optional)",
        required=False,
        max_length=10,
    )
    contact_fax = acf_fields.CharField(
        title="Fax number (Optional)",
        widget=forms.TelInput,  # type: ignore
        required=False,
    )
    contact_email = acf_fields.CharField(
        title="Email address",
        widget=forms.EmailInput,
        max_length=150,
    )

    # 1.5 Delegation of Authority
    has_delegation = acf_fields.ChoiceField(
        title="Is signature authority being delegated?",
        description="If No, proceed to Section 2.",
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.RadioSelect(attrs={"radio_type": "tile"}),
    )
    # 1.5b Additional Authorized Official (conditional on has_delegation = yes)
    delegation_name = acf_fields.CharField(title="Full name", required=False, max_length=200)
    delegation_title = acf_fields.CharField(title="Title", required=False, max_length=200)
    delegation_phone = acf_fields.CharField(
        title="Phone number",
        widget=forms.TelInput,  # type: ignore
        required=False,
    )
    delegation_extension = acf_fields.CharField(
        title="Extension (Optional)",
        required=False,
        max_length=10,
    )
    delegation_email = acf_fields.CharField(
        title="Email address",
        widget=forms.EmailInput,
        required=False,
        max_length=100,
    )

    # endregion

    # region Section 2 — Tribal Resolution and Recognition
    # NOTE: Section 2.1 (standalone "Is the applicant representing more than one Tribe?")
    # has been removed per 3/24 PO Notes. The question and associated upload have been
    # consolidated into Section 1 at field 1.2b. See tribal_resolution_upload above.

    # 2.2a
    has_recognition = acf_fields.ChoiceField(
        title="Do all Tribes/Villages/Communities/Jurisdictions served have state or federal recognition?",
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.RadioSelect(attrs={"radio_type": "tile"}),
    )
    # 2.2b Recognition citation and upload (conditional on has_recognition = yes)
    recognition_citation = acf_fields.CharField(
        title="State or federal recognition citation",
        description="Required if recognition exists. Provide the citation for the recognition.",
        max_length=500,
        required=False,
    )
    recognition_upload = acf_fields.FileField(
        title="Recognition documentation",
        description=(
            "Upload supporting recognition documentation. Required if recognition exists. "
            "Allowed types: PDF, PNG, JPG, JPEG. Maximum size: 10 MB."
        ),
        required=False,
    )
    # NOTE: 2.2b-no (explanation for lack of recognition) has been removed per 3/24 PO Notes.
    # POs confirmed: "Tribes don't need to explain. There does not need to be a pop-up if a tribe selects No."

    # endregion

    # region Section 3 — CSBG Tribal Plan Goals and Objectives

    # 3.1
    goals_and_objectives = acf_fields.TextareaField(
        title="CSBG Goals, Objectives, and Strategies",
        description="Maximum 5,000 characters.",
        max_length=5000,
    )

    # endregion

    # region Section 4 — CSBG Community-Based Feedback

    # 4.1a/b
    community_feedback = acf_fields.YesNoDisplayField(
        title="Did the Tribe solicit feedback from Tribal members served?",
        fields=[
            acf_fields.TextareaField(
                title="Describe how feedback was solicited",
                description="Maximum 5,000 characters.",
                max_length=5000,
                required=False,
            )
        ],
        validators=[],
    )

    # endregion

    # region Section 5 — Use of Funds and Fiscal Controls

    # 5.1 Year 1 Allocations (must total 100%)
    alloc_admin_y1 = acf_fields.DecimalField(
        title="Administrative Funds",
        review_title="Administrative Funds (Year 1 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )
    alloc_employment_y1 = acf_fields.DecimalField(
        title="Employment",
        review_title="Employment (Year 1 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )
    alloc_education_y1 = acf_fields.DecimalField(
        title="Childcare, Early Childhood, Youth Development, and Adult Education",
        review_title="Education and Youth Development (Year 1 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )
    alloc_income_y1 = acf_fields.DecimalField(
        title="Income and Asset Building",
        review_title="Income and Asset Building (Year 1 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )
    alloc_housing_y1 = acf_fields.DecimalField(
        title="Housing",
        review_title="Housing (Year 1 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )
    alloc_health_y1 = acf_fields.DecimalField(
        title="Health and Nutrition",
        review_title="Health and Nutrition (Year 1 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )
    alloc_civic_y1 = acf_fields.DecimalField(
        title="Civic Engagement and Community Involvement",
        review_title="Civic Engagement and Community Involvement (Year 1 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )
    alloc_transportation_y1 = acf_fields.DecimalField(
        title="Transportation",
        review_title="Transportation (Year 1 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )
    alloc_partnerships_y1 = acf_fields.DecimalField(
        title="Partnerships, Linkages, and Service Coordination",
        review_title="Partnerships, Linkages, and Service Coordination (Year 1 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )
    alloc_total_y1 = acf_fields.CalculatedDecimalField(
        title="Year 1 Total",
        review_title="Year 1 Total (%)",
        fields=_Y1_ALLOCATION_FIELDS,
        max_digits=5,
        decimal_places=2,
    )

    # 5.1 Year 2 Allocations (conditional on two-year plan; must total 100%)
    alloc_admin_y2 = acf_fields.DecimalField(
        title="Administrative Funds",
        review_title="Administrative Funds (Year 2 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
    )
    alloc_employment_y2 = acf_fields.DecimalField(
        title="Employment",
        review_title="Employment (Year 2 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
    )
    alloc_education_y2 = acf_fields.DecimalField(
        title="Childcare, Early Childhood, Youth Development, and Adult Education",
        review_title="Education and Youth Development (Year 2 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
    )
    alloc_income_y2 = acf_fields.DecimalField(
        title="Income and Asset Building",
        review_title="Income and Asset Building (Year 2 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
    )
    alloc_housing_y2 = acf_fields.DecimalField(
        title="Housing",
        review_title="Housing (Year 2 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
    )
    alloc_health_y2 = acf_fields.DecimalField(
        title="Health and Nutrition",
        review_title="Health and Nutrition (Year 2 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
    )
    alloc_civic_y2 = acf_fields.DecimalField(
        title="Civic Engagement and Community Involvement",
        review_title="Civic Engagement and Community Involvement (Year 2 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
    )
    alloc_transportation_y2 = acf_fields.DecimalField(
        title="Transportation",
        review_title="Transportation (Year 2 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
    )
    alloc_partnerships_y2 = acf_fields.DecimalField(
        title="Partnerships, Linkages, and Service Coordination",
        review_title="Partnerships, Linkages, and Service Coordination (Year 2 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
    )
    alloc_total_y2 = acf_fields.CalculatedDecimalField(
        title="Year 2 Total",
        review_title="Year 2 Total (%)",
        fields=_Y2_ALLOCATION_FIELDS,
        max_digits=5,
        decimal_places=2,
    )

    # 5.2 Limitation on Use of Funds - Acknowledgment
    use_of_funds_acknowledgment = acf_fields.BooleanField(
        title="I acknowledge the limitation on use of CSBG funds as described above.",
    )

    # 5.3 Single Audit Review
    audit_date = acf_fields.DateField(
        title="Date of most recent audit",
        description="Enter as mm/dd/yyyy.",
        required=False,
    )
    # NOTE: Fiscal year covered is implemented as free text per 3/24 PO Notes.
    # PDE/PS teams will provide guidance on final instruction language.
    audit_fiscal_period = acf_fields.CharField(
        title="Fiscal year covered by most recent audit",
        description=(
            "Enter the fiscal period as mm/dd/yyyy – mm/dd/yyyy. "
            "If you received less than $750,000 in total federal funds, this question is optional."
        ),
        required=False,
        max_length=50,
    )

    # endregion

    # region Section 6 — Individual Eligibility and Targeted Community Eligibility

    # 6.1
    individual_eligibility = acf_fields.TextareaField(
        title="Individual Eligibility",
        description=(
            "Describe your policies and procedures for determining individual eligibility. "
            "Maximum 5,000 characters."
        ),
        max_length=5000,
    )

    # 6.2
    targeted_community_eligibility = acf_fields.TextareaField(
        title="Targeted Community Eligibility",
        description=(
            "Describe how your services target and benefit low-income communities. "
            "Maximum 5,000 characters."
        ),
        max_length=5000,
    )

    # endregion

    # region Section 7 — CSBG Statement of Assurances

    # 7.1 Assurances Narrative
    assurance_narrative = acf_fields.TextareaField(
        title="Description",
        description="Maximum 5,000 characters.",
        max_length=5000,
    )

    # 7.2 Attestation and typed signature
    assurance_attestation = acf_fields.BooleanField(
        title=(
            "By checking this box, the Tribal CSBG authorized official is certifying "
            "the assurances set out above."
        ),
    )
    assurance_signature = acf_fields.CharField(
        title="Authorized Tribal Official Signature",
        description="Type your full name to sign.",
        max_length=200,
    )

    # endregion

    # region Section 8 — Federal Certifications

    # 8.1 Lobbying Certification
    lobbying_attestation = acf_fields.BooleanField(
        title=(
            "I have reviewed this certification and affirm that the Tribe or Tribal "
            "Organization will ensure compliance with it"
        ),
    )
    lobbying_signature = acf_fields.CharField(
        title="Authorized Tribal Official Signature",
        description="Type your full name to sign.",
        max_length=200,
    )

    # 8.2 Drug-Free Workplace Certification
    drug_free_attestation = acf_fields.BooleanField(
        title=(
            "I have reviewed this certification and affirm that the Tribe or Tribal "
            "Organization will ensure compliance with it"
        ),
    )
    drug_free_place_of_performance = acf_fields.CharField(
        title="Place of Performance (street, city, county, state, ZIP code)",
        description=(
            "Provide the address or location where CSBG-funded activities will be performed."
        ),
        max_length=500,
    )
    # TODO: Exact question wording and behavior for "unidentified workplaces" is pending
    # guidance from ACF legal team (Kayla and Melanie following up with program specialists).
    drug_free_unidentified_workplaces = acf_fields.YesNoDisplayField(
        title="Are there additional locations where CSBG-funded work is performed?",
        fields=[
            acf_fields.TextareaField(
                title="List additional workplace location(s)",
                description="500 characters allowed.",
                max_length=500,
                required=False,
            )
        ],
        validators=[],
    )
    drug_free_signature = acf_fields.CharField(
        title="Authorized Tribal Official Signature",
        description="Type your full name to sign.",
        max_length=200,
    )

    # 8.3 Debarment, Suspension Certification
    debarment_attestation = acf_fields.BooleanField(
        title=(
            "I have reviewed this certification and affirm that the Tribe or Tribal "
            "Organization will ensure compliance with it"
        ),
    )
    debarment_signature = acf_fields.CharField(
        title="Authorized Tribal Official Signature",
        description="Type your full name to sign.",
        max_length=200,
    )

    # 8.4 Tobacco Smoke Certification
    tobacco_attestation = acf_fields.BooleanField(
        title=(
            "I have reviewed this certification and affirm that the Tribe or Tribal "
            "Organization will ensure compliance with it"
        ),
    )
    tobacco_signature = acf_fields.CharField(
        title="Authorized Tribal Official Signature",
        description="Type your full name to sign.",
        max_length=200,
    )

    # endregion

    # region Additional Documents

    # TODO: Final file upload constraints (allowed types, count, size) pending confirmation from ACF.
    additional_documents = acf_fields.FileField(
        title="Additional Documents (Optional)",
        description=(
            "Upload any additional supporting documents. "
            "Allowed types: PDF, PNG, JPG, JPEG. Maximum size: 10 MB."
        ),
        required=False,
    )

    # endregion

    def clean(self):
        cleaned_data = super().clean()

        plan_coverage = cleaned_data.get("plan_coverage")
        is_multi_tribe = cleaned_data.get("is_multi_tribe")
        has_delegation = cleaned_data.get("has_delegation")
        has_recognition = cleaned_data.get("has_recognition")

        # 1.2b: Multi-tribe names and tribal resolution upload are required when
        # representing more than one tribe.
        if is_multi_tribe == "yes":
            if not cleaned_data.get("multi_tribe_names"):
                self.add_error(
                    "multi_tribe_names",
                    "Names of all represented tribes are required when representing more than one tribe.",
                )
            if not cleaned_data.get("tribal_resolution_upload"):
                self.add_error(
                    "tribal_resolution_upload",
                    "Tribal resolution documentation is required when representing more than one tribe.",
                )

        # 1.5: Additional Authorized Official fields are required when delegating authority.
        if has_delegation == "yes":
            for field_name, label in [
                ("delegation_name", "Full name"),
                ("delegation_title", "Title"),
                ("delegation_phone", "Phone number"),
                ("delegation_email", "Email address"),
            ]:
                if not cleaned_data.get(field_name):
                    self.add_error(
                        field_name,
                        f"{label} is required when delegating signature authority.",
                    )

        # 2.2b: At least one of citation or upload is required when tribes have recognition.
        if has_recognition == "yes":
            if not cleaned_data.get("recognition_citation") and not cleaned_data.get(
                "recognition_upload"
            ):
                self.add_error(
                    "recognition_citation",
                    "Provide a recognition citation or upload supporting documentation.",
                )

        # 1.1a-Y2 and Year 2 allocations: required when a two-year plan is selected.
        if plan_coverage == "two_year":
            if not cleaned_data.get("fiscal_year_y2"):
                self.add_error(
                    "fiscal_year_y2",
                    "Fiscal year for Year Two is required for a two-year plan.",
                )
            for field_name in _Y2_ALLOCATION_FIELDS:
                if cleaned_data.get(field_name) is None:
                    self.add_error(field_name, "This allocation is required for a two-year plan.")

        # 5.1: Year 1 allocation total must equal 100%.
        y1_values = [cleaned_data.get(f) for f in _Y1_ALLOCATION_FIELDS]
        if all(v is not None for v in y1_values):
            y1_total = sum(Decimal(str(v)) for v in y1_values)
            if y1_total != Decimal("100"):
                raise forms.ValidationError(
                    f"Year 1 allocation percentages must total 100%. Current total: {y1_total}%."
                )

        # 5.1: Year 2 allocation total must equal 100% when a two-year plan is selected.
        if plan_coverage == "two_year":
            y2_values = [cleaned_data.get(f) for f in _Y2_ALLOCATION_FIELDS]
            if all(v is not None for v in y2_values):
                y2_total = sum(Decimal(str(v)) for v in y2_values)
                if y2_total != Decimal("100"):
                    raise forms.ValidationError(
                        f"Year 2 allocation percentages must total 100%. Current total: {y2_total}%."
                    )

        return cleaned_data


class TribalPlanForm(BaseFormSchema):
    family: FormFamilies = Field(FormFamilies.CSBG_TRIBAL_PLAN_APPLICATION, frozen=True)
    name: AllFormNames = Field(CSBGTribalPlanApplicationForms.CSBG_TRIBAL_PLAN, frozen=True)
    variant: SemanticVersion = Field(SemanticVersion(1, 0, 0), frozen=True)
    form_fields: TribalPlanFormFields  # type: ignore
    ui: UIDefinition = Field(
        frozen=True,
        default=[
            # Step 1: Section 1 — Tribal Administrative Information
            StepBlock(
                title="Tribal Administrative Information",
                children=[
                    PermanentPageBlock(
                        title="Plan Coverage",
                        children=[
                            SectionBlock(
                                title="Plan Coverage",
                                children=[
                                    ReviewSubheadingBlock(title="Plan Coverage"),
                                    FieldBlock(field_name="plan_coverage"),
                                    FieldBlock(field_name="fiscal_year_y1"),
                                    FieldBlock(field_name="fiscal_year_y2"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Tribal Information",
                        children=[
                            SectionBlock(
                                title="Tribal Information",
                                children=[
                                    ReviewSubheadingBlock(title="Tribal Information"),
                                    FieldBlock(field_name="tribal_lead_agency_name"),
                                    FieldBlock(field_name="org_name"),
                                ],
                            ),
                            SectionBlock(
                                title="Tribal Representation",
                                children=[
                                    ReviewSubheadingBlock(title="Tribal Representation"),
                                    FieldBlock(field_name="is_multi_tribe"),
                                    FieldBlock(field_name="multi_tribe_names"),
                                    FieldBlock(field_name="tribal_resolution_upload"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Authorized Tribal Official",
                        children=[
                            SectionBlock(
                                title="Authorized Tribal Official",
                                children=[
                                    ReviewSubheadingBlock(title="Authorized Tribal Official"),
                                    FieldBlock(field_name="authorized_official_name"),
                                    FieldBlock(field_name="authorized_official_title"),
                                    FieldBlock(field_name="authorized_official_street"),
                                    FieldBlock(field_name="authorized_official_city"),
                                    FieldBlock(field_name="authorized_official_state"),
                                    FieldBlock(field_name="authorized_official_zip"),
                                    FieldBlock(field_name="authorized_official_phone"),
                                    FieldBlock(field_name="authorized_official_extension"),
                                    FieldBlock(field_name="authorized_official_fax"),
                                    FieldBlock(field_name="authorized_official_email"),
                                    FieldBlock(field_name="authorized_official_website"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Tribal Program Contact",
                        children=[
                            SectionBlock(
                                title="Tribal Program Contact",
                                children=[
                                    ReviewSubheadingBlock(title="Tribal Program Contact"),
                                    FieldBlock(field_name="contact_name"),
                                    FieldBlock(field_name="contact_title"),
                                    FieldBlock(field_name="contact_street"),
                                    FieldBlock(field_name="contact_city"),
                                    FieldBlock(field_name="contact_state"),
                                    FieldBlock(field_name="contact_zip"),
                                    FieldBlock(field_name="contact_phone"),
                                    FieldBlock(field_name="contact_extension"),
                                    FieldBlock(field_name="contact_fax"),
                                    FieldBlock(field_name="contact_email"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Delegation of Authority",
                        subtitle=(
                            "If signature authority is being delegated, complete the "
                            "Additional Authorized Official fields below."
                        ),
                        children=[
                            SectionBlock(
                                title="Delegation of Authority",
                                children=[
                                    ReviewSubheadingBlock(title="Delegation of Authority"),
                                    FieldBlock(field_name="has_delegation"),
                                ],
                            ),
                            SectionBlock(
                                title="Additional Authorized Official",
                                description="Complete only if signature authority is being delegated.",
                                children=[
                                    ReviewSubheadingBlock(title="Additional Authorized Official"),
                                    FieldBlock(field_name="delegation_name"),
                                    FieldBlock(field_name="delegation_title"),
                                    FieldBlock(field_name="delegation_phone"),
                                    FieldBlock(field_name="delegation_extension"),
                                    FieldBlock(field_name="delegation_email"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Step 2: Section 2 — Tribal Recognition
            StepBlock(
                title="Tribal Recognition",
                children=[
                    PermanentPageBlock(
                        title="Tribal Recognition",
                        children=[
                            SectionBlock(
                                title="Tribal Recognition",
                                children=[
                                    ReviewSubheadingBlock(title="Tribal Recognition"),
                                    FieldBlock(field_name="has_recognition"),
                                    FieldBlock(field_name="recognition_citation"),
                                    FieldBlock(field_name="recognition_upload"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Step 3: Section 3 — Goals and Objectives
            StepBlock(
                title="Goals and Objectives",
                children=[
                    PermanentPageBlock(
                        title="Goals and Objectives",
                        subtitle=(
                            "Briefly describe the Tribe or Tribal Organization's CSBG-specific goals "
                            "and objectives for the Community Services Block Grant funding, as applicable."
                        ),
                        children=[
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Goals and Objectives"),
                                    FieldBlock(field_name="goals_and_objectives"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Step 4: Section 4 — Community-Based Feedback
            StepBlock(
                title="Community-Based Feedback",
                children=[
                    PermanentPageBlock(
                        title="Community-Based Feedback",
                        children=[
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Community-Based Feedback"),
                                    FieldBlock(
                                        field_name="community_feedback",
                                        review_template_name="form_manager/forms/yes_no_display_review.html",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Step 5: Section 5 — Use of Funds & Fiscal Controls
            StepBlock(
                title="Use of Funds & Fiscal Controls",
                children=[
                    PermanentPageBlock(
                        title="Planned Allocation of Funds",
                        subtitle=(
                            "For program funds, enter the percentage allocated to each CSBG service "
                            "area. The total must equal 100%."
                        ),
                        children=[
                            AlertBoxBlock(
                                alert_type="info",
                                heading="Allocation requirements for CSBG funds",
                                message=(
                                    "According to the CSBG Act: no more than 5% of funds may be used "
                                    "for administrative costs, and at least 95% must be allocated to "
                                    "program services."
                                ),
                            ),
                            FieldGroupBlock(
                                description=(
                                    "Year One allocations: enter percentages (0–100). "
                                    "The total must equal 100%."
                                ),
                                children=[
                                    ReviewSubheadingBlock(title="Year One"),
                                    FieldBlock(field_name="alloc_admin_y1"),
                                    FieldBlock(field_name="alloc_employment_y1"),
                                    FieldBlock(field_name="alloc_education_y1"),
                                    FieldBlock(field_name="alloc_income_y1"),
                                    FieldBlock(field_name="alloc_housing_y1"),
                                    FieldBlock(field_name="alloc_health_y1"),
                                    FieldBlock(field_name="alloc_civic_y1"),
                                    FieldBlock(field_name="alloc_transportation_y1"),
                                    FieldBlock(field_name="alloc_partnerships_y1"),
                                    FieldBlock(field_name="alloc_total_y1"),
                                ],
                            ),
                            AlertBoxBlock(
                                alert_type="info",
                                heading="Two-Year Plan Only",
                                message=(
                                    "Complete Year Two allocations only if you selected a two-year "
                                    "plan in Section 1 (Plan Coverage)."
                                ),
                            ),
                            FieldGroupBlock(
                                description=(
                                    "Year Two allocations: enter percentages (0–100). "
                                    "The total must equal 100%."
                                ),
                                children=[
                                    ReviewSubheadingBlock(title="Year Two"),
                                    FieldBlock(field_name="alloc_admin_y2"),
                                    FieldBlock(field_name="alloc_employment_y2"),
                                    FieldBlock(field_name="alloc_education_y2"),
                                    FieldBlock(field_name="alloc_income_y2"),
                                    FieldBlock(field_name="alloc_housing_y2"),
                                    FieldBlock(field_name="alloc_health_y2"),
                                    FieldBlock(field_name="alloc_civic_y2"),
                                    FieldBlock(field_name="alloc_transportation_y2"),
                                    FieldBlock(field_name="alloc_partnerships_y2"),
                                    FieldBlock(field_name="alloc_total_y2"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Limitation on Use of Funds",
                        children=[
                            SectionBlock(
                                title="Limitation on Use of Funds",
                                children=[
                                    ReviewSubheadingBlock(title="Limitation on Use of Funds"),
                                    FieldBlock(field_name="use_of_funds_acknowledgment"),
                                ],
                            ),
                            SectionBlock(
                                title="Single Audit Review",
                                children=[
                                    ReviewSubheadingBlock(title="Single Audit Review"),
                                    FieldBlock(field_name="audit_date"),
                                    FieldBlock(field_name="audit_fiscal_period"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Step 6: Section 6 — Individual & Targeted Community Eligibility
            StepBlock(
                title="Individual & Targeted Community Eligibility",
                children=[
                    PermanentPageBlock(
                        title="Individual Eligibility",
                        subtitle=(
                            "Describe your tribe's policies and procedures for determining "
                            "individual eligibility for CSBG services."
                        ),
                        children=[
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Individual Eligibility"),
                                    FieldBlock(field_name="individual_eligibility"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Targeted Community",
                        subtitle=(
                            "Describe how your tribe's services target and benefit "
                            "low-income communities."
                        ),
                        children=[
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Targeted Community"),
                                    FieldBlock(field_name="targeted_community_eligibility"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Step 7: Section 7 — Statement of Assurances
            StepBlock(
                title="Statement of Assurances",
                children=[
                    PermanentPageBlock(
                        title="Assurances Narrative",
                        subtitle=(
                            "Provide a narrative description of how the tribe or tribal organization "
                            "will carry out the required programmatic assurances."
                        ),
                        children=[
                            AlertBoxBlock(
                                alert_type="info",
                                heading="Programmatic assurances topics",
                                message=_ASSURANCES_NARRATIVE_TOPICS,
                            ),
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Assurances Narrative"),
                                    FieldBlock(field_name="assurance_narrative"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Statement of Assurances",
                        subtitle=(
                            "Review the certification below and sign at the bottom of this page to "
                            "affirm compliance. Full legislation: Community Services Block Grant "
                            "Reauthorization Act of 1998 (P.L. 105-285)."
                        ),
                        children=[
                            TextBlock(
                                bordered=True,
                                heading="Statement of CSBG Assurances",
                                text=_CSBG_ASSURANCES_NARRATIVE,
                            ),
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Statement of Assurances"),
                                    FieldBlock(field_name="assurance_attestation"),
                                    FieldBlock(field_name="assurance_signature"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Step 8: Section 8 — Federal Certifications
            StepBlock(
                title="Federal Certifications",
                children=[
                    PermanentPageBlock(
                        title="Regarding Lobbying",
                        subtitle=(
                            "Review the certification below and sign at the bottom of this page to "
                            "affirm compliance."
                        ),
                        children=[
                            TextBlock(
                                bordered=True,
                                heading="Certification Regarding Lobbying",
                                text=_LOBBYING_CERTIFICATION_TEXT,
                            ),
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Regarding Lobbying"),
                                    FieldBlock(field_name="lobbying_attestation"),
                                    FieldBlock(field_name="lobbying_signature"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Drug-Free Workplace Requirements",
                        subtitle=(
                            "Review the certification below and sign at the bottom of this page to "
                            "affirm compliance."
                        ),
                        children=[
                            AccordionBlock(
                                items=[
                                    AccordionItem(
                                        heading="Instructions for Certifications",
                                        text=_DRUG_FREE_WORKPLACE_CERTIFICATION_TEXT,
                                        is_expanded=False,
                                    )
                                ]
                            ),
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Drug-Free Workplace Requirements"),
                                    FieldBlock(field_name="drug_free_attestation"),
                                    FieldBlock(field_name="drug_free_place_of_performance"),
                                    FieldBlock(
                                        field_name="drug_free_unidentified_workplaces",
                                        review_template_name="form_manager/forms/yes_no_display_review.html",
                                    ),
                                    FieldBlock(field_name="drug_free_signature"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Debarment, Suspension and Other Responsibility Matters",
                        subtitle=(
                            "Review the certification below and sign at the bottom of this page to "
                            "affirm compliance."
                        ),
                        children=[
                            AccordionBlock(
                                items=[
                                    AccordionItem(
                                        heading=(
                                            "Instructions for Certifications - Primary Covered Transactions"
                                        ),
                                        text=_DEBARMENT_PRIMARY_INSTRUCTIONS_TEXT,
                                        is_expanded=False,
                                    ),
                                    AccordionItem(
                                        heading=(
                                            "Instructions for Certifications - Lower Tier Covered Transactions"
                                        ),
                                        text=_DEBARMENT_LOWER_TIER_INSTRUCTIONS_TEXT,
                                        is_expanded=False,
                                    ),
                                ]
                            ),
                            TextBlock(
                                bordered=False,
                                text=_DEBARMENT_CERTIFICATION_TEXT,
                            ),
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(
                                        title="Debarment, Suspension and Other Responsibility Matters"
                                    ),
                                    FieldBlock(field_name="debarment_attestation"),
                                    FieldBlock(field_name="debarment_signature"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Environmental Tobacco Smoke",
                        subtitle=(
                            "Review the certification below and sign at the bottom of this page to "
                            "affirm compliance."
                        ),
                        children=[
                            TextBlock(
                                bordered=True,
                                heading="Certification Regarding Environmental Tobacco Smoke",
                                text=_TOBACCO_SMOKE_CERTIFICATION_TEXT,
                            ),
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Environmental Tobacco Smoke"),
                                    FieldBlock(field_name="tobacco_attestation"),
                                    FieldBlock(field_name="tobacco_signature"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    model_config = ConfigDict(use_enum_values=True)
