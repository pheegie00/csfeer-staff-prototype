from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import FormAuditTrail, FormDefinition, FormEntry, OrganizationProfile
from .utils import (
    build_dynamic_form,
    reconstruct_state,
    record_field_diffs,
    to_jsonable,
    user_can_edit,
    user_can_submit,
    user_can_view,
)


@login_required
def form_list(request):
    org = OrganizationProfile.objects.filter(userorganizationmembership__user=request.user).first()
    entries = FormEntry.objects.filter(organization=org, is_archived=False) if org else []
    definitions = FormDefinition.objects.filter(is_active=True)
    return render(request, "forms/form_list.html", {"entries": entries, "definitions": definitions})


@login_required
def form_start(request, form_id: str):
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
def form_edit(request, pk: int):
    entry = get_object_or_404(FormEntry, pk=pk)
    org = entry.organization
    if entry.is_archived:
        messages.error(request, "This entry is archived (soft deleted).")
        return redirect("form_list")
    if not user_can_view(request.user, org):
        messages.error(request, "No permission to view.")
        return redirect("form_list")
    can_edit = user_can_edit(request.user, org) and not entry.locked
    can_submit = user_can_submit(request.user, org) and not entry.locked
    form = build_dynamic_form(
        entry.form_definition, data=request.POST or None, initial=entry.data, disabled=not can_edit
    )
    form.is_valid()
    if request.method == "POST" and can_edit:
        if "save" in request.POST:
            form.is_valid()
            old = entry.data.copy() if entry.data else {}
            entry.data = to_jsonable(form.cleaned_data)
            entry.save()
            FormAuditTrail.objects.create(form_entry=entry, user=request.user, action="save")
            record_field_diffs(entry, old, entry.data, user=request.user)
            messages.success(request, "Draft saved.")
            return redirect("form_edit", pk=pk)
        if "submit" in request.POST and can_submit and form.is_valid():
            old = entry.data.copy() if entry.data else {}
            entry.data = to_jsonable(form.cleaned_data)
            entry.status = "submitted"
            entry.submitted_at = timezone.now()
            entry.save()
            FormAuditTrail.objects.create(form_entry=entry, user=request.user, action="submit")
            record_field_diffs(entry, old, entry.data, user=request.user)
            messages.success(request, "Submitted.")
            return redirect("form_list")

    return render(
        request,
        "forms/form_edit.html",
        {
            "form": form,
            "entry": entry,
            "can_edit": can_edit,
            "can_submit": can_submit,
        },
    )


@login_required
def form_preview(request, pk: int):
    entry = get_object_or_404(FormEntry, pk=pk)
    if not user_can_view(request.user, entry.organization):
        messages.error(request, "No permission to view.")
        return redirect("form_list")
    form = build_dynamic_form(entry.form_definition, initial=entry.data, disabled=True)
    return render(request, "forms/form_preview.html", {"form": form, "entry": entry})


@login_required
def form_history(request, pk: int):
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


@login_required
def form_snapshot(request, pk: int, audit_id: int):
    entry = get_object_or_404(FormEntry, pk=pk)
    if not user_can_view(request.user, entry.organization):
        messages.error(request, "No permission to view.")
        return redirect("form_list")
    audit = get_object_or_404(FormAuditTrail, pk=audit_id, form_entry=entry)
    data = reconstruct_state(entry, upto=audit.timestamp)
    form = build_dynamic_form(entry.form_definition, initial=data, disabled=True)
    context = {
        "form": form,
        "entry": entry,
        "snapshot_at": audit.timestamp,
        "snapshot_action": audit.action,
    }
    return render(request, "forms/form_preview.html", context)


@login_required
def form_lock(request, pk: int):
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
def form_unlock(request, pk: int):
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
def form_archive(request, pk: int):
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
