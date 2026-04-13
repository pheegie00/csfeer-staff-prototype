import logging

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from form_manager.models import FormEntry
from form_manager.schema.forms.utils import import_form_schema
from form_manager.schema.navigation import (
    build_form_edit_url,
    build_review_sections,
    build_side_nav_items,
)
from form_manager.utils import save_form_entry
from form_manager.views.form_edit import remove_nodes_with_excluded_fields

logger = logging.getLogger(__name__)


@login_required
@require_http_methods(["GET", "POST"])
def form_review(request, pk):
    """
    Review a FormEntry before submission.

    This view allows users to review their form data before final submission.
    It displays the form data in a read-only format for confirmation.

    """
    entry: FormEntry = get_object_or_404(FormEntry, pk=pk)

    schema_class_ref = entry.form_definition.schema_class

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

    if request.POST:
        save_form_entry(django_form_class, entry, request)

    entry.refresh_from_db()

    form = django_form_class(entry.data, initial=entry.data)

    is_valid = form.is_valid(use_default_if_excluded=True)

    # Set session flag to indicate user has seen the review page
    # This will cause form_edit to show validation errors
    request.session[f"show_errors_{entry.pk}"] = True

    ui_components = [step.model_copy(deep=True) for step in schema.ui]

    if form.fields_to_exclude:
        ui_components = remove_nodes_with_excluded_fields(ui_components, form.fields_to_exclude)

    context = {
        "form": form,
        "entry": entry,
        "steps": ui_components,
        "review_sections": build_review_sections(ui_components, entry_pk=entry.pk),
        "prev_url": build_form_edit_url(
            entry.pk,
            step_number=len(ui_components) - 1,
            page_number=len(ui_components[-1].children or []) - 1,
        ),
        "is_valid": is_valid,
        "side_nav_items": build_side_nav_items(ui_components, is_review=True, entry_pk=entry.pk),
    }

    for component in ui_components:
        component.set_extra_context(form=form)

    return render(request, "form_manager/review_and_submit.html", context)
