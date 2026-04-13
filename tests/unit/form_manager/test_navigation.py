import uuid

import pytest
from django.urls import reverse

from form_manager.schema.layout import PageBlock, PageTitleBlock, StepBlock
from form_manager.schema.navigation import build_form_edit_url, build_side_nav_items


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
