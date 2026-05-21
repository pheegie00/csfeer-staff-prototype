import itertools

from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class FormFamilies(TextChoices):
    """A form family represents a collection of forms
    approved under the Paperwork Reduction Act. Such
    collections are assigned an OMB control number.

    Find the official names of OMB numbers here: https://www.reginfo.gov/public/do/PRASearch

    SCALING NOTE: Currently CSBG-only. When adding new ACF programs
    (TANF, Tribal TANF, HMRF, HPOG -- see docs/multi_program_architecture.md
    and STAFF-MP-10 in docs/backlog.md), add sibling enum entries here.
    """

    # --- CSBG (OCS) ---
    CSBG_ANNUAL_REPORT = "0970-0492", _("CSBG Annual Report")
    CSBG_TRIBAL_PLAN_APPLICATION = "0970-0635", _("CSBG Model Tribal Plan Applications")
    # Phase II per PWS (D01 FA - Attachment 1 - PWS CSFEER_v2.pdf, p9):
    CSBG_STATE_TERRITORY_PLAN = "0970-0382", _("CSBG State and Territory Plan")
    CSBG_ELIGIBLE_ENTITY_LIST = "0970-0408", _("CSBG Eligible Entity List")

    # --- Other OCS programs (sample data for multi-program prototype) ---
    LIHEAP_FAMILY = "0970-0080", _("LIHEAP Performance Data Form")
    LIHWAP_FAMILY = "0970-0567", _("LIHWAP Performance Data Form")
    AFI_FAMILY = "0970-0202", _("Assets for Independence (AFI) Annual Report")
    CED_FAMILY = "0970-0386", _("Community Economic Development (CED) Performance Report")
    SSBG_FAMILY = "0970-0234", _("SSBG Annual Report (SF-PPR)")
    RCD_FAMILY = "0970-RCD", _("Rural Community Development Performance Report")

    # TODO STAFF-MP-10: TANF financial / data / MOE families
    # TODO STAFF-MP-11: SF-424 (shared standard federal application)


# ============================================================
# CSBG (already shipped)
# ============================================================

class CSBGAnnualReportForms(TextChoices):
    """Forms approved under OMB control no. 0970-0492 (CSBG Annual Report)."""

    ENTITIES_ANNUAL_REPORT_2_1 = "CSBG Annual Report 2.1 (Eligible Entities)"
    STATES_ANNUAL_REPORT_2_1 = "CSBG Annual Report 2.1 (States)"
    ENTITITES_ANNUAL_REPORT_3_0 = "CSBG Annual Report 3.0 (Eligible Entities)"
    STATES_ANNUAL_REPORT_3_0 = "CSBG Annual Report 3.0 (States)"
    TRIBAL_ANNUAL_REPORT_3_0 = "CSBG Annual Report 3.0 Tribal Annual Report (Tribes)"
    TRIBAL_ANNUAL_REPORT_3_0_SHORT = "CSBG Annual Report 3.0 Tribal Short Form (Tribes)"


class CSBGTribalPlanApplicationForms(TextChoices):
    """Forms approved under OMB control no. 0970-0635 (CSBG Tribal Plan)."""

    CSBG_TRIBAL_PLAN = "CSBG Model Tribal Plan"


class CSBGStateTerritoryPlanForms(TextChoices):
    """Phase II per PWS p9 -- CSBG State and Territory Plan."""

    CSBG_STATE_PLAN = "CSBG State Plan"
    CSBG_TERRITORY_PLAN = "CSBG Territory Plan"


class CSBGEligibleEntityListForms(TextChoices):
    """Phase II per PWS p9 -- CSBG Eligible Entity List."""

    CSBG_ELIGIBLE_ENTITY_LIST = "CSBG Eligible Entity List"


# ============================================================
# Other OCS programs (sample forms, schema TBD pending design)
# ============================================================

class LIHEAPForms(TextChoices):
    """Low Income Home Energy Assistance Program. OMB 0970-0080.

    Schema is placeholder pending Figma design (referenced from CSBG
    Tribal Plan design pattern -- navy + green USWDS-adjacent, section-
    based, recipient + AO signatures).
    """
    LIHEAP_MODEL_PLAN = "LIHEAP Model State / Tribal Plan"
    LIHEAP_PERFORMANCE_DATA_FORM = "LIHEAP Performance Data Form"
    LIHEAP_HOUSEHOLD_REPORT = "LIHEAP Household Report"


class LIHWAPForms(TextChoices):
    """Low Income Household Water Assistance Program. OMB 0970-0567."""
    LIHWAP_PERFORMANCE_DATA_FORM = "LIHWAP Performance Data Form"
    LIHWAP_QUARTERLY_DRAWDOWN = "LIHWAP Quarterly Drawdown Report"


class AFIForms(TextChoices):
    """Assets for Independence. OMB 0970-0202 (program is dormant
    but historical reports may still be reviewed)."""
    AFI_ANNUAL_REPORT = "AFI Annual Report"
    AFI_PROJECT_APPLICATION = "AFI Project Application"


class CEDForms(TextChoices):
    """Community Economic Development. OMB 0970-0386."""
    CED_APPLICATION = "CED Project Application"
    CED_PERFORMANCE_PROGRESS_REPORT = "CED Performance Progress Report"
    CED_FINAL_PERFORMANCE_REPORT = "CED Final Performance Report"


class RCDForms(TextChoices):
    """Rural Community Development. OMB-RCD (placeholder)."""
    RCD_APPLICATION = "RCD Project Application"
    RCD_PERFORMANCE_REPORT = "RCD Annual Performance Report"


class SSBGForms(TextChoices):
    """Social Services Block Grant. OMB 0970-0234."""
    SSBG_ANNUAL_REPORT = "SSBG Annual Report (SF-PPR)"
    SSBG_PRE_EXPENDITURE_REPORT = "SSBG Pre-Expenditure Report"


# ============================================================
# Aggregated choices for FormDefinition.name field
# ============================================================

ALL_FORM_NAME_CHOICES = list(itertools.chain(
    CSBGAnnualReportForms.choices,
    CSBGTribalPlanApplicationForms.choices,
    CSBGStateTerritoryPlanForms.choices,
    CSBGEligibleEntityListForms.choices,
    LIHEAPForms.choices,
    LIHWAPForms.choices,
    AFIForms.choices,
    CEDForms.choices,
    RCDForms.choices,
    SSBGForms.choices,
))

type AllFormNames = (
    CSBGAnnualReportForms | CSBGTribalPlanApplicationForms |
    CSBGStateTerritoryPlanForms | CSBGEligibleEntityListForms |
    LIHEAPForms | LIHWAPForms | AFIForms | CEDForms | RCDForms | SSBGForms
)
