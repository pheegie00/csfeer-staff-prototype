import logging
from typing import TypedDict
from uuid import UUID

from django.urls import reverse

from form_manager.schema.layout import (
    AbstractPageBlock,
    ConditionalBlock,
    FieldBlock,
    PageBlock,
    PageTitleBlock,
    ReviewSubheadingBlock,
    StepBlock,
)

logger = logging.getLogger(__name__)

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


def _condition_met(form, controller_field: str, show_when: str | list[str]) -> bool:
    """Return True if the form's current value for controller_field matches show_when."""
    try:
        value = form[controller_field].value()
    except (KeyError, TypeError):
        return True
    # MultiValueField (e.g. YesNoDisplayField) returns a list; the radio is the first element.
    if isinstance(value, (list, tuple)):
        value = value[0] if value else None
    conditions = [show_when] if isinstance(show_when, str) else show_when
    return value in conditions


def _collect_review_blocks(
    node, *, form=None, controller_field: str | None = None
) -> list[FieldBlock | ReviewSubheadingBlock]:
    blocks: list[FieldBlock | ReviewSubheadingBlock] = []

    # SectionBlocks carry the controller field name for their ConditionalBlock children.
    active_controller = getattr(node, "alpine_controller_field", None) or controller_field

    for child in node.children or []:
        if isinstance(child, ConditionalBlock):
            if (
                form
                and active_controller
                and not _condition_met(form, active_controller, child.show_when)
            ):
                continue
            blocks.extend(
                _collect_review_blocks(child, form=form, controller_field=active_controller)
            )
        elif isinstance(child, (ReviewSubheadingBlock, FieldBlock)):
            blocks.append(child)
        elif child.children:
            blocks.extend(
                _collect_review_blocks(child, form=form, controller_field=active_controller)
            )

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


def get_next_step_and_page(
    components: list[StepBlock], current_step: int, current_page: int
) -> tuple[int | None, int | None]:
    current_step_pages = get_step_pages(components[current_step])

    if not current_step_pages or current_page == len(current_step_pages) - 1:
        next_step = current_step + 1
        while next_step < len(components):
            if get_step_pages(components[next_step]):
                return next_step, 0
            next_step += 1
        return None, None

    return current_step, current_page + 1


def get_previous_step_and_page(
    components: list[StepBlock], current_step: int, current_page: int
) -> tuple[None, None] | tuple[int, int]:
    if current_step == 0 and current_page == 0:
        return None, None

    if current_page == 0:
        prev_step = current_step - 1
        while prev_step >= 0:
            prev_pages = get_step_pages(components[prev_step])
            if prev_pages:
                return prev_step, len(prev_pages) - 1
            prev_step -= 1
        return None, None

    return current_step, current_page - 1


def remove_nodes_with_excluded_fields(
    components: list[StepBlock], fields_to_exclude: list[str]
) -> list[StepBlock]:
    """Remove excluded FieldBlocks and any PageBlocks that become empty.

    StepBlocks are preserved so the side nav can keep showing disabled sections.
    """

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

        return component.model_copy(update={"children": children_to_keep})

    return [remove_excluded_nodes(comp) for comp in components]


def build_review_sections(
    steps: list[StepBlock], *, entry_pk: EntryPk, form=None
) -> list[ReviewSection]:
    final: list[ReviewSection] = []

    for step_index, step in enumerate(steps):
        section: ReviewSection = {
            "title": step.title,
            "edit_url": build_form_edit_url(entry_pk, step_number=step_index, page_number=0),
            "blocks": _collect_review_blocks(step, form=form),
        }
        final.append(section)

    return final
