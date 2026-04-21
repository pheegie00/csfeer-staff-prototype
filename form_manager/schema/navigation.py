from typing import TypedDict
from uuid import UUID

from django.urls import reverse

from form_manager.schema.layout import (
    AbstractPageBlock,
    FieldBlock,
    PageTitleBlock,
    ReviewSubheadingBlock,
    StepBlock,
)

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
    disabled_reason: str
    pages: list[SideNavPage]


class ReviewSection(TypedDict):
    title: str | None
    edit_url: str
    blocks: list[FieldBlock | ReviewSubheadingBlock]


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


def get_step_pages(step: StepBlock) -> list[AbstractPageBlock]:
    return [child for child in (step.children or []) if isinstance(child, AbstractPageBlock)]


def find_nearest_navigable_step_page(
    steps: list[StepBlock], *, requested_step: int, requested_page: int
) -> tuple[int, int] | None:
    """Return the closest visible edit destination while preserving empty steps for the rail."""
    if not steps:
        return None

    normalized_step = min(max(requested_step, 0), len(steps) - 1)
    step_pages = get_step_pages(steps[normalized_step])
    if step_pages:
        normalized_page = min(max(requested_page, 0), len(step_pages) - 1)
        return normalized_step, normalized_page

    previous_step = normalized_step - 1
    while previous_step >= 0:
        previous_pages = get_step_pages(steps[previous_step])
        if previous_pages:
            return previous_step, 0
        previous_step -= 1

    next_step = normalized_step + 1
    while next_step < len(steps):
        next_pages = get_step_pages(steps[next_step])
        if next_pages:
            return next_step, 0
        next_step += 1

    return None


def _collect_review_blocks(node) -> list[FieldBlock | ReviewSubheadingBlock]:
    blocks: list[FieldBlock | ReviewSubheadingBlock] = []

    for child in node.children or []:
        if isinstance(child, ReviewSubheadingBlock):
            blocks.append(child)

        if isinstance(child, FieldBlock):
            blocks.append(child)

        if child.children:
            blocks.extend(_collect_review_blocks(child))

    return blocks


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
        step_pages = get_step_pages(step)
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
                "disabled_reason": (step.disabled_reason or "") if not step_pages else "",
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
            "disabled_reason": "",
            "pages": [],
        }
    )

    return side_nav_items


def build_review_sections(steps: list[StepBlock], *, entry_pk: EntryPk) -> list[ReviewSection]:
    final: list[ReviewSection] = []

    for step_index, initial_step in enumerate(steps):
        section: ReviewSection = {
            "title": initial_step.title,
            "edit_url": build_form_edit_url(entry_pk, step_number=step_index, page_number=0),
            "blocks": _collect_review_blocks(initial_step),
        }
        final.append(section)

    return final
