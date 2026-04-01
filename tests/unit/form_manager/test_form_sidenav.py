from types import SimpleNamespace
from uuid import uuid4
from typing import Any, cast

import pytest

from form_manager.constants import CSBGAnnualReportForms
from form_manager.schema.forms.tribal_long_form import TribalLongForm
from form_manager.schema.forms.tribal_short_form import TribalShortForm
from form_manager.schema.layout import StepBlock
from form_manager.views.form_sidenav import (
    build_form_sidenav_items,
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


def build_sidenav_items_for_test(
    steps: list[StepBlock], current_step_number: int, current_page_number: int
):
    entry = cast(Any, SimpleNamespace(pk=uuid4()))
    return build_form_sidenav_items(entry, steps, current_step_number, current_page_number)


@pytest.mark.parametrize("schema_cls", [TribalShortForm, TribalLongForm])
def test_build_form_sidenav_items_only_expands_current_section_marks_current_page_and_omits_hidden_pages(
    schema_cls,
):
    fields_to_exclude = [
        field_name
        for field_name in DETAIL_DESCRIPTION_FIELDS
        if field_name
        not in {
            "employment_related_services_description",
            "housing_services_description",
        }
    ]
    steps = get_filtered_steps(schema_cls, fields_to_exclude)

    sidenav_items = build_sidenav_items_for_test(steps, 2, 1)

    assert sidenav_items[2]["is_current"] is True
    assert [child["title"] for child in sidenav_items[2]["children"]] == [
        "Details on employment services",
        "Details on housing services",
    ]
    assert [child["is_current"] for child in sidenav_items[2]["children"]] == [False, True]

    collapsed_titles = [
        item["title"] for index, item in enumerate(sidenav_items[:-1]) if index != 2
    ]
    assert collapsed_titles
    assert all(
        item["children"] == [] for index, item in enumerate(sidenav_items[:-1]) if index != 2
    )
    assert all(
        item["is_current"] is False for index, item in enumerate(sidenav_items[:-1]) if index != 2
    )


def test_build_form_sidenav_items_keeps_duplicate_long_form_child_labels_unchanged():
    steps = get_filtered_steps(TribalLongForm, [])

    sidenav_items = build_sidenav_items_for_test(steps, 3, 1)

    assert [child["title"] for child in sidenav_items[3]["children"]] == [
        "Let's collect demographic details",
        "About the individuals served",
        "About the individuals served",
    ]


@pytest.mark.parametrize("schema_cls", [TribalShortForm, TribalLongForm])
def test_build_form_sidenav_items_marks_review_as_current_and_collapses_edit_sections_on_review(
    schema_cls,
):
    steps = get_filtered_steps(schema_cls, [])
    entry = cast(Any, SimpleNamespace(pk=uuid4()))

    sidenav_items = build_form_sidenav_items(
        entry,
        steps,
        0,
        0,
        is_review_page=True,
    )

    assert [item["title"] for item in sidenav_items[:-1]] == [step.title for step in steps]
    assert all(item["is_current"] is False for item in sidenav_items[:-1])
    assert all(item["children"] == [] for item in sidenav_items[:-1])
    assert sidenav_items[-1]["title"] == "Review and Submit"
    assert sidenav_items[-1]["is_current"] is True
    assert sidenav_items[-1]["children"] == []


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
