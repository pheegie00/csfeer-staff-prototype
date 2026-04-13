from typing import TypedDict
from uuid import UUID

from django.urls import reverse

from form_manager.schema.layout import AbstractPageBlock, PageTitleBlock, StepBlock

EntryPk = UUID | str


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


def build_form_edit_url(entry_pk: EntryPk, *, step_number: int, page_number: int) -> str:
    return reverse(
        "form_edit",
        kwargs={"pk": entry_pk},
        query={"step": step_number, "page": page_number},
    )


def _get_page_nav_label(page: AbstractPageBlock, page_index: int) -> str:
    if page.title:
        return page.title

    for child in page.children or []:
        if isinstance(child, PageTitleBlock):
            return child.title

    return f"Page {page_index + 1}"


def _get_step_pages(step: StepBlock, *, step_index: int) -> list[AbstractPageBlock]:
    pages = [child for child in (step.children or []) if isinstance(child, AbstractPageBlock)]

    if not pages:
        raise ValueError(
            f"Section {step_index + 1} has no pages after filtering. "
            "Current navigation requires at least one page per visible section."
        )

    return pages


def build_side_nav_items(
    steps: list[StepBlock],
    *,
    current_step_number: int | None = None,
    current_page_number: int | None = None,
    is_review: bool = False,
    entry_pk: EntryPk,
) -> list[SideNavSection]:
    side_nav_items: list[SideNavSection] = []

    for step_index, step in enumerate(steps):
        step_pages = _get_step_pages(step, step_index=step_index)
        children: list[SideNavPage] = [
            {
                "kind": "page",
                "label": _get_page_nav_label(page, page_index),
                "href": build_form_edit_url(
                    entry_pk, step_number=step_index, page_number=page_index
                ),
                "is_current": (
                    not is_review
                    and step_index == current_step_number
                    and page_index == current_page_number
                ),
            }
            for page_index, page in enumerate(step_pages)
        ]

        side_nav_items.append(
            {
                "kind": "section",
                "label": f"Section {step_index + 1}: {step.title}",
                "href": build_form_edit_url(entry_pk, step_number=step_index, page_number=0),
                "is_current": not is_review and step_index == current_step_number,
                "is_expanded": not is_review and step_index == current_step_number,
                "pages": children,
            }
        )

    side_nav_items.append(
        {
            "kind": "review",
            "label": "Review and Submit",
            "href": reverse("form_review", kwargs={"pk": entry_pk}),
            "is_current": is_review,
            "is_expanded": False,
            "pages": [],
        }
    )

    return side_nav_items
