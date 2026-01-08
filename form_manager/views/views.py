from functools import lru_cache
from typing import Any, cast
from uuid import UUID

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from weasyprint import HTML

from form_manager.models import (
    FormAuditTrail,
    FormDefinition,
    FormEntry,
    OrganizationProfile,
)
from form_manager.schema.forms.utils import import_form_schema
from form_manager.schema.layout import PageBlock
from form_manager.utils import (
    reconstruct_state,
    record_field_diffs,
    to_jsonable,
    user_can_edit,
    user_can_view,
)
from form_manager.views.base import BaseSingleFormView, FormPermissionMixin
from tests.conftest import page


@login_required
def form_list(request):
    org = OrganizationProfile.objects.filter(userorganizationmembership__user=request.user).first()
    entries = FormEntry.objects.filter(organization=org, is_archived=False) if org else []
    definitions = FormDefinition.objects.filter(is_active=True)
    return render(request, "forms/form_list.html", {"entries": entries, "definitions": definitions})


@login_required
def form_start(request, form_id: UUID):
    org = OrganizationProfile.objects.filter(userorganizationmembership__user=request.user).first()
    if not org or not user_can_edit(request.user, org):
        messages.error(request, "No permission to create forms.")
        return redirect("form_list")
    form_def = get_object_or_404(FormDefinition, id=form_id, is_active=True)
    last = (
        FormEntry.objects.filter(organization=org, form_definition=form_def)
        .order_by("-version_number")
        .first()
    )
    next_ver = 1 if not last else last.version_number + 1
    entry = FormEntry.objects.create(
        form_definition=form_def, organization=org, created_by=request.user, version_number=next_ver
    )
    FormAuditTrail.objects.create(form_entry=entry, user=request.user, action="create")
    return redirect("form_edit", pk=entry.pk)


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
    current_page.set_extra_context(form=django_form_class())

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

    context = {
        "form": django_form_class,
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

    return render(request, "form_manager/form_edit.html", context)


class FormPreviewView(BaseSingleFormView, FormPermissionMixin):
    template_name = "forms/form_preview.html"
    context_object_name = "entry"

    def has_permission(self) -> bool:

        if not self.can_view():
            messages.error(self.request, "No permission to view.")
            return False

        return True


@login_required
def form_history(request, pk: UUID):
    """Show submission events for this entry and allow previewing snapshots at each submit/amend."""
    entry = get_object_or_404(FormEntry, pk=pk)
    if not user_can_view(request.user, entry.organization):
        messages.error(request, "No permission to view.")
        return redirect("form_list")

    events = (
        FormAuditTrail.objects.filter(form_entry=entry, action__in=["submit", "amend"])  # type: ignore[arg-type]
        .order_by("-timestamp")
        .all()
    )

    return render(
        request,
        "forms/form_history.html",
        {"current": entry, "events": events},
    )


class FormSnapshotView(BaseSingleFormView, FormPermissionMixin):
    template_name = "forms/form_preview.html"
    context_object_name = "entry"

    def has_permission(self) -> bool:

        if not self.can_view():
            messages.error(self.request, "No permission to view.")
            return False

        return True

    def get_initial(self):
        audit = self.get_audit()
        return reconstruct_state(self.object, upto=audit.timestamp)

    @lru_cache
    def get_audit(self):

        audit_id = self.kwargs["audit_id"]
        return get_object_or_404(FormAuditTrail, pk=audit_id, form_entry=self.object)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        audit = self.get_audit()
        context.update(
            {
                "snapshot_at": audit.timestamp,
                "snapshot_action": audit.action,
            }
        )
        return context


@login_required
def form_lock(request, pk: UUID):
    entry = get_object_or_404(FormEntry, pk=pk)
    if not user_can_edit(request.user, entry.organization):
        messages.error(request, "No permission to lock/unlock.")
        return redirect("form_list")
    entry.locked = True
    entry.save()
    FormAuditTrail.objects.create(form_entry=entry, user=request.user, action="lock")
    messages.info(request, "Entry locked.")
    return redirect("form_edit", pk=pk)


@login_required
def form_unlock(request, pk: UUID):
    entry = get_object_or_404(FormEntry, pk=pk)
    if not user_can_edit(request.user, entry.organization):
        messages.error(request, "No permission to lock/unlock.")
        return redirect("form_list")
    entry.locked = False
    entry.save()
    FormAuditTrail.objects.create(form_entry=entry, user=request.user, action="unlock")
    messages.info(request, "Entry unlocked.")
    return redirect("form_edit", pk=pk)


@login_required
def form_archive(request, pk: UUID):
    entry = get_object_or_404(FormEntry, pk=pk)
    if not user_can_edit(request.user, entry.organization):
        messages.error(request, "No permission to archive.")
        return redirect("form_list")
    entry.is_archived = True
    entry.status = "archived"
    entry.save()
    FormAuditTrail.objects.create(form_entry=entry, user=request.user, action="archive")
    messages.info(request, "Entry archived (soft deleted).")
    return redirect("form_list")


class FormDownloadPDFView(BaseSingleFormView, FormPermissionMixin):
    """Generate and download a PDF of the form entry."""

    def has_permission(self) -> bool:
        if not self.can_view():
            messages.error(self.request, "No permission to view.")
            return False
        return True

    def get(self, request, *args, **kwargs):
        self.object = cast(FormEntry, self.get_object())

        # Build the form with current data
        form = self.get_form()

        # Render the PDF template
        html_string = render_to_string(
            "forms/form_pdf.html",
            {
                "form": form,
                "entry": self.object,
            },
        )

        # Generate PDF
        pdf = HTML(string=html_string).write_pdf()

        # Create response with PDF
        response = HttpResponse(pdf, content_type="application/pdf")
        filename = (
            f"{self.object.form_definition.name}_v{self.object.version_number}_{self.object.pk}.pdf"
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        return response
