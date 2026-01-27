import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from form_manager.models import FormEntry
from form_manager.schema.forms.utils import import_form_schema

logger = logging.getLogger(__name__)


@login_required
@require_http_methods(["POST"])
def form_finalize(request, pk):
    """
    Finalize a FormEntry.

    This is the last step in the form submission process. After the user
    reviews the draft information, they can save the form when all errors are
    fixed and submit the form a final time.

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

    form = django_form_class(entry.data)  # noqa: F841

    # if form.is_valid():
    entry.status = "submitted"
    entry.submitted_at = timezone.now()
    entry.save()

    messages.success(request, "Your form has been successfully submitted.")

    return redirect(
        reverse(
            "form_preview",
            kwargs={
                "pk": entry.pk,
            },
        )
    )

    messages.error(
        request, "There were errors in your form. Please correct them before submitting."
    )
    return redirect(
        reverse(
            "form_edit",
            kwargs={
                "pk": entry.pk,
            },
        )
        + f"?step={len(schema.ui)-1}&page={len(schema.ui[-1].children)-1}"
    )
