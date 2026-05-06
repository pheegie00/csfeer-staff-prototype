import logging
from functools import lru_cache
from typing import Any
from uuid import UUID

import django.contrib.messages as messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from form_manager.locking import annotate_active_editors, refresh_editing_lock, release_editing_lock
from form_manager.models import (
    FormAuditTrail,
    FormDefinition,
    FormEntry,
)
from form_manager.utils import reconstruct_state
from form_manager.views.base import BaseSingleFormView, FormPermissionMixin
from organizations.models import OrganizationProfile
from users.utils import user_can_edit, user_can_start_form, user_can_view

logger = logging.getLogger(__name__)


@login_required
def form_list(request):
    org = OrganizationProfile.objects.filter(userorganizationmembership__user=request.user).first()
    raw_entries = (
        FormEntry.objects.filter(organization=org, is_archived=False)
        if org
        else FormEntry.objects.none()
    )
    entries = annotate_active_editors(raw_entries)
    definitions = FormDefinition.objects.filter(is_active=True)
    return render(
        request,
        "forms/form_list.html",
        {"entries": entries, "definitions": definitions, "organization": org},
    )


@login_required
def form_start(request, form_id: UUID):

    org = OrganizationProfile.objects.filter(userorganizationmembership__user=request.user).first()
    if not org:
        messages.error(request, "User is not part of an organization.")
        logger.info("User is not part of an organization")
        return redirect("form_list")
    if not user_can_start_form(request.user, org):
        messages.error(request, "No permission to create forms.")
        logger.info(f"{request.user} does not have permission to start forms for org {org.name}")
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

    submission_events = (
        FormAuditTrail.objects.filter(form_entry=entry, action__in=["submit", "amend"])  # type: ignore[arg-type]
        .order_by("-created_at")
        .all()
    )

    all_events = FormAuditTrail.objects.filter(form_entry=entry).order_by("-created_at").all()

    return render(
        request,
        "forms/form_history.html",
        {"current": entry, "submission_events": submission_events, "all_events": all_events},
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
        return reconstruct_state(self.object, upto=audit.created_at)

    @lru_cache
    def get_audit(self):

        audit_id = self.kwargs["audit_id"]
        return get_object_or_404(FormAuditTrail, pk=audit_id, form_entry=self.object)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        audit = self.get_audit()
        context.update(
            {
                "snapshot_at": audit.created_at,
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


@login_required
@require_POST
def editing_lock_heartbeat(request, pk: UUID):
    """Refresh the editing lock TTL. Called periodically by JS on the form edit page."""
    entry = get_object_or_404(FormEntry, pk=pk)
    refresh_editing_lock(entry, request.user)
    return JsonResponse({"status": "ok"})


@login_required
@require_POST
def editing_lock_release(request, pk: UUID):
    """Explicitly release the editing lock. Called by sendBeacon on page unload."""
    entry = get_object_or_404(FormEntry, pk=pk)
    lock_token = request.POST.get("lock_token")
    release_editing_lock(entry, request.user, lock_token=lock_token)
    return JsonResponse({"status": "ok"})
