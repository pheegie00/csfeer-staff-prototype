"""Field definitions for the CSBG Tribal Plan form."""

from decimal import Decimal

from django import forms

from form_manager.schema.choices import FISCAL_YEAR_CHOICES, US_STATES
from form_manager.schema.fields import acf_fields
from form_manager.schema.forms.base import BaseFields

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

_NEXT_FISCAL_YEAR_VALUE, _NEXT_FISCAL_YEAR_LABEL = FISCAL_YEAR_CHOICES[1]
_FOLLOWING_FISCAL_YEAR_VALUE, _FOLLOWING_FISCAL_YEAR_LABEL = FISCAL_YEAR_CHOICES[2]
_RECOGNITION_METHOD_MANUAL = "manual"
_RECOGNITION_METHOD_UPLOAD = "upload"


class TribalPlanFormFields(BaseFields):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        has_completed_single_audit = self.data.get("has_completed_single_audit")
        if has_completed_single_audit is None:
            has_completed_single_audit = self.initial.get("has_completed_single_audit")

        single_audit_dates_required = has_completed_single_audit == "yes"
        for field_name in ("audit_date", "audit_period_start", "audit_period_end"):
            self.fields[field_name].required = single_audit_dates_required

    # region Section 1 — CSBG Tribal Administrative Information

    # 1.1 Plan Coverage
    plan_coverage = acf_fields.ChoiceField(
        title="Plan Coverage",
        choices=[("one_year", "One year plan"), ("two_year", "Two year plan")],
        widget=forms.RadioSelect(attrs={"radio_type": "tile"}),
    )

    # 1.1a Fiscal Years
    fiscal_year_y1 = acf_fields.ChoiceField(
        title="Fiscal Year (Year One)",
        review_title="Year One",
        choices=FISCAL_YEAR_CHOICES,
        initial=_NEXT_FISCAL_YEAR_VALUE,
        required=False,
        widget=forms.HiddenInput,
    )
    fiscal_year_y2 = acf_fields.ChoiceField(
        title="Fiscal Year (Year Two)",
        review_title="Year Two",
        description="Required only if a two-year plan is selected above.",
        choices=FISCAL_YEAR_CHOICES,
        required=False,
        widget=forms.HiddenInput(
            attrs={
                "x-bind:value": (f"checked === 'two_year' ? '{_FOLLOWING_FISCAL_YEAR_VALUE}' : ''")
            }
        ),
    )
    fiscal_year_y1_display_one_year = acf_fields.CharField(
        title="Year One",
        initial=_NEXT_FISCAL_YEAR_LABEL,
        required=False,
        disabled=True,
        is_presentational_only=True,
    )
    fiscal_year_y1_display_two_year = acf_fields.CharField(
        title="Year One",
        initial=_NEXT_FISCAL_YEAR_LABEL,
        required=False,
        disabled=True,
        is_presentational_only=True,
    )
    fiscal_year_y2_display = acf_fields.CharField(
        title="Year Two",
        initial=_FOLLOWING_FISCAL_YEAR_LABEL,
        required=False,
        disabled=True,
        is_presentational_only=True,
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
        title="List the names of Tribes, Villages, Communities, or Jurisdictions",
        description="Required if representing more than one tribe. Maximum 1,000 characters.",
        max_length=1000,
        required=False,
    )
    # NOTE: Per CSV decisions (3/24 PO Notes), tribal resolution upload was moved here
    # from Section 2.1 to be adjacent to the multi-tribe question at 1.2b.
    # TODO: Final allowed file types and max size pending confirmation from ACF.
    tribal_resolution_upload = acf_fields.FileField(
        title="Attach Tribal Resolutions granting authority to receive CSBG funds",
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
        title=(
            "Do all Tribes, Villages, Communities, and Jurisdictions served"
            " have state or federal recognition?"
        ),
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.RadioSelect(attrs={"radio_type": "tile"}),
    )
    recognition_information_method = acf_fields.ChoiceField(
        title="How would you like to provide this information?",
        choices=[
            (_RECOGNITION_METHOD_MANUAL, "Enter it manually"),
            (_RECOGNITION_METHOD_UPLOAD, "Upload a file"),
        ],
        required=False,
        widget=forms.RadioSelect(attrs={"radio_type": "tile"}),
    )
    # 2.2b Recognition citation and upload (conditional on has_recognition = yes)
    recognition_citation = acf_fields.TextareaField(
        title="Provide a citation to the State statute or code acknowledging State recognition",
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={"rows": 7, "cols": 49}),
    )
    recognition_upload = acf_fields.FileField(
        title="Recognition documentation",
        description=(
            "Upload supporting recognition documentation. "
            "Required if the upload option is selected. "
            "Allowed types: PDF, PNG, JPG, JPEG. Maximum size: 10 MB."
        ),
        required=False,
    )
    # NOTE: 2.2b-no (explanation for lack of recognition) has been removed per 3/24 PO Notes.
    # POs confirmed: "Tribes don't need to explain. There does not need to be a pop-up
    # if a tribe selects No."

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
        title=(
            "Did the Tribe or Tribal Organization solicit feedback from Tribal members "
            "that demonstrates evidence of public participation?"
        ),
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
        title="Administrative Cost",
        review_title="Administrative Cost (Year 1 %)",
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
        title="Income & Asset Building",
        review_title="Income & Asset Building (Year 1 %)",
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
        title="Health & Nutrition",
        review_title="Health & Nutrition (Year 1 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )
    alloc_civic_y1 = acf_fields.DecimalField(
        title="Civic Engagement & Community Involvement",
        review_title="Civic Engagement & Community Involvement (Year 1 %)",
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
        title="Total (auto-calculated)",
        review_title="Total (auto-calculated) (%)",
        fields=_Y1_ALLOCATION_FIELDS,
        max_digits=5,
        decimal_places=2,
    )

    # 5.1 Year 2 Allocations (conditional on two-year plan; must total 100%)
    alloc_admin_y2 = acf_fields.DecimalField(
        title="Administrative Cost",
        review_title="Administrative Cost (Year 2 %)",
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
        title="Income & Asset Building",
        review_title="Income & Asset Building (Year 2 %)",
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
        title="Health & Nutrition",
        review_title="Health & Nutrition (Year 2 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
    )
    alloc_civic_y2 = acf_fields.DecimalField(
        title="Civic Engagement & Community Involvement",
        review_title="Civic Engagement & Community Involvement (Year 2 %)",
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
        title="Total (auto-calculated)",
        review_title="Total (auto-calculated) (%)",
        fields=_Y2_ALLOCATION_FIELDS,
        max_digits=5,
        decimal_places=2,
    )

    # 5.2 Limitation on Use of Funds - Acknowledgment
    use_of_funds_acknowledgment = acf_fields.BooleanField(
        title=(
            "The Tribe or Tribal Organization acknowledges and assures compliance "
            "with Section 678F of the CSBG Act"
        ),
    )

    # 5.3 Single Audit Review
    has_completed_single_audit = acf_fields.ChoiceField(
        title="Has your Tribe or Tribal Organization completed a Single Audit?",
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.RadioSelect(attrs={"radio_type": "tile"}),
    )
    audit_date = acf_fields.DateField(
        title="Date of audit",
        error_messages={"required": "Date of audit is required when a Single Audit was completed."},
        required=False,
    )
    audit_period_start = acf_fields.DateField(
        title="Period start",
        error_messages={"required": "Period start is required when a Single Audit was completed."},
        required=False,
    )
    audit_period_end = acf_fields.DateField(
        title="Period end",
        error_messages={"required": "Period end is required when a Single Audit was completed."},
        required=False,
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

    # TODO: Final file upload constraints (allowed types, count, size) pending
    # confirmation from ACF.
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

        if not cleaned_data:
            return cleaned_data

        plan_coverage = cleaned_data.get("plan_coverage")
        is_multi_tribe = cleaned_data.get("is_multi_tribe")
        has_delegation = cleaned_data.get("has_delegation")
        has_recognition = cleaned_data.get("has_recognition")
        recognition_information_method = cleaned_data.get("recognition_information_method")
        # 1.2b: Multi-tribe names and tribal resolution upload are required when
        # representing more than one tribe.
        if is_multi_tribe == "yes":
            if not cleaned_data.get("multi_tribe_names"):
                self.add_error(
                    "multi_tribe_names",
                    "Names of all represented tribes are required"
                    " when representing more than one tribe.",
                )
            if not cleaned_data.get("tribal_resolution_upload"):
                self.add_error(
                    "tribal_resolution_upload",
                    "Tribal resolution documentation is required"
                    " when representing more than one tribe.",
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

        # 2.2b: When recognition exists, users must choose how to provide it and
        # complete the field associated with that choice.
        if has_recognition == "yes":
            if not recognition_information_method:
                self.add_error(
                    "recognition_information_method",
                    "Select how you want to provide the recognition information.",
                )
            elif (
                recognition_information_method == _RECOGNITION_METHOD_MANUAL
                and not cleaned_data.get("recognition_citation")
            ):
                self.add_error(
                    "recognition_citation",
                    (
                        "Provide a citation to the State statute or code "
                        "acknowledging State recognition."
                    ),
                )
            elif recognition_information_method == _RECOGNITION_METHOD_UPLOAD and not (
                cleaned_data.get("recognition_upload") or self.initial.get("recognition_upload")
            ):
                self.add_error(
                    "recognition_upload",
                    "Upload supporting recognition documentation.",
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
                        "Year 2 allocation percentages must total 100%."
                        f" Current total: {y2_total}%."
                    )

        return cleaned_data
