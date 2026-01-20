import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from form_manager.models import FormEntry
from form_manager.schema.forms.utils import import_form_schema
from form_manager.schema.layout import PageBlock
from form_manager.utils import save_form_entry, user_can_edit, user_can_submit

logger = logging.getLogger(__name__)


def get_step_page(components, step: int, page: int) -> PageBlock:
    return components[step].children[page]


def get_next_step_and_page(
    components, current_step: int, current_page: int
) -> tuple[int | None, int | None]:
    current_ui_step = components[current_step]

    # If we're on the last step and page, move on to the review page
    if (
        current_step == len(components) - 1
        and current_page == len(current_ui_step.children or []) - 1
    ):
        return None, None

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
    components, current_step: int, current_page: int
) -> tuple[None, None] | tuple[int, int]:

    # if we're on the first step and page, you can't go back so
    # just return None
    if current_step == 0 and current_page == 0:
        return None, None

    # if we're on the first page of a step, decrement the current step and
    # return the last page of the previous step.
    if current_page == 0:
        return current_step - 1, len(components[current_step - 1].children) - 1

    # Otherwise, stay on the current step but decrement the next page
    return current_step, current_page - 1


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

    def has_permission():
        if entry.locked:
            return False

        if "save" in request.POST and not user_can_edit(request.user, entry.organization):
            return False

        if "submit" in request.POST and not user_can_submit(request.user, entry.organization):
            return False

        return True

    if request.method == "POST":

        if not has_permission():
            messages.error(request, "Permission denied.")
            return redirect("form_list")  # Assuming a form list URL

        form = django_form_class(request.POST)

        save_form_entry(form, entry, request)
        messages.success(request, "Draft saved.")

    form = django_form_class(initial=entry.data or {})

    next_step_number, next_page_number = get_next_step_and_page(
        ui_components, current_step_number, current_page_number
    )

    previous_step_number, previous_page_number = get_previous_step_and_page(
        ui_components, current_step_number, current_page_number
    )

    current_page = get_step_page(
        ui_components, int(current_step_number or 0), current_page_number or 0
    )

    if next_step_number is None:
        next_page_url = reverse("form_review", kwargs={"pk": entry.pk})
    else:
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

    context = {
        "form": form,
        "steps": ui_components,
        "entry": entry,
        "schema": schema,
        "current_step_number": current_step_number,
        "current_page_number": current_page_number,
        "is_last_page": next_step_number is None,
        "next_url": next_page_url,
        "prev_url": prev_page_url,
    }

    # add the context to all steps, even if we're not going to render that step
    # on this page.
    for component in ui_components:
        component.set_extra_context(**context)

    current_page = get_step_page(
        ui_components, int(current_step_number or 0), current_page_number or 0
    )

    context.update(
        {
            "current_page": current_page,
        }
    )

    return render(request, "form_manager/form_edit.html", context)
