import logging
from typing import TypedDict

from django.urls import reverse

from form_manager.constants import CSBGAnnualReportForms
from form_manager.models import FormEntry
from form_manager.schema.layout import (
    AbstractPageBlock,
    FieldBlock,
    PageBlock,
    PageTitleBlock,
    StepBlock,
)

logger = logging.getLogger(__name__)


FORM_SIDENAV_FORM_NAMES = {
    CSBGAnnualReportForms.TRIBAL_ANNUAL_REPORT_3_0,
    CSBGAnnualReportForms.TRIBAL_ANNUAL_REPORT_3_0_SHORT,
}


class FormSidenavItem(TypedDict):
    title: str | None
    href: str
    is_current: bool
    children: list["FormSidenavItem"]


def uses_form_sidenav(form_definition_name: str) -> bool:
    return form_definition_name in FORM_SIDENAV_FORM_NAMES


def remove_nodes_with_excluded_fields(
    components: list[StepBlock], fields_to_exclude: list[str]
) -> list[StepBlock]:
    """Remove excluded fields and any pages that become empty after filtering."""

    def remove_excluded_nodes(component):
        children_to_keep = []

        for child in component.children:
            if isinstance(child, FieldBlock) and child.field_name in fields_to_exclude:
                logger.info("Removing field %s", child.field_name)
                continue

            if hasattr(child, "children") and child.children:
                child = remove_excluded_nodes(child)

            if isinstance(child, PageBlock) and not child.has_field_blocks(child):
                logger.info("Removing empty page %s", child.title)
                continue

            children_to_keep.append(child)

        component.children = children_to_keep
        return component

    return [remove_excluded_nodes(comp) for comp in components]


def get_page_title(page: AbstractPageBlock) -> str:
    if page.title:
        return page.title

    for child in page.children or []:
        if isinstance(child, PageTitleBlock) and child.title:
            return child.title

    return "Untitled page"


def get_step_pages(step: StepBlock) -> list[AbstractPageBlock]:
    return [child for child in step.children or [] if isinstance(child, AbstractPageBlock)]


def get_form_edit_url(entry: FormEntry, step_number: int, page_number: int) -> str:
    return reverse("form_edit", kwargs={"pk": entry.pk}) + f"?step={step_number}&page={page_number}"


def build_form_sidenav_children(
    entry: FormEntry, step: StepBlock, step_number: int, current_page_number: int
) -> list[FormSidenavItem]:
    return [
        {
            "title": get_page_title(page),
            "href": get_form_edit_url(entry, step_number, page_index),
            "is_current": page_index == current_page_number,
            "children": [],
        }
        for page_index, page in enumerate(get_step_pages(step))
    ]


def build_form_sidenav_items(
    entry: FormEntry,
    steps: list[StepBlock],
    current_step_number: int,
    current_page_number: int,
    *,
    is_review_page: bool = False,
) -> list[FormSidenavItem]:
    sidenav_items: list[FormSidenavItem] = []

    for step_index, step in enumerate(steps):
        sidenav_items.append(
            {
                "title": step.title,
                "href": get_form_edit_url(entry, step_index, 0),
                "is_current": not is_review_page and step_index == current_step_number,
                "children": (
                    build_form_sidenav_children(entry, step, step_index, current_page_number)
                    if not is_review_page and step_index == current_step_number
                    else []
                ),
            }
        )

    sidenav_items.append(
        {
            "title": "Review and Submit",
            "href": reverse("form_review", kwargs={"pk": entry.pk}),
            "is_current": is_review_page,
            "children": [],
        }
    )

    return sidenav_items


def resolve_form_edit_destination(
    steps: list[StepBlock], requested_step_number: int, requested_page_number: int
) -> tuple[int, int]:
    """Return a visible edit destination after filtering changes the page set."""

    if not steps:
        raise ValueError("No visible form sidenav edit destination is available.")

    resolved_step_number = min(max(requested_step_number, 0), len(steps) - 1)

    if resolved_step_number != requested_step_number:
        logger.info(
            "Form sidenav destination step %s is out of range; " "clamping to step %s.",
            requested_step_number,
            resolved_step_number,
        )

    requested_step_pages = get_step_pages(steps[resolved_step_number])
    if requested_step_pages:
        if 0 <= requested_page_number < len(requested_step_pages):
            return resolved_step_number, requested_page_number
        logger.info(
            "Form sidenav destination %s/%s no longer exists; "
            "falling back to first page in step.",
            requested_step_number,
            requested_page_number,
        )
        return resolved_step_number, 0

    fallback_step_numbers = list(range(resolved_step_number - 1, -1, -1))
    fallback_step_numbers.extend(range(resolved_step_number + 1, len(steps)))

    for fallback_step_number in fallback_step_numbers:
        fallback_pages = get_step_pages(steps[fallback_step_number])
        if fallback_pages:
            logger.info(
                "Form sidenav destination %s/%s has no visible pages; "
                "falling back to step %s page 0.",
                requested_step_number,
                requested_page_number,
                fallback_step_number,
            )
            return fallback_step_number, 0

    raise ValueError("No visible form sidenav edit destination is available.")
