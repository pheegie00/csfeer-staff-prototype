import uuid

import pytest
from django.urls import reverse

from form_manager.schema.layout import PageBlock, PageTitleBlock, StepBlock
from form_manager.schema.navigation import build_form_edit_url, build_side_nav_items
from form_manager.views.form_edit import get_next_step_and_page, get_previous_step_and_page


@pytest.fixture
def entry_pk():
    return uuid.uuid4()


@pytest.fixture
def steps():
    return [
        StepBlock(
            title="Basic Information",
            children=[
                PageBlock(title="Your basic information"),
            ],
        ),
        StepBlock(
            title="Expenditure categories",
            children=[
                PageBlock(children=[PageTitleBlock(title="Category selection")]),
                PageBlock(title="Administration costs"),
            ],
        ),
    ]


@pytest.mark.django_db
def test_build_side_nav_items_marks_current_step_page_and_review_state(steps, entry_pk):
    side_nav_items = build_side_nav_items(
        steps,
        current_step_number=1,
        current_page_number=0,
        entry_pk=entry_pk,
    )

    assert len(side_nav_items) == 3

    first_step = side_nav_items[0]
    current_step = side_nav_items[1]
    review_item = side_nav_items[2]

    assert first_step["label"] == "Section 1: Basic Information"
    assert first_step["is_current"] is False
    assert first_step["is_expanded"] is False

    assert current_step["label"] == "Section 2: Expenditure categories"
    assert current_step["is_current"] is True
    assert current_step["is_expanded"] is True
    assert current_step["pages"][0]["label"] == "Category selection"
    assert current_step["pages"][0]["is_current"] is True
    assert current_step["pages"][1]["label"] == "Administration costs"
    assert current_step["pages"][1]["is_current"] is False

    assert review_item["label"] == "Review and Submit"
    assert review_item["is_current"] is False

    review_nav_items = build_side_nav_items(steps, is_review=True, entry_pk=entry_pk)

    assert review_nav_items[-1]["is_current"] is True
    assert all(item["is_current"] is False for item in review_nav_items[:-1])
    assert all(item["is_expanded"] is False for item in review_nav_items[:-1])


@pytest.mark.django_db
def test_build_side_nav_items_builds_real_urls(steps, entry_pk):
    review_url = reverse("form_review", kwargs={"pk": entry_pk})

    side_nav_items = build_side_nav_items(
        steps,
        current_step_number=1,
        current_page_number=0,
        entry_pk=entry_pk,
    )

    # Section 1 links to its first child page (step=0, page=0)
    assert side_nav_items[0]["href"] == build_form_edit_url(entry_pk, step_number=0, page_number=0)
    assert side_nav_items[0]["pages"][0]["href"] == build_form_edit_url(
        entry_pk, step_number=0, page_number=0
    )

    # Section 2 links to its first child page (step=1, page=0)
    assert side_nav_items[1]["href"] == build_form_edit_url(entry_pk, step_number=1, page_number=0)
    assert side_nav_items[1]["pages"][0]["href"] == build_form_edit_url(
        entry_pk, step_number=1, page_number=0
    )
    assert side_nav_items[1]["pages"][1]["href"] == build_form_edit_url(
        entry_pk, step_number=1, page_number=1
    )

    # Review and Submit links to the review URL
    assert side_nav_items[2]["href"] == review_url


@pytest.mark.django_db
def test_build_side_nav_items_review_state_has_real_urls(steps, entry_pk):
    review_url = reverse("form_review", kwargs={"pk": entry_pk})

    side_nav_items = build_side_nav_items(steps, is_review=True, entry_pk=entry_pk)

    assert side_nav_items[0]["href"] == build_form_edit_url(entry_pk, step_number=0, page_number=0)
    assert side_nav_items[1]["href"] == build_form_edit_url(entry_pk, step_number=1, page_number=0)
    assert side_nav_items[-1]["href"] == review_url


@pytest.fixture
def steps_with_empty_middle():
    return [
        StepBlock(
            title="Section 1",
            children=[PageBlock(title="Page 1")],
        ),
        StepBlock(
            title="Section 2 (empty)",
            children=[],
        ),
        StepBlock(
            title="Section 3",
            children=[PageBlock(title="Page 3")],
        ),
    ]


def test_get_next_step_skips_empty_steps(steps_with_empty_middle):
    # From section 1 last page, should skip empty section 2 and land on section 3
    assert get_next_step_and_page(steps_with_empty_middle, 0, 0) == (2, 0)


def test_get_next_step_goes_to_review_when_all_remaining_empty():
    steps = [
        StepBlock(title="S1", children=[PageBlock(title="P1")]),
        StepBlock(title="S2 empty", children=[]),
    ]
    assert get_next_step_and_page(steps, 0, 0) == (None, None)


def test_get_previous_step_skips_empty_steps(steps_with_empty_middle):
    # From section 3 first page, should skip empty section 2 and land on section 1 last page
    assert get_previous_step_and_page(steps_with_empty_middle, 2, 0) == (0, 0)


def test_get_previous_step_returns_none_when_all_previous_empty():
    steps = [
        StepBlock(title="S1 empty", children=[]),
        StepBlock(title="S2", children=[PageBlock(title="P1")]),
    ]
    assert get_previous_step_and_page(steps, 1, 0) == (None, None)
