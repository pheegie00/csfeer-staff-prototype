from typing import cast

from form_manager.schema.forms.tribal_short_form import TribalShortForm
from form_manager.schema.layout import StepBlock
from form_manager.views.short_form_navigation import (
    remove_nodes_with_excluded_fields,
    resolve_short_form_edit_destination,
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


def get_filtered_short_form_steps(fields_to_exclude: list[str]):
    schema = TribalShortForm.model_construct()
    ui_components = cast(list[StepBlock], [step.model_copy(deep=True) for step in schema.ui])
    return remove_nodes_with_excluded_fields(ui_components, fields_to_exclude)


def test_resolve_short_form_edit_destination_falls_back_to_first_visible_page_in_step():
    fields_to_exclude = [
        field_name
        for field_name in DETAIL_DESCRIPTION_FIELDS
        if field_name != "employment_related_services_description"
    ]
    steps = get_filtered_short_form_steps(fields_to_exclude)

    assert resolve_short_form_edit_destination(steps, 2, 1) == (2, 0)


def test_resolve_short_form_edit_destination_falls_back_to_previous_visible_step_when_empty():
    steps = get_filtered_short_form_steps(DETAIL_DESCRIPTION_FIELDS)

    assert resolve_short_form_edit_destination(steps, 2, 0) == (1, 0)
