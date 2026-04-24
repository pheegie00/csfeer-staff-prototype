import io
import re

from django.contrib import admin
from django.core.management import call_command
from django.db import models
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html
from django_json_widget.widgets import JSONEditorWidget

from form_manager.models import (
    FormAuditDetail,
    FormAuditTrail,
    FormDefinition,
    FormEntry,
)

# TODO: Review permission and remove any unnecessary admin actions like delete, save etc.

_ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


@admin.register(FormDefinition)
class FormDefinitionAdmin(admin.ModelAdmin):
    list_display = ("family", "name", "variant", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "variant", "family")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "load-forms/",
                self.admin_site.admin_view(self.load_forms_view),
                name="form_manager_formdefinition_load_forms",
            ),
        ]
        return custom_urls + urls

    def load_forms_view(self, request):
        if not self.has_change_permission(request):
            self.message_user(request, "Permission denied.", level="error")
            return HttpResponseRedirect(reverse("admin:form_manager_formdefinition_changelist"))

        force = request.GET.get("force") == "1"
        stdout = io.StringIO()

        try:
            call_command("load_initial_forms", force=force, stdout=stdout, no_color=True)
        except Exception as e:
            self.message_user(request, f"Error running load_initial_forms: {e}", level="error")
        else:
            for line in _ANSI_ESCAPE.sub("", stdout.getvalue()).splitlines():
                if line.strip():
                    self.message_user(request, line.strip())

        return HttpResponseRedirect(reverse("admin:form_manager_formdefinition_changelist"))


@admin.register(FormEntry)
class FormEntryAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "form_definition",
        "version_number",
        "status",
        "locked",
        "updated_at",
        "download_pdf_link",
    )
    list_filter = ("status", "locked")
    search_fields = ("organization__name", "form_definition__name")

    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }

    @admin.display(description="PDF")
    def download_pdf_link(self, obj):
        """Add a download PDF link in the admin list view."""
        url = reverse("form_download_pdf", args=[obj.pk])
        return format_html('<a href="{}" target="_blank">Download PDF</a>', url)


@admin.register(FormAuditTrail)
class FormAuditTrailAdmin(admin.ModelAdmin):
    list_display = ("form_entry", "user", "action", "created_at")
    list_filter = ("action",)


@admin.register(FormAuditDetail)
class FormAuditDetailAdmin(admin.ModelAdmin):
    list_display = ("form_entry", "user", "user__email", "field_name", "created_at")
    search_fields = ("field_name",)
    list_filter = ("form_entry__form_definition__name",)
