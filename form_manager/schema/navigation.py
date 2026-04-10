from typing import TypedDict

from form_manager.schema.layout import AbstractPageBlock, PageTitleBlock, StepBlock

PLACEHOLDER_HREF = "#"


class SideNavPage(TypedDict):
    kind: str
    label: str
    href: str
    is_current: bool


class SideNavSection(TypedDict):
    kind: str
    label: str
    href: str
    is_current: bool
    is_expanded: bool
    pages: list[SideNavPage]


def _get_page_nav_label(page: AbstractPageBlock, page_index: int) -> str:
    if page.title:
        return page.title

    for child in page.children or []:
        if isinstance(child, PageTitleBlock):
            return child.title

    return f"Page {page_index + 1}"


def _build_page_nav_item(
    page: AbstractPageBlock,
    *,
    page_index: int,
    is_current: bool,
) -> SideNavPage:
    return {
        "kind": "page",
        "label": _get_page_nav_label(page, page_index),
        "href": PLACEHOLDER_HREF,
        "is_current": is_current,
    }


def build_side_nav_items(
    steps: list[StepBlock],
    *,
    current_step_number: int | None = None,
    current_page_number: int | None = None,
    is_review: bool = False,
) -> list[SideNavSection]:
    side_nav_items: list[SideNavSection] = []

    for step_index, step in enumerate(steps):
        children = [
            _build_page_nav_item(
                page,
                page_index=page_index,
                is_current=(
                    not is_review
                    and step_index == current_step_number
                    and page_index == current_page_number
                ),
            )
            for page_index, page in enumerate(step.children or [])
        ]

        is_current = not is_review and step_index == current_step_number

        side_nav_items.append(
            {
                "kind": "section",
                "label": f"Section {step_index + 1}: {step.title}",
                "href": PLACEHOLDER_HREF,
                "is_current": is_current,
                "is_expanded": is_current,
                "pages": children,
            }
        )

    side_nav_items.append(
        {
            "kind": "review",
            "label": "Review and Submit",
            "href": PLACEHOLDER_HREF,
            "is_current": is_review,
            "is_expanded": False,
            "pages": [],
        }
    )

    return side_nav_items
