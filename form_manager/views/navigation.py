from typing import Any

from form_manager.schema.layout import PageTitleBlock


def _get_page_nav_label(page: Any, page_index: int) -> str:
    if page.title:
        return page.title

    for child in page.children or []:
        if isinstance(child, PageTitleBlock):
            return child.title

    return f"Page {page_index + 1}"


def build_side_nav_items(
    steps: list[Any],
    *,
    current_step_number: int | None = None,
    current_page_number: int | None = None,
    is_review: bool = False,
) -> list[dict[str, Any]]:
    side_nav_items: list[dict[str, Any]] = []

    for step_index, step in enumerate(steps):
        children = [
            {
                "kind": "page",
                "label": _get_page_nav_label(page, page_index),
                "href": "#",
                "is_current": (
                    not is_review
                    and step_index == current_step_number
                    and page_index == current_page_number
                ),
            }
            for page_index, page in enumerate(step.children or [])
        ]

        is_current = not is_review and step_index == current_step_number

        side_nav_items.append(
            {
                "kind": "section",
                "label": f"Section {step_index + 1}: {step.title}",
                "href": "#",
                "is_current": is_current,
                "is_expanded": is_current,
                "children": children,
            }
        )

    side_nav_items.append(
        {
            "kind": "review",
            "label": "Review & Submit",
            "href": "#",
            "is_current": is_review,
            "is_expanded": False,
            "children": [],
        }
    )

    return side_nav_items
