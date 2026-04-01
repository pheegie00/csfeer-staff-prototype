from typing import cast

import pytest

from form_manager.constants import CSBGAnnualReportForms
from form_manager.schema.forms.tribal_long_form import TribalLongForm
from form_manager.schema.forms.tribal_short_form import TribalShortForm
from form_manager.schema.layout import StepBlock
from form_manager.views.form_sidenav import (
    remove_nodes_with_excluded_fields,
    resolve_form_edit_destination,
    uses_form_sidenav,
)

DETAIL_DESCRIPTION_FIELDS = [
    "employment_related_services_description",
    "education_related_service_description",
    "income_services_description",
    "housing_services_description",
    "health_services_description",
    "civic_services_description",
    "transportation_services_description",
]


def get_filtered_steps(schema_cls, fields_to_exclude: list[str]):
    schema = schema_cls.model_construct()
    ui_components = cast(list[StepBlock], [step.model_copy(deep=True) for step in schema.ui])
    return remove_nodes_with_excluded_fields(ui_components, fields_to_exclude)


@pytest.mark.parametrize("schema_cls", [TribalShortForm, TribalLongForm])
def test_resolve_form_edit_destination_falls_back_to_first_visible_page_in_step(schema_cls):
    fields_to_exclude = [
        field_name
        for field_name in DETAIL_DESCRIPTION_FIELDS
        if field_name != "employment_related_services_description"
    ]
    steps = get_filtered_steps(schema_cls, fields_to_exclude)

    assert resolve_form_edit_destination(steps, 2, 1) == (2, 0)


@pytest.mark.parametrize("schema_cls", [TribalShortForm, TribalLongForm])
def test_resolve_form_edit_destination_falls_back_to_previous_visible_step_when_empty(schema_cls):
    steps = get_filtered_steps(schema_cls, DETAIL_DESCRIPTION_FIELDS)

    assert resolve_form_edit_destination(steps, 2, 0) == (1, 0)


@pytest.mark.parametrize(
    ("form_name", "expected"),
    [
        (CSBGAnnualReportForms.TRIBAL_ANNUAL_REPORT_3_0, True),
        (CSBGAnnualReportForms.TRIBAL_ANNUAL_REPORT_3_0_SHORT, True),
        (CSBGAnnualReportForms.STATES_ANNUAL_REPORT_3_0, False),
    ],
)
def test_uses_form_sidenav(form_name: str, expected: bool):
    assert uses_form_sidenav(form_name) is expected
