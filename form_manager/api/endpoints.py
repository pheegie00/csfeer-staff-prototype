"""
REST API endpoints for form_manager using Django Ninja.
Read-only (GET) endpoints only.
"""

from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja.errors import HttpError
from ninja.security import django_auth

from form_manager.api.schemas import (
    AuditDetailSchema,
    AuditTrailSchema,
    FormDefinitionListSchema,
    FormDefinitionSchema,
    FormEntryListSchema,
    FormEntrySchema,
    OrganizationSchema,
)
from form_manager.models import (
    FormAuditDetail,
    FormAuditTrail,
    FormDefinition,
    FormEntry,
    OrganizationProfile,
)
from form_manager.utils import user_can_view

# Initialize API with Django session authentication
api = NinjaAPI(
    title="Form Manager API",
    version="1.0.0",
    description="Read-only API for accessing form definitions, entries, and audit trails",
    auth=django_auth,
)


# ==================== Helper Functions ====================


def get_user_organization(request) -> OrganizationProfile:
    """Get the user's organization or raise 404."""
    org = OrganizationProfile.objects.filter(userorganizationmembership__user=request.user).first()
    if not org:
        raise HttpError(404, "No organization found for user")
    return org


def check_view_permission(request, entry: FormEntry) -> None:
    """Check if user can view the entry."""
    if not user_can_view(request.user, entry.organization):
        raise HttpError(403, "Permission denied")


# ==================== Form Definitions Endpoints ====================


@api.get("/forms/definitions", response=list[FormDefinitionListSchema], tags=["Forms"])
def list_form_definitions(request):
    """List all active form definitions."""
    return FormDefinition.objects.filter(is_active=True).order_by("name", "variant")


@api.get(
    "/forms/definitions/{definition_id}",
    response=FormDefinitionSchema,
    tags=["Forms"],
)
def get_form_definition(request, definition_id: int):
    """Get a specific form definition by ID."""
    definition = get_object_or_404(FormDefinition, pk=definition_id, is_active=True)
    return definition


# ==================== Form Entries Endpoints ====================


@api.get(
    "/forms/definitions/{definition_id}/entries", response=list[FormEntryListSchema], tags=["Forms"]
)
def list_form_entries_for_definition(
    request,
    definition_id: int,
    status: str | None = None,
    include_archived: bool = False,
):
    """
    List form entries for a specific form definition within the user's organization.

    Filters:
    - status: Filter by entry status (draft, submitted, amended, archived)
    - include_archived: Include archived entries (default: false)
    """
    # Ensure the form definition exists and is active
    get_object_or_404(FormDefinition, pk=definition_id, is_active=True)

    org = get_user_organization(request)

    queryset = FormEntry.objects.filter(
        organization=org, form_definition__id=definition_id
    ).select_related("form_definition", "organization")

    if not include_archived:
        queryset = queryset.filter(is_archived=False)

    if status:
        queryset = queryset.filter(status=status)

    entries = queryset.order_by("-updated_at")

    return [
        {
            "id": entry.pk,
            "form_definition_name": entry.form_definition.name,
            "form_definition_variant": str(entry.form_definition.variant),
            "organization_name": entry.organization.name,
            "version_number": entry.version_number,
            "status": entry.status,
            "submitted_at": entry.submitted_at,
            "updated_at": entry.updated_at,
            "locked": entry.locked,
        }
        for entry in entries
    ]


@api.get("/forms/entries/{entry_id}", response=FormEntrySchema, tags=["Forms"])
def get_form_entry(request, entry_id: int):
    """Get a specific form entry with full details."""
    entry = get_object_or_404(
        FormEntry.objects.select_related("form_definition", "organization"),
        pk=entry_id,
    )
    check_view_permission(request, entry)
    return entry


# ==================== Audit Trail Endpoints ====================


@api.get(
    "/forms/entries/{entry_id}/audit-trail",
    response=list[AuditTrailSchema],
    tags=["Forms"],
)
def get_audit_trail(request, entry_id: int):
    """Get audit trail for a form entry."""
    entry = get_object_or_404(FormEntry, pk=entry_id)
    check_view_permission(request, entry)

    audits = FormAuditTrail.objects.filter(form_entry=entry).order_by("-timestamp")

    return audits


@api.get(
    "/forms/entries/{entry_id}/audit-details",
    response=list[AuditDetailSchema],
    tags=["Forms"],
)
def get_audit_details(request, entry_id: int):
    """Get detailed field-level changes for a form entry."""
    entry = get_object_or_404(FormEntry, pk=entry_id)
    check_view_permission(request, entry)

    details = FormAuditDetail.objects.filter(form_entry=entry).order_by("-timestamp")

    return details


# ==================== Organization Endpoint ====================


@api.get("/forms/organizations/me", response=OrganizationSchema, tags=["Forms"])
def get_my_organization(request):
    """Get the current user's organization."""
    org = get_user_organization(request)
    return org
