import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import Resolver404, resolve, reverse

from form_manager.models import FormEntry
from form_manager.schema.forms.utils import import_form_schema
from form_manager.schema.layout import AbstractPageBlock, FieldBlock, PageBlock, StepBlock
from form_manager.schema.navigation import build_form_edit_url, build_side_nav_items, get_step_pages
from form_manager.utils import save_form_entry, user_can_edit, user_can_submit

logger = logging.getLogger(__name__)


def _parse_step_or_page_param(raw_value: str | None) -> int:
    try:
        return int(raw_value or 0)
    except (TypeError, ValueError):
        return 0


def normalize_step_and_page(
    components: list[StepBlock], current_step: int, current_page: int
) -> tuple[int, int]:
    if not components:
        raise Http404("Form has no steps defined")

    normalized_step = min(max(current_step, 0), len(components) - 1)
    step_pages = get_step_pages(components[normalized_step])

    if not step_pages:
        raise Http404("Form section has no pages defined")

    normalized_page = min(max(current_page, 0), len(step_pages) - 1)
    return normalized_step, normalized_page


def get_step_page(components: list[StepBlock], step: int, page: int) -> AbstractPageBlock:
    return get_step_pages(components[step])[page]


def _get_safe_nav_redirect(redirect_to: str, *, entry_pk: str) -> str | None:
    """Allow side-nav POST redirects only to this entry's edit/review routes.

    The edit form stores a client-provided `redirect_to` value in a hidden input so
    the side nav can save the current page before navigating elsewhere. Because that
    value can be tampered with, we only allow redirects that:

    1. stay on this host (reject `//example.com` style URLs),
    2. resolve to a known form route, and
    3. target the same FormEntry being edited.

    Any other value falls back to the normal post-save flow and keeps the user on
    the current page.
    """
    if not redirect_to.startswith("/") or redirect_to.startswith("//"):
        return None

    path_only = redirect_to.split("?")[0]
    try:
        match = resolve(path_only)
    except Resolver404:
        return None

    if str(match.kwargs.get("pk")) != str(entry_pk):
        return None

    if match.view_name not in {"form_edit", "form_review"}:
        return None

    return redirect_to


def get_next_step_and_page(
    components, current_step: int, current_page: int
) -> tuple[int | None, int | None]:
    current_step_pages = get_step_pages(components[current_step])

    # If we're on the last step and page, move on to the review page
    if current_step == len(components) - 1 and current_page == len(current_step_pages) - 1:
        return None, None

    # If there's no children in the current step, move to the next step and first page
    if not current_step_pages:
        return current_step + 1, 0

    # Check if we're on the last page, and if so, move to the next step
    # and first page
    if current_page == len(current_step_pages) - 1:
        return current_step + 1, 0

    # Otherwise, stay on the current step but advance the next page
    return current_step, current_page + 1


def get_previous_step_and_page(
    components, current_step: int, current_page: int
) -> tuple[None, None] | tuple[int, int]:
    # if we're on the first step and page, you can't go back so
    # just return None
    if current_step == 0 and current_page == 0:
        return None, None

    # if we're on the first page of a step, decrement the current step and
    # return the last page of the previous step.
    if current_page == 0:
        return current_step - 1, len(get_step_pages(components[current_step - 1])) - 1

    # Otherwise, stay on the current step but decrement the next page
    return current_step, current_page - 1


def remove_nodes_with_excluded_fields(
    components: list[StepBlock], fields_to_exclude: list[str]
) -> list[StepBlock]:
    """This function takes a list of UI components (steps), removes any descendant FieldBlock
    components whose names are listed in `fields_to_exclude`, and removes any PageBlock nodes that
    lack descendant FieldBlock nodes.

    TODO: prune StepBlocks that become empty after filtering so navigation/review helpers
    can safely skip fully excluded sections instead of assuming every visible section
    still has at least one page.

    Current navigation assumes each visible section still has at least one page after filtering.
    Empty sections are not removed in this pass.
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
                # If the page has no remaining FieldBlock children, skip it
                logger.info("Removing empty page %s", child.title)
                continue

            children_to_keep.append(child)

        component.children = children_to_keep
        return component

    return [remove_excluded_nodes(comp) for comp in components]


@login_required
def form_edit(request, pk):
    """
    Edit an existing FormEntry.
    """
    entry: FormEntry = get_object_or_404(FormEntry, pk=pk)

    schema_class_ref = entry.form_definition.schema_class

    current_step_number = _parse_step_or_page_param(request.GET.get("step"))
    current_page_number = _parse_step_or_page_param(request.GET.get("page"))

    if request.method == "GET" and ("step" not in request.GET or "page" not in request.GET):
        return redirect(
            build_form_edit_url(
                entry.pk,
                step_number=current_step_number,
                page_number=current_page_number,
            )
        )

    # Check if user has visited the review page for this entry
    show_errors = request.session.get(f"show_errors_{entry.pk}", False)

    if not schema_class_ref:
        raise Http404("FormEntry has no schema_class defined")

    try:
        schema_cls = import_form_schema(schema_class_ref)
    except (ImportError, AttributeError) as exc:
        raise Http404(f"Unable to import schema class {schema_class_ref!r}: {exc}") from exc

    # Instantiate the schema if possible; fall back to using the class object
    schema = schema_cls.model_construct()

    # The django form is expected to be available on schema.form_fields
    django_form_class = schema_cls.get_form_fields_class()

    ui_components = [step.model_copy(deep=True) for step in schema.ui]

    def has_permission():
        return not (
            entry.locked
            or not user_can_edit(request.user, entry.organization)
            or not user_can_submit(request.user, entry.organization)
        )

    if request.method == "POST":
        if not has_permission():
            messages.error(request, "Permission denied.")
            return redirect("form_list")  # Assuming a form list URL

        save_form_entry(django_form_class, entry, request)

        # Check if user clicked "Save & Exit"
        page_action = request.POST.get("page-action")
        if page_action == "save-exit":
            return redirect("form_list")

        # Side nav navigation: save and redirect to the clicked page
        redirect_to = request.POST.get("redirect_to", "")
        safe_redirect_to = _get_safe_nav_redirect(redirect_to, entry_pk=str(entry.pk))
        if safe_redirect_to:
            return redirect(safe_redirect_to)

        messages.success(request, "Draft saved.")

    # If user has visited the review page, create a bound form with validation
    # to show error states. Otherwise, create an unbound form.
    if show_errors and entry.data:
        form = django_form_class(entry.data, initial=entry.data)
        form.is_valid(use_default_if_excluded=True)
    else:
        form = django_form_class(initial=entry.data or {})

    if form.fields_to_exclude:
        logger.info("Excluding the following fields: %s", form.fields_to_exclude)
        ui_components = remove_nodes_with_excluded_fields(ui_components, form.fields_to_exclude)

    current_step_number, current_page_number = normalize_step_and_page(
        ui_components, current_step_number, current_page_number
    )

    next_step_number, next_page_number = get_next_step_and_page(
        ui_components, current_step_number, current_page_number
    )

    previous_step_number, previous_page_number = get_previous_step_and_page(
        ui_components, current_step_number, current_page_number
    )

    if next_step_number is None:
        next_page_url = reverse("form_review", kwargs={"pk": entry.pk})
    else:
        assert next_page_number is not None
        next_page_url = build_form_edit_url(
            entry.pk,
            step_number=next_step_number,
            page_number=next_page_number,
        )

    prev_page_url = build_form_edit_url(
        entry.pk,
        step_number=previous_step_number or 0,
        page_number=previous_page_number or 0,
    )

    page_to_render = get_step_page(ui_components, current_step_number, current_page_number)

    page_to_render.set_extra_context(
        prev_url=prev_page_url,
        form=form,
        is_last_page=next_step_number is None,
        current_step_number=current_step_number,
        current_page_number=current_page_number,
        plan_coverage_value=(
            form["plan_coverage"].value() if "plan_coverage" in form.fields else None
        ),
    )

    context = {
        "steps": ui_components,
        "entry": entry,
        "current_step_number": current_step_number,
        "current_page_number": current_page_number,
        "current_step": ui_components[current_step_number],
        "current_page": page_to_render,
        "next_url": next_page_url,
        "prev_url": prev_page_url,
        "side_nav_items": build_side_nav_items(
            ui_components,
            current_step_number=current_step_number,
            current_page_number=current_page_number,
            entry_pk=entry.pk,
        ),
    }

    return render(request, "form_manager/form_edit.html", context)
