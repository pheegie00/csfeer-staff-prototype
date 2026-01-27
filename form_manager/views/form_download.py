from typing import cast

from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from form_manager.models import FormEntry
from form_manager.views.base import BaseSingleFormView, FormPermissionMixin


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
