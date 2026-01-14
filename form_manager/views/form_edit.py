import logging
from typing import Any, cast
from uuid import UUID

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from form_manager.models import FormAuditTrail, FormEntry
from form_manager.schema.forms.utils import import_form_schema
from form_manager.schema.layout import PageBlock
from form_manager.utils import record_field_diffs, to_jsonable

logger = logging.getLogger(__name__)


@login_required
def form_edit(request, pk):
    """
    Edit an existing FormEntry.

    Context provided to the template:
      - form: the django form (value of the form schema's `form_fields` property)
      - ui_components: a dict representation of the form schema's `ui` property
      - form_entry: the FormEntry instance
      - schema: the instantiated schema object
    """
    entry: FormEntry = get_object_or_404(FormEntry, pk=pk)

    schema_class_ref = entry.form_definition.schema_class

    current_step_number = int(request.GET.get("step", 0))
    current_page_number = int(request.GET.get("page", 0))

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

    ui_components = schema.ui

    def get_step_page(step: int, page: int) -> PageBlock:
        return ui_components[step].children[page]

    def get_next_step_and_page(
        current_step: int, current_page: int
    ) -> tuple[int | None, int | None]:
        current_ui_step = ui_components[current_step]

        # If there's no children in the current step, move to the next step and first page
        if not current_ui_step.children or len(current_ui_step.children) == 0:
            return current_step + 1, 0

        # Check if we're on the last page, and if so, move to the next step
        # and first page
        if current_page == len(current_ui_step.children) - 1:
            return current_step + 1, 0

        # Otherwise, stay on the current step but advance the next page
        return current_step, current_page + 1

    def get_previous_step_and_page(
        current_step: int, current_page: int
    ) -> tuple[None, None] | tuple[int, int]:

        # if we're on the first step and page, you can't go back so
        # just return None
        if current_step == 0 and current_page == 0:
            return None, None

        # if we're on the first page of a step, decrement the current step and
        # return the last page of the previous step.
        if current_page == 0:
            return current_step - 1, len(ui_components[current_step - 1].children) - 1

        # Otherwise, stay on the current step but decrement the next page
        return current_step, current_page - 1

    next_step_number, next_page_number = get_next_step_and_page(
        current_step_number, current_page_number
    )

    previous_step_number, previous_page_number = get_previous_step_and_page(
        current_step_number, current_page_number
    )

    current_page = get_step_page(int(current_step_number or 0), current_page_number or 0)

    def is_last_page(target_step_number, target_page_number):

        if len(ui_components) - 1 != target_step_number:
            return False

        if len(ui_components[target_step_number].children) - 1 != target_page_number:
            return False

        return True

    next_page_url = (
        reverse(
            "form_edit",
            kwargs={
                "pk": entry.pk,
            },
        )
        + f"?page={next_page_number}&step={next_step_number}"
    )

    prev_page_url = (
        reverse(
            "form_edit",
            kwargs={
                "pk": entry.pk,
            },
        )
        + f"?page={previous_page_number}&step={previous_step_number}"
    )

    def save_form_entry(form, status=None):
        is_valid = form.is_valid()
        old = entry.data.copy() if entry.data else {}

        # Only save fields that were actually in the POST request
        # to avoid overwriting data from other pages
        excluded_fields = {"csrfmiddlewaretoken", "current-step", "current-page", "page-action"}
        submitted_fields = set(request.POST.keys()) - excluded_fields

        # Build new_data from cleaned_data when available, otherwise from POST
        new_data = {}
        for field_name in submitted_fields:
            if is_valid and field_name in form.cleaned_data:
                # Use cleaned data for validated fields (proper type conversion)
                jsonable_dict = cast(
                    dict[str, Any], to_jsonable({field_name: form.cleaned_data[field_name]})
                )
                new_data[field_name] = jsonable_dict[field_name]
            elif field_name in request.POST:
                # For invalid forms or fields not in cleaned_data, use raw POST data
                new_data[field_name] = request.POST.get(field_name)

        entry.data = {**(entry.data or {}), **new_data}
        FormAuditTrail.objects.create(form_entry=entry, user=request.user, action="save")
        record_field_diffs(entry, old, entry.data, user=request.user)

        if status:
            entry.status = status

        if status == "submitted":
            entry.submitted_at = timezone.now()

        entry.save()

    def can_edit():
        # Implement based on your permission logic; e.g., check user roles or ownership
        return True  # Placeholder; replace with actual check

    def can_submit():
        # Implement based on your permission logic; e.g., check user roles or ownership
        return True  # Placeholder; replace with actual check

    def has_permission():
        if entry.locked:
            return False

        if "save" in request.POST and not can_edit():
            return False

        if "submit" in request.POST and not can_submit():
            return False

        return True

    if request.method == "POST":
        form = django_form_class(request.POST)

        if not has_permission():
            messages.error(request, "Permission denied.")
            return redirect("form_list")  # Assuming a form list URL

        if form.is_valid():
            if "submit" in request.POST:
                save_form_entry(form, status="submitted")
                messages.success(request, "Submitted.")
                return redirect("form_list")
            else:
                save_form_entry(form)
                messages.success(request, "Draft saved.")
                # Redirect to next page if "Save & Continue" was clicked, otherwise stay on current page
                page_action = request.POST.get("page-action")
                if page_action == "next":
                    return redirect(next_page_url)
                else:
                    return redirect(
                        request.path + f"?step={current_step_number}&page={current_page_number}"
                    )
        else:
            # Form is invalid (usually because page-action is in POST but not a form field)
            # Save as draft and handle navigation
            if "submit" in request.POST:
                messages.error(request, "Could not submit form due to errors.")
            else:
                # This is a save (either explicit save button or Save & Continue)
                save_form_entry(form)
                messages.success(request, "Draft saved.")
                # Navigate to next page if "Save & Continue" was clicked
                if request.POST.get("page-action") == "next":
                    return redirect(next_page_url)
                else:
                    return redirect(
                        request.path + f"?step={current_step_number}&page={current_page_number}"
                    )
    else:
        form = django_form_class(initial=entry.data or {})

    context = {
        "form": form,
        "steps": ui_components,
        "entry": entry,
        "schema": schema,
        "current_step_number": current_step_number,
        "current_page_number": current_page_number,
        "current_page": current_page,
        "is_last_page": is_last_page(current_step_number, current_page_number),
        "next_url": next_page_url,
        "prev_url": prev_page_url,
    }

    current_page.set_extra_context(**context)

    return render(request, "form_manager/form_edit.html", context)
