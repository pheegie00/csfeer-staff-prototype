from form_manager.schema.layout import PageBlock, PageTitleBlock, StepBlock
from form_manager.schema.navigation import build_side_nav_items


def test_build_side_nav_items_marks_current_step_page_and_review_state():
    steps = [
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

    side_nav_items = build_side_nav_items(
        steps,
        current_step_number=1,
        current_page_number=0,
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

    assert review_item["label"] == "Review & Submit"
    assert review_item["is_current"] is False

    review_nav_items = build_side_nav_items(steps, is_review=True)

    assert review_nav_items[-1]["is_current"] is True
    assert all(item["is_current"] is False for item in review_nav_items[:-1])
    assert all(item["is_expanded"] is False for item in review_nav_items[:-1])
