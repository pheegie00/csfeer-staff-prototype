import itertools

from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class FormFamilies(TextChoices):
    """A form family represents a collection of forms
    approved under the Paperwork Reduction Act. Such
    collections are assigned an OMB control number.

    Find the official names of OBM numbers here: https://www.reginfo.gov/public/do/PRASearch

    SCALING NOTE: Currently CSBG-only. When adding new ACF programs
    (TANF, Tribal TANF, HMRF, HPOG -- see docs/multi_program_architecture.md
    and STAFF-MP-10 in docs/backlog.md), add sibling enum entries here.
    """

    CSBG_ANNUAL_REPORT = "0970-0492", _("CSBG Annual Report")
    CSBG_TRIBAL_PLAN_APPLICATION = "0970-0635", _("CSBG Model Tribal Plan Applications")
    # TODO STAFF-MP-10: TANF financial / data / MOE families
    # TODO STAFF-MP-11: SF-424 (shared standard federal application)


class CSBGAnnualReportForms(TextChoices):
    """This enum represents names of forms approved under OMB control no. 0970-0492."""

    ENTITIES_ANNUAL_REPORT_2_1 = "CSBG Annual Report 2.1 (Eligible Entities)"
    STATES_ANNUAL_REPORT_2_1 = "CSBG Annual Report 2.1 (States)"
    ENTITITES_ANNUAL_REPORT_3_0 = "CSBG Annual Report 3.0 (Eligible Entities)"
    STATES_ANNUAL_REPORT_3_0 = "CSBG Annual Report 3.0 (States)"
    TRIBAL_ANNUAL_REPORT_3_0 = "CSBG Annual Report 3.0 Tribal Annual Report (Tribes)"
    TRIBAL_ANNUAL_REPORT_3_0_SHORT = "CSBG Annual Report 3.0 Tribal Short Form (Tribes)"


class CSBGTribalPlanApplicationForms(TextChoices):
    """This enum represents names of forms approved under OMB control no. 0970-0635."""

    CSBG_TRIBAL_PLAN = "CSBG Model Tribal Plan"


ALL_FORM_NAME_CHOICES = itertools.chain(
    CSBGAnnualReportForms.choices, CSBGTribalPlanApplicationForms.choices
)

type AllFormNames = CSBGAnnualReportForms | CSBGTribalPlanApplicationForms
