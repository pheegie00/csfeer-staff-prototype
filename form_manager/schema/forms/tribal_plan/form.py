"""UI layout definition for the CSBG Tribal Plan form."""

from pydantic import ConfigDict, Field
from pydantic_extra_types.semantic_version import SemanticVersion

from form_manager.constants import AllFormNames, CSBGTribalPlanApplicationForms, FormFamilies
from form_manager.schema.forms.base import BaseFormSchema, UIDefinition
from form_manager.schema.forms.tribal_plan.fields import TribalPlanFormFields
from form_manager.schema.forms.tribal_plan.texts import (
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
    ConditionalBlock,
    FieldBlock,
    FieldGroupBlock,
    PermanentPageBlock,
    ReviewSubheadingBlock,
    SectionBlock,
    StepBlock,
    TextBlock,
)


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
                        children=[
                            SectionBlock(
                                title="Delegation of Authority",
                                alpine_controller_field="has_delegation",
                                children=[
                                    ReviewSubheadingBlock(title="Delegation of Authority"),
                                    FieldBlock(field_name="has_delegation"),
                                    ConditionalBlock(
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
                                title="Tribal Recognition",
                                alpine_controller_field="has_recognition",
                                children=[
                                    ReviewSubheadingBlock(title="Tribal Recognition"),
                                    FieldBlock(field_name="has_recognition"),
                                    ConditionalBlock(
                                        show_when="yes",
                                        children=[
                                            FieldBlock(field_name="recognition_citation"),
                                            FieldBlock(field_name="recognition_upload"),
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
