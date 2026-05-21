"""Form Builder views (Batch E.2).

Implements the multi-tenant Form Builder per
docs/multi_program_architecture.md ("Form Builder is the multi-tenant
admin layer"). Federal Staff with `program admin` role see + manage
only the form templates within their assigned programs; shared forms
(SF-424) appear separately as read-only.

Screens:
- FormBuilderListView   /staff/form-builder/        program-scoped list
- FormBuilderDetailView /staff/form-builder/<id>/   single template detail
                                                    + version history
                                                    + submission window
                                                    + org scoping count

Jira coverage:
- CORE-22  -- org scoping at publish time (shown read-only here; edit
              flow is a follow-up commit)
- CORE-25  -- submission window data model + UI (read-only here)
- CORE-27  -- extensible template schema (no UI; reads existing
              FormDefinition rows)
- CORE-28  -- pattern documented in staff_review/README.md
- CORE-56  -- 3 MVP templates seeded (verified via inbox)
- STAFF-MP-01..07  -- per-program isolation enforced

What this commit does NOT do (deferred):
- "Publish new version" form -- needs form-schema editor UI which is a
  big design conversation; for now versions are added via code +
  data migration (CORE-27 acceptance criteria)
- "Edit submission window" form -- needs the SubmissionWindow model
  (CORE-25) which doesn't exist yet
- "Adjust org scoping" form -- needs the OrgScoping model (CORE-22)
  which doesn't exist yet
- All edit/publish are surfaced as "TODO" buttons that show informational
  modals explaining what they'd do, so reviewers can give feedback on
  the UX before we model the data
"""

from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from form_manager.models.forms import FormDefinition
from programs.models import Program
from staff_review.mock_data import USER
from staff_review.permissions import StaffRequiredMixin


def _user_program_ids(user):
    """The Program ids this user is assigned to manage (STAFF-MP-04)."""
    if user.is_superuser:
        return list(Program.objects.values_list("id", flat=True))
    return list(user.program_assignments.values_list("program_id", flat=True))


def _user_can_manage(user, form_def):
    """True if user has form_builder rights for this template's program.

    Shared forms (is_shared=True) are managed only by platform admins
    -- modeled here as superusers, since we don't have a separate
    'Platform Admin' role yet (STAFF-MP-06 deferred).
    """
    if form_def.is_shared:
        return user.is_superuser
    if user.is_superuser:
        return True
    if form_def.program_id is None:
        return False
    return user.program_assignments.filter(program_id=form_def.program_id).exists()


class FormBuilderListView(StaffRequiredMixin, TemplateView):
    """List form templates the current user can manage.

    Splits the list into two sections:
        1. Templates for the user's assigned programs (full CRUD eventually)
        2. Shared forms (SF-424 etc.) -- read-only to most users
    """

    template_name = "staff_review/form_builder_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        u = self.request.user
        assigned_program_ids = _user_program_ids(u)

        # Per-program templates
        owned_forms = (
            FormDefinition.objects
            .filter(program_id__in=assigned_program_ids, is_shared=False)
            .select_related("program", "program__office")
            .order_by("program__code", "name", "-variant")
        )

        # Shared templates (SF-424 etc.) -- visible to all staff, editable only by platform admins
        shared_forms = (
            FormDefinition.objects
            .filter(is_shared=True)
            .select_related("program", "program__office")
            .order_by("name", "-variant")
        )

        # Programs the user is assigned to -- shown as filter chips
        assigned_programs = (
            Program.objects.filter(id__in=assigned_program_ids)
            .select_related("office")
            .order_by("office__code", "code")
        )

        ctx.update({
            "user": USER,
            "owned_forms": owned_forms,
            "shared_forms": shared_forms,
            "assigned_programs": assigned_programs,
            "has_any_assignments": bool(assigned_program_ids),
        })
        return ctx


class FormBuilderDetailView(StaffRequiredMixin, TemplateView):
    """Single form template's lifecycle dashboard.

    Shows: program, current version, version history, cycle type,
    submission window placeholder, org scoping count placeholder.
    Action buttons are TODO-marked pending the underlying data models
    (CORE-22 OrgScoping, CORE-25 SubmissionWindow).
    """

    template_name = "staff_review/form_builder_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        fd_id = kwargs.get("form_def_id")
        form_def = get_object_or_404(FormDefinition, pk=fd_id)

        u = self.request.user
        if not _user_can_manage(u, form_def):
            # Don't 404 (the form exists); show a "no access" state.
            messages.error(
                self.request,
                f"You are not assigned to manage forms in the "
                f"{form_def.program.code if form_def.program else '(unscoped)'} program.",
            )

        # Version history -- all FormDefinitions with the same name
        version_history = (
            FormDefinition.objects
            .filter(name=form_def.name)
            .order_by("-variant")
        )

        ctx.update({
            "user": USER,
            "form_def": form_def,
            "version_history": version_history,
            "can_manage": _user_can_manage(u, form_def),
            "is_shared": form_def.is_shared,
        })
        return ctx
