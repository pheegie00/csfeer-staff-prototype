"""Field definitions for the CSBG Tribal Plan form."""

from datetime import date
from decimal import Decimal

from django import forms
from django.core.validators import RegexValidator

from form_manager.schema.choices import US_STATES
from form_manager.schema.fields import acf_fields
from form_manager.schema.forms.base import BaseFields
from form_manager.schema.widgets import DatePickerInput, PhoneInput

_PHONE_VALIDATOR = RegexValidator(r"^\d{10}$", "Enter a 10-digit phone number.")

_TODAY = date.today()
_NEXT_FY = (_TODAY.year + 1 if _TODAY.month >= 10 else _TODAY.year) + 1
_FY_Y1_LABEL = f"FY {_NEXT_FY} (October 1, {_NEXT_FY - 1} - Sept 30, {_NEXT_FY})"
_FY_Y2_LABEL = f"FY {_NEXT_FY + 1} (October 1, {_NEXT_FY} - Sept 30, {_NEXT_FY + 1})"

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
        title="Select a plan",
        choices=[("one_year", "One year plan"), ("two_year", "Two year plan")],
        widget=forms.RadioSelect(attrs={"radio_type": "tile"}),
    )

    # 1.1a Fiscal Years
    fiscal_year_y1 = acf_fields.CharField(
        title="Year One",
        initial=_FY_Y1_LABEL,
        disabled=True,
    )
    fiscal_year_y2 = acf_fields.CharField(
        title="Year Two",
        initial=_FY_Y2_LABEL,
        disabled=True,
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
        max_length=1000,
        required=False,
    )
    # NOTE: Per CSV decisions (3/24 PO Notes), tribal resolution upload was moved here
    # from Section 2.1 to be adjacent to the multi-tribe question at 1.2b.
    # TODO: Final allowed file types and max size pending confirmation from ACF.
    tribal_resolution_upload = acf_fields.FileField(
        title="Attach Tribal Resolutions granting authority to receive CSBG funds",
        description=("Accepted file types: PDF, PNG, JPG, JPEG. Maximum size: 10 MB"),
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
        description="Enter a 10-digit U.S. phone number (example: 123-456-7890)",
        widget=PhoneInput,
        validators=[_PHONE_VALIDATOR],
    )
    authorized_official_extension = acf_fields.CharField(
        title="Extension (Optional)",
        required=False,
        max_length=10,
    )
    authorized_official_fax = acf_fields.CharField(
        title="Fax number (Optional)",
        widget=PhoneInput,
        required=False,
        validators=[_PHONE_VALIDATOR],
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
        description="Enter a 10-digit U.S. phone number (example: 123-456-7890)",
        widget=PhoneInput,
        validators=[_PHONE_VALIDATOR],
    )
    contact_extension = acf_fields.CharField(
        title="Extension (Optional)",
        required=False,
        max_length=10,
    )
    contact_fax = acf_fields.CharField(
        title="Fax number (Optional)",
        widget=PhoneInput,
        required=False,
        validators=[_PHONE_VALIDATOR],
    )
    contact_email = acf_fields.CharField(
        title="Email address",
        widget=forms.EmailInput,
        max_length=150,
    )

    # 1.5 Delegation of Authority
    has_delegation = acf_fields.ChoiceField(
        title=(
            "Is the Authorized Tribal Official delegating signature authority"
            " to another individual?"
        ),
        description="If No, proceed to Section 2.",
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.RadioSelect(attrs={"radio_type": "tile"}),
    )
    # 1.5b Additional Authorized Official (conditional on has_delegation = yes)
    delegation_name = acf_fields.CharField(title="Full name", required=False, max_length=200)
    delegation_title = acf_fields.CharField(title="Title", required=False, max_length=200)
    delegation_phone = acf_fields.CharField(
        title="Phone number",
        description="Enter a 10-digit U.S. phone number (example: 123-456-7890)",
        widget=PhoneInput,
        required=False,
        validators=[_PHONE_VALIDATOR],
    )
    delegation_extension = acf_fields.CharField(
        title="Extension Number (Optional)",
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
            "Do all Tribes, Villages, Communities, and Jurisdictions have state"
            " or federal recognition?"
        ),
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.RadioSelect(attrs={"radio_type": "tile"}),
    )
    # 2.2b Method for providing recognition (conditional on has_recognition = yes)
    recognition_provision_method = acf_fields.ChoiceField(
        title="How would you like to provide this information?",
        choices=[("manual", "Enter it manually"), ("upload", "Upload a file")],
        widget=forms.RadioSelect(attrs={"radio_type": "tile"}),
        required=False,
    )
    # 2.2b Recognition citation (conditional on recognition_provision_method = manual)
    recognition_citation = acf_fields.TextareaField(
        title="Provide a citation to the State statute or code acknowledging State recognition",
        max_length=1000,
        required=False,
    )
    # 2.2b Recognition upload (conditional on recognition_provision_method = upload)
    recognition_upload = acf_fields.FileField(
        title="Attach a citation to State statute or code acknowledging State Recognition",
        description=("Accepted file types: PDF, PNG, JPG, JPEG. Maximum size: 10 MB"),
        required=False,
    )
    # NOTE: 2.2b-no (explanation for lack of recognition) has been removed per 3/24 PO Notes.
    # POs confirmed: "Tribes don't need to explain. There does not need to be a pop-up
    # if a tribe selects No."

    # endregion

    # region Section 3 — CSBG Tribal Plan Goals and Objectives

    # 3.1
    goals_and_objectives = acf_fields.TextareaField(
        title="Description",
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
    alloc_admin_y1 = acf_fields.PercentageField(
        title="Administrative cost",
        review_title="Administrative Funds (Year 1 %)",
        max_digits=5,
        decimal_places=0,
        min_value=0,
        max_value=5,
        error_messages={"max_value": "Cannot exceed 5%%"},
    )
    alloc_employment_y1 = acf_fields.PercentageField(
        title="Employment",
        review_title="Employment (Year 1 %)",
        max_digits=5,
        decimal_places=0,
        min_value=0,
    )
    alloc_education_y1 = acf_fields.PercentageField(
        title="Childcare, Early Childhood, Youth Development & Adult Education",
        review_title="Education and Youth Development (Year 1 %)",
        max_digits=5,
        decimal_places=0,
        min_value=0,
    )
    alloc_income_y1 = acf_fields.PercentageField(
        title="Income & Asset Building",
        review_title="Income and Asset Building (Year 1 %)",
        max_digits=5,
        decimal_places=0,
        min_value=0,
    )
    alloc_housing_y1 = acf_fields.PercentageField(
        title="Housing",
        review_title="Housing (Year 1 %)",
        max_digits=5,
        decimal_places=0,
        min_value=0,
    )
    alloc_health_y1 = acf_fields.PercentageField(
        title="Health & Nutrition",
        review_title="Health and Nutrition (Year 1 %)",
        max_digits=5,
        decimal_places=0,
        min_value=0,
    )
    alloc_civic_y1 = acf_fields.PercentageField(
        title="Civic Engagement & Community Involvement",
        review_title="Civic Engagement and Community Involvement (Year 1 %)",
        max_digits=5,
        decimal_places=0,
        min_value=0,
    )
    alloc_transportation_y1 = acf_fields.PercentageField(
        title="Transportation",
        review_title="Transportation (Year 1 %)",
        max_digits=5,
        decimal_places=0,
        min_value=0,
    )
    alloc_partnerships_y1 = acf_fields.PercentageField(
        title="Partnerships, Linkages & Coordination",
        review_title="Partnerships, Linkages, and Service Coordination (Year 1 %)",
        max_digits=5,
        decimal_places=0,
        min_value=0,
    )
    alloc_total_y1 = acf_fields.CalculatedPercentageField(
        title="Total (auto-calculated)",
        review_title="Year 1 Total (%)",
        fields=_Y1_ALLOCATION_FIELDS,
        max_digits=5,
        decimal_places=0,
        max_value=100,
        error_messages={"max_value": "Exceeds 100%%. Adjust so it adds up to 100%%."},
    )

    # 5.1 Year 2 Allocations (conditional on two-year plan; must total 100%)
    alloc_admin_y2 = acf_fields.PercentageField(
        title="Administrative cost",
        review_title="Administrative Funds (Year 2 %)",
        max_digits=5,
        decimal_places=0,
        min_value=0,
        max_value=5,
        required=False,
        error_messages={"max_value": "Cannot exceed 5%%"},
    )
    alloc_employment_y2 = acf_fields.PercentageField(
        title="Employment",
        review_title="Employment (Year 2 %)",
        max_digits=5,
        decimal_places=0,
        min_value=0,
        required=False,
    )
    alloc_education_y2 = acf_fields.PercentageField(
        title="Childcare, Early Childhood, Youth Development & Adult Education",
        review_title="Education and Youth Development (Year 2 %)",
        max_digits=5,
        decimal_places=0,
        min_value=0,
        required=False,
    )
    alloc_income_y2 = acf_fields.PercentageField(
        title="Income & Asset Building",
        review_title="Income and Asset Building (Year 2 %)",
        max_digits=5,
        decimal_places=0,
        min_value=0,
        required=False,
    )
    alloc_housing_y2 = acf_fields.PercentageField(
        title="Housing",
        review_title="Housing (Year 2 %)",
        max_digits=5,
        decimal_places=0,
        min_value=0,
        required=False,
    )
    alloc_health_y2 = acf_fields.PercentageField(
        title="Health & Nutrition",
        review_title="Health and Nutrition (Year 2 %)",
        max_digits=5,
        decimal_places=0,
        min_value=0,
        required=False,
    )
    alloc_civic_y2 = acf_fields.PercentageField(
        title="Civic Engagement & Community Involvement",
        review_title="Civic Engagement and Community Involvement (Year 2 %)",
        max_digits=5,
        decimal_places=0,
        min_value=0,
        required=False,
    )
    alloc_transportation_y2 = acf_fields.PercentageField(
        title="Transportation",
        review_title="Transportation (Year 2 %)",
        max_digits=5,
        decimal_places=0,
        min_value=0,
        required=False,
    )
    alloc_partnerships_y2 = acf_fields.PercentageField(
        title="Partnerships, Linkages & Coordination",
        review_title="Partnerships, Linkages, and Service Coordination (Year 2 %)",
        max_digits=5,
        decimal_places=0,
        min_value=0,
        required=False,
    )
    alloc_total_y2 = acf_fields.CalculatedPercentageField(
        title="Total (auto-calculated)",
        review_title="Year 2 Total (%)",
        fields=_Y2_ALLOCATION_FIELDS,
        max_digits=5,
        decimal_places=0,
        max_value=100,
        error_messages={"max_value": "Exceeds 100%%. Adjust so it adds up to 100%%."},
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
        required=False,
    )
    audit_date = acf_fields.DateField(
        title="Date of audit",
        required=False,
        widget=DatePickerInput(),
    )
    audit_period_start = acf_fields.DateField(
        title="Period start",
        required=False,
        widget=DatePickerInput(),
    )
    audit_period_end = acf_fields.DateField(
        title="Period end",
        required=False,
        widget=DatePickerInput(),
    )

    # endregion

    # region Section 6 — Individual Eligibility and Community Eligibility

    # 6.1
    individual_eligibility = acf_fields.TextareaField(
        title="Description",
        description="5000 characters allowed.",
        max_length=5000,
    )

    # 6.2
    community_eligibility = acf_fields.TextareaField(
        title="Description",
        description="5000 characters allowed.",
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
            "I have reviewed the CSBG Assurances above and affirm that the Tribe or "
            "Tribal Organization will ensure compliance with these assurances"
        ),
    )
    assurance_signature = acf_fields.CharField(
        title="Authorized Tribal Official Signature",
        description="Type in your full name as part of this signature",
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
        description="Type in your full name as part of this signature",
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
        description="Type in your full name as part of this signature",
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
        description="Type in your full name as part of this signature",
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
        description="Type in your full name as part of this signature",
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
        has_completed_single_audit = cleaned_data.get("has_completed_single_audit")

        # 1.2b: Multi-tribe names and tribal resolution upload are required when
        # representing more than one tribe.
        if is_multi_tribe == "yes":
            if not cleaned_data.get("multi_tribe_names"):
                self.add_error("multi_tribe_names", "This field is required.")
            if not cleaned_data.get("tribal_resolution_upload"):
                self.add_error("tribal_resolution_upload", "This field is required.")

        # 1.5: Additional Authorized Official fields are required when delegating authority.
        if has_delegation == "yes":
            for field_name in [
                "delegation_name",
                "delegation_title",
                "delegation_phone",
                "delegation_email",
            ]:
                if not cleaned_data.get(field_name):
                    self.add_error(field_name, "This field is required.")

        # 2.2b: When tribes have recognition, the user must pick a provision method and
        # provide the corresponding citation or upload.
        if has_recognition == "yes":
            provision_method = cleaned_data.get("recognition_provision_method")
            if not provision_method:
                self.add_error("recognition_provision_method", "This field is required.")
            elif provision_method == "manual" and not cleaned_data.get("recognition_citation"):
                self.add_error("recognition_citation", "This field is required.")
            elif provision_method == "upload" and not cleaned_data.get("recognition_upload"):
                self.add_error("recognition_upload", "This field is required.")

        # 5.3: Audit dates are required when the applicant reports completing a Single Audit.
        if has_completed_single_audit == "yes":
            for field_name in [
                "audit_date",
                "audit_period_start",
                "audit_period_end",
            ]:
                if not cleaned_data.get(field_name):
                    self.add_error(field_name, "This field is required.")

        # Year 2 allocations: required when a two-year plan is selected.
        if plan_coverage == "two_year":
            for field_name in _Y2_ALLOCATION_FIELDS:
                if cleaned_data.get(field_name) is None:
                    self.add_error(field_name, "This field is required.")

        # 5.1: Year 1 allocation total must equal 100%.
        y1_values = [cleaned_data.get(f) for f in _Y1_ALLOCATION_FIELDS]
        if all(v is not None for v in y1_values):
            y1_total = sum(Decimal(str(v)) for v in y1_values)
            if y1_total > Decimal("100"):
                self.add_error(
                    "alloc_total_y1",
                    "Exceeds 100%. Adjust so it adds up to 100%.",
                )
            elif y1_total < Decimal("100"):
                self.add_error("alloc_total_y1", "Total must equal 100%")

        # 5.1: Year 2 allocation total must equal 100% when a two-year plan is selected.
        if plan_coverage == "two_year":
            y2_values = [cleaned_data.get(f) for f in _Y2_ALLOCATION_FIELDS]
            if all(v is not None for v in y2_values):
                y2_total = sum(Decimal(str(v)) for v in y2_values)
                if y2_total > Decimal("100"):
                    self.add_error(
                        "alloc_total_y2",
                        "Exceeds 100%. Adjust so it adds up to 100%.",
                    )
                elif y2_total < Decimal("100"):
                    self.add_error("alloc_total_y2", "Total must equal 100%")

        return cleaned_data
