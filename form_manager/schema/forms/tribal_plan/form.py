"""UI layout definition for the CSBG Tribal Plan form."""

from datetime import date

from pydantic import ConfigDict, Field
from pydantic_extra_types.semantic_version import SemanticVersion

from form_manager.constants import AllFormNames, CSBGTribalPlanApplicationForms, FormFamilies
from form_manager.schema.forms.base import BaseFormSchema, UIDefinition
from form_manager.schema.forms.tribal_plan.fields import TribalPlanFormFields
from form_manager.schema.forms.tribal_plan.texts import (
    _DEBARMENT_CERTIFICATION_TEXT,
    _DEBARMENT_LOWER_TIER_INSTRUCTIONS_TEXT,
    _DEBARMENT_PRIMARY_INSTRUCTIONS_TEXT,
    _DRUG_FREE_WORKPLACE_CERTIFICATION_TEXT,
    _DRUG_FREE_WORKPLACE_INSTRUCTIONS_TEXT,
    _LIMITATION_ON_USE_OF_FUNDS_TEXT,
    _LOBBYING_CERTIFICATION_TEXT,
    _SINGLE_AUDIT_REQUIREMENTS_TEXT,
    _TOBACCO_SMOKE_CERTIFICATION_TEXT,
)
from form_manager.schema.layout import (
    AccordionBlock,
    AccordionItem,
    AlertBoxBlock,
    CardBlock,
    CardGroupBlock,
    ConditionalBlock,
    DateRangePickerBlock,
    FieldBlock,
    PermanentPageBlock,
    ReviewSubheadingBlock,
    SectionBlock,
    StepBlock,
    TextBlock,
)

_TODAY = date.today()
_NEXT_FY = (_TODAY.year + 1 if _TODAY.month >= 10 else _TODAY.year) + 1
_Y1_DATE_RANGE = f"October 1, {_NEXT_FY - 1} - Sept 30, {_NEXT_FY}"
_Y2_DATE_RANGE = f"October 1, {_NEXT_FY} - Sept 30, {_NEXT_FY + 1}"


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
                            AlertBoxBlock(
                                alert_type="info",
                                message=(
                                    "Tribal Plans covering a two-year period are strongly"
                                    " recommended to minimize administrative burden for"
                                    " grant recipients."
                                ),
                                slim=True,
                            ),
                            SectionBlock(
                                alpine_controller_field="plan_coverage",
                                children=[
                                    ReviewSubheadingBlock(title="Plan Coverage"),
                                    FieldBlock(field_name="plan_coverage"),
                                    ConditionalBlock(
                                        show_when=["one_year", "two_year"],
                                        children=[FieldBlock(field_name="fiscal_year_y1")],
                                    ),
                                    ConditionalBlock(
                                        show_when="two_year",
                                        children=[FieldBlock(field_name="fiscal_year_y2")],
                                    ),
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
                                alpine_controller_field="is_multi_tribe",
                                children=[
                                    ReviewSubheadingBlock(title="Tribal Representation"),
                                    FieldBlock(field_name="is_multi_tribe"),
                                    ConditionalBlock(
                                        show_when="yes",
                                        children=[
                                            FieldBlock(field_name="multi_tribe_names"),
                                            FieldBlock(field_name="tribal_resolution_upload"),
                                        ],
                                    ),
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
                            "Delegation of authority may include granting signature authority"
                            " for assurances, certifications, and other required CSBG documents"
                            " on behalf of the Authorized Tribal Official."
                        ),
                        children=[
                            SectionBlock(
                                alpine_controller_field="has_delegation",
                                children=[
                                    ReviewSubheadingBlock(title="Delegation of Authority"),
                                    FieldBlock(field_name="has_delegation"),
                                    ConditionalBlock(
                                        title="Additional Authorized Official",
                                        show_when="yes",
                                        children=[
                                            ReviewSubheadingBlock(
                                                title="Additional Authorized Official"
                                            ),
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
                                alpine_controller_field="has_recognition",
                                children=[
                                    ReviewSubheadingBlock(title="Tribal Recognition"),
                                    FieldBlock(field_name="has_recognition"),
                                    ConditionalBlock(
                                        show_when="yes",
                                        children=[
                                            SectionBlock(
                                                alpine_controller_field=(
                                                    "recognition_provision_method"
                                                ),
                                                children=[
                                                    FieldBlock(
                                                        field_name="recognition_provision_method"
                                                    ),
                                                    ConditionalBlock(
                                                        show_when="manual",
                                                        children=[
                                                            FieldBlock(
                                                                field_name="recognition_citation"
                                                            ),
                                                        ],
                                                    ),
                                                    ConditionalBlock(
                                                        show_when="upload",
                                                        children=[
                                                            FieldBlock(
                                                                field_name="recognition_upload"
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
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
                            "Briefly describe the Tribe or Tribal Organization's"
                            " CSBG-specific goals and objectives for the"
                            " Community Services Block Grant funding, as applicable."
                        ),
                        children=[
                            AlertBoxBlock(
                                alert_type="info",
                                message=(
                                    "Consider how your Tribe or Tribal Organization's goals"
                                    " and objectives align with the purposes of the CSBG"
                                    " program, including: removing obstacles that block the"
                                    " achievement of self-sufficiency; securing and retaining"
                                    " meaningful employment; attaining adequate literacy and"
                                    " education; making better use of available income;"
                                    " obtaining and maintaining adequate housing; obtaining"
                                    " emergency assistance; achieving greater participation in"
                                    " the affairs of the communities; supporting youth"
                                    " development in low-income communities; coordinating with"
                                    " other programs related to the purposes of the CSBG Act;"
                                    " and linkages to fill service gaps."
                                ),
                            ),
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
                                        review_template_name=(
                                            "form_manager/forms/yes_no_display_review.html"
                                        ),
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
                        children=[
                            AlertBoxBlock(
                                alert_type="info",
                                heading="Allocation requirements for CSBG funds",
                                message=(
                                    "According to the CSBG Act, no more than 5% of funds"
                                    " may be used for administrative costs and at least 95%"
                                    " of funds must be allocated to program services."
                                    " For program funds, enter the percentage allocated to"
                                    " each CSBG service area. The total must equal 100%."
                                ),
                            ),
                            CardGroupBlock(
                                children=[
                                    CardBlock(
                                        title="Year one",
                                        subtitle=_Y1_DATE_RANGE,
                                        show_when_field="plan_coverage",
                                        show_when_value=["one_year", "two_year"],
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
                                    CardBlock(
                                        title="Year two",
                                        subtitle=_Y2_DATE_RANGE,
                                        show_when_field="plan_coverage",
                                        show_when_value="two_year",
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
                        ],
                    ),
                    PermanentPageBlock(
                        title="Limitation on Use of Funds",
                        subtitle=(
                            "Review the requirement below and select the checkbox"
                            " to confirm compliance."
                        ),
                        children=[
                            TextBlock(
                                heading="Limitation on the Use of Funds",
                                text=_LIMITATION_ON_USE_OF_FUNDS_TEXT,
                                template_name="form_manager/use_of_funds_notice.html",
                            ),
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Limitation on Use of Funds"),
                                    FieldBlock(field_name="use_of_funds_acknowledgment"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Single Audit Review",
                        subtitle=(
                            "Provide the date and time period covered by your most recent audit,"
                            " if applicable."
                        ),
                        children=[
                            AlertBoxBlock(
                                alert_type="info",
                                heading="Single Audit requirements",
                                message=_SINGLE_AUDIT_REQUIREMENTS_TEXT,
                            ),
                            SectionBlock(
                                alpine_controller_field="has_completed_single_audit",
                                children=[
                                    ReviewSubheadingBlock(title="Single Audit Review"),
                                    FieldBlock(field_name="has_completed_single_audit"),
                                    ConditionalBlock(
                                        show_when="yes",
                                        children=[
                                            FieldBlock(field_name="audit_date"),
                                            DateRangePickerBlock(
                                                children=[
                                                    FieldBlock(field_name="audit_period_start"),
                                                    FieldBlock(field_name="audit_period_end"),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Step 6: Section 6 — Individual & Community Eligibility
            StepBlock(
                title="Individual & Community Eligibility",
                children=[
                    PermanentPageBlock(
                        title="Individual Eligibility",
                        subtitle=(
                            "Describe policies and procedures for determining eligibility for "
                            "individual services, including policies and procedures when "
                            "individual income verification is not possible or practical."
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
                        title="Community Eligibility",
                        subtitle=(
                            "For those services that provide a community-wide benefit, "
                            "describe how the tribe or tribal organization ensures that "
                            "services target and benefit communities with low income."
                        ),
                        children=[
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Community Eligibility"),
                                    FieldBlock(field_name="community_eligibility"),
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
                            "Provide a narrative description of how the tribe or tribal"
                            " organization will carry out the required programmatic assurances."
                        ),
                        children=[
                            AlertBoxBlock(
                                alert_type="info",
                                heading="Programmatic assurances topics",
                                message="",
                                template_name=(
                                    "form_manager/content_blocks/programmatic_assurances_alert.html"
                                ),
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
                        submit_permissions=[
                            "form_manager.form_tribal_plan_can_sign_authorized_official"
                        ],
                        title="Statement of Assurances",
                        subtitle=(
                            "Review the certification below and sign at the bottom of this page"
                            " to affirm compliance."
                        ),
                        children=[
                            TextBlock(
                                text="",
                                template_name="form_manager/legislation_link.html",
                            ),
                            TextBlock(
                                text="",
                                template_name="form_manager/content_blocks/csbg_assurances_narrative.html",
                            ),
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Statement of Assurances"),
                                    FieldBlock(field_name="assurance_attestation"),
                                    FieldBlock(field_name="assurance_signature"),
                                ],
                            ),
                            AlertBoxBlock(
                                alert_type="warning",
                                heading="Only an authorized official can complete this section",
                                message=(
                                    "Your changes will not be saved. Contact your organization's "
                                    "Authorized Official to complete and sign this page."
                                ),
                                render_when=lambda ctx: not ctx.get("page_permissions_met"),
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
                        submit_permissions=[
                            "form_manager.form_tribal_plan_can_sign_authorized_official"
                        ],
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
                            AlertBoxBlock(
                                alert_type="warning",
                                heading="Only an authorized official can complete this section",
                                message=(
                                    "Your changes will not be saved. Contact your organization's "
                                    "Authorized Official to complete and sign this page."
                                ),
                                render_when=lambda ctx: not ctx.get("page_permissions_met"),
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Drug-Free Workplace Requirements",
                        subtitle=(
                            "Review the certification below and sign at the bottom of this page to "
                            "affirm compliance."
                        ),
                        submit_permissions=[
                            "form_manager.form_tribal_plan_can_sign_authorized_official"
                        ],
                        children=[
                            AccordionBlock(
                                bordered=True,
                                items=[
                                    AccordionItem(
                                        heading="Instructions for Certifications",
                                        text=_DRUG_FREE_WORKPLACE_INSTRUCTIONS_TEXT,
                                        is_expanded=False,
                                    )
                                ],
                            ),
                            TextBlock(
                                bordered=True,
                                heading="Drug-Free Workplace Certification",
                                text=_DRUG_FREE_WORKPLACE_CERTIFICATION_TEXT,
                            ),
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Drug-Free Workplace Requirements"),
                                    FieldBlock(field_name="drug_free_attestation"),
                                ],
                            ),
                            SectionBlock(
                                title="Place of performance",
                                description=(
                                    "The grant recipient may insert in the space provided"
                                    " below the site for the performance of work done in"
                                    " connection with the specific grant."
                                ),
                                children=[
                                    FieldBlock(field_name="drug_free_place_of_performance"),
                                    FieldBlock(
                                        field_name="drug_free_unidentified_workplaces",
                                        review_template_name=(
                                            "form_manager/forms/yes_no_display_review.html"
                                        ),
                                    ),
                                ],
                            ),
                            SectionBlock(
                                children=[
                                    FieldBlock(field_name="drug_free_signature"),
                                ],
                            ),
                            AlertBoxBlock(
                                alert_type="warning",
                                heading="Only an authorized official can complete this section",
                                message=(
                                    "Your changes will not be saved. Contact your organization's "
                                    "Authorized Official to complete and sign this page."
                                ),
                                render_when=lambda ctx: not ctx.get("page_permissions_met"),
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Debarment, Suspension and Other Responsibility Matters",
                        subtitle=(
                            "Review the certification below and sign at the bottom of this page to "
                            "affirm compliance."
                        ),
                        submit_permissions=[
                            "form_manager.form_tribal_plan_can_sign_authorized_official"
                        ],
                        children=[
                            AccordionBlock(
                                bordered=True,
                                items=[
                                    AccordionItem(
                                        heading=(
                                            "Instructions for Certifications"
                                            " - Primary Covered Transactions"
                                        ),
                                        text=_DEBARMENT_PRIMARY_INSTRUCTIONS_TEXT,
                                        is_expanded=False,
                                    ),
                                    AccordionItem(
                                        heading=(
                                            "Instructions for Certifications"
                                            " - Lower Tier Covered Transactions"
                                        ),
                                        text=_DEBARMENT_LOWER_TIER_INSTRUCTIONS_TEXT,
                                        is_expanded=False,
                                    ),
                                ],
                            ),
                            TextBlock(
                                bordered=True,
                                text=_DEBARMENT_CERTIFICATION_TEXT,
                            ),
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(
                                        title=(
                                            "Debarment, Suspension and Other"
                                            " Responsibility Matters"
                                        )
                                    ),
                                    FieldBlock(field_name="debarment_attestation"),
                                    FieldBlock(field_name="debarment_signature"),
                                ],
                            ),
                            AlertBoxBlock(
                                alert_type="warning",
                                heading="Only an authorized official can complete this section",
                                message=(
                                    "Your changes will not be saved. Contact your organization's "
                                    "Authorized Official to complete and sign this page."
                                ),
                                render_when=lambda ctx: not ctx.get("page_permissions_met"),
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Environmental Tobacco Smoke",
                        subtitle=(
                            "Review the certification below and sign at the bottom of this page to "
                            "affirm compliance."
                        ),
                        submit_permissions=[
                            "form_manager.form_tribal_plan_can_sign_authorized_official"
                        ],
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
                            AlertBoxBlock(
                                alert_type="warning",
                                heading="Only an authorized official can complete this section",
                                message=(
                                    "Your changes will not be saved. Contact your organization's "
                                    "Authorized Official to complete and sign this page."
                                ),
                                render_when=lambda ctx: not ctx.get("page_permissions_met"),
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    model_config = ConfigDict(use_enum_values=True)
