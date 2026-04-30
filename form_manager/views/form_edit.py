import logging
from urllib.parse import parse_qs, urlsplit

import django.contrib.messages as messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import Resolver404, resolve, reverse

from form_manager.models import FormEntry
from form_manager.schema.forms.utils import import_form_schema
from form_manager.schema.layout import AbstractPageBlock, StepBlock
from form_manager.schema.navigation import (
    build_form_edit_url,
    build_side_nav_items,
    find_nearest_navigable_step_page,
    get_next_step_and_page,
    get_previous_step_and_page,
    get_step_pages,
    remove_nodes_with_excluded_fields,
)
from form_manager.utils import save_form_entry
from users.utils import user_can_edit, user_can_submit

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

    resolved_step_and_page = find_nearest_navigable_step_page(
        components,
        requested_step=current_step,
        requested_page=current_page,
    )

    if resolved_step_and_page is None:
        raise Http404("Form has no visible pages defined")

    return resolved_step_and_page


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


def _build_post_save_redirect(
    safe_redirect_to: str,
    *,
    entry_pk: str,
    components: list[StepBlock],
) -> str:
    """Resolve side-nav targets against the filtered post-save UI.

    If the target step still has pages, go there. If it became empty after
    saving, go forward from the clicked step (same direction as the Next button).
    """
    parsed_redirect = urlsplit(safe_redirect_to)
    match = resolve(parsed_redirect.path)

    if match.view_name == "form_review":
        return safe_redirect_to

    query_params = parse_qs(parsed_redirect.query)
    requested_step = _parse_step_or_page_param(query_params.get("step", [None])[0])
    requested_page = _parse_step_or_page_param(query_params.get("page", [None])[0])

    # Clamp to valid range — guards against a tampered step param
    requested_step = min(requested_step, len(components) - 1)

    if get_step_pages(components[requested_step]):
        resolved_step_and_page = find_nearest_navigable_step_page(
            components,
            requested_step=requested_step,
            requested_page=requested_page,
        )
        if resolved_step_and_page is not None:
            resolved_step, resolved_page = resolved_step_and_page
            return build_form_edit_url(
                entry_pk, step_number=resolved_step, page_number=resolved_page
            )

    # Target step is empty — go forward from the clicked step
    next_step, next_page = get_next_step_and_page(components, requested_step, requested_page)
    if next_step is None or next_page is None:
        return reverse("form_review", kwargs={"pk": entry_pk})
    return build_form_edit_url(entry_pk, step_number=next_step, page_number=next_page)


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
    safe_redirect_to: str | None = None

    if not user_can_edit(request.user, entry.organization):
        messages.error(request, "Permission denied.")
        return redirect("form_list")

    if entry.locked and not user_can_submit(request.user, entry.organization):
        messages.error(request, "Permission denied.")
        return redirect("form_list")

    if request.method == "POST":

        save_form_entry(django_form_class, entry, request)

        # Check if user clicked "Save & Exit"
        page_action = request.POST.get("page-action")
        if page_action == "save-exit":
            return redirect("form_list")

        # Side nav navigation: save and redirect to the clicked page
        redirect_to = request.POST.get("redirect_to", "")
        safe_redirect_to = _get_safe_nav_redirect(redirect_to, entry_pk=str(entry.pk))

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

    if request.method == "POST" and safe_redirect_to:
        return redirect(
            _build_post_save_redirect(
                safe_redirect_to,
                entry_pk=str(entry.pk),
                components=ui_components,
            )
        )

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
