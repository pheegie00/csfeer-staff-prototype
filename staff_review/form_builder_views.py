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

from datetime import datetime, timezone as dt_tz

from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from form_manager.models.forms import FormDefinition, FormEntry
from organizations.models import OrgType
from programs.models import FormScoping, Program, SubmissionWindow
from staff_review.feature_flags import FeatureRequiredMixin
from staff_review.mock_data import USER
from staff_review.permissions import StaffRequiredMixin
from staff_review.publish_service import (
    IN_PROGRESS_STATUSES,
    PublishError,
    bump_major,
    bump_minor,
    publish_new_version,
)


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


class FormBuilderListView(FeatureRequiredMixin, StaffRequiredMixin, TemplateView):
    feature_key = "form_builder"

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

        # Programs the user is assigned to -- shown as filter chips
        assigned_programs = list(
            Program.objects.filter(id__in=assigned_program_ids)
            .select_related("office")
            .order_by("office__code", "code")
        )

        # ?program=<code> narrows the list to one program. Empty / unknown
        # falls back to "all my programs." Gated by feature flag so a demo
        # presenter can disable the filtering UI entirely if desired.
        from staff_review.feature_flags import is_enabled
        chip_filters_on = is_enabled("form_builder_chip_filters")
        program_filter = (self.request.GET.get("program") or "").strip() if chip_filters_on else ""
        active_program = None
        if program_filter:
            active_program = next(
                (p for p in assigned_programs if p.code == program_filter), None,
            )

        # Per-program templates -- filtered if a chip is selected
        owned_qs = (
            FormDefinition.objects
            .filter(program_id__in=assigned_program_ids, is_shared=False)
            .select_related("program", "program__office")
            .order_by("program__code", "name", "-variant")
        )
        if active_program is not None:
            owned_qs = owned_qs.filter(program=active_program)
        owned_forms = owned_qs

        # Shared templates (SF-424 etc.) -- visible to all staff, editable only by platform admins
        shared_forms = (
            FormDefinition.objects
            .filter(is_shared=True)
            .select_related("program", "program__office")
            .order_by("name", "-variant")
        )

        ctx.update({
            "user": USER,
            "owned_forms": owned_forms,
            "shared_forms": shared_forms,
            "assigned_programs": assigned_programs,
            "has_any_assignments": bool(assigned_program_ids),
            "active_program_code": active_program.code if active_program else None,
        })
        return ctx


class FormBuilderDetailView(FeatureRequiredMixin, StaffRequiredMixin, TemplateView):
    feature_key = "form_builder"

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

        # CORE-25: submission windows for this form across fiscal years
        windows = list(form_def.submission_windows.order_by("-opens_at"))
        current_fy = "FY26"  # TODO: derive from a global setting
        current_window = next((w for w in windows if w.fiscal_year == current_fy), None)

        # CORE-22: org scoping for this form
        scoping = getattr(form_def, "scoping", None)
        scoped_org_count = scoping.in_scope_org_count() if scoping else 0

        # Human labels for org types in scope
        org_type_labels = []
        if scoping and scoping.scope_to_org_types:
            type_dict = {c[0]: c[1] for c in OrgType.choices}
            org_type_labels = [type_dict.get(t, t) for t in scoping.scope_to_org_types]

        # STAFF-MP-13: schema-driven runtime. Just need to know whether a
        # real spec exists + a FormEntry id to point "Preview as recipient"
        # at. The previous technical observability (View spec modal, lint
        # status, version, item count) was stripped -- non-technical users
        # don't need to see raw JSON or schema diagnostics.
        from staff_review.feature_flags import is_enabled
        runtime_on = is_enabled("form_runtime")
        has_spec = (
            runtime_on
            and isinstance(form_def.schema, dict)
            and bool(form_def.schema)
            and form_def.schema.get("$formspec")
        )
        first_entry_id = None
        if has_spec:
            first = FormEntry.objects.filter(form_definition=form_def).first()
            first_entry_id = first.id if first else None

        # STAFF-MP-14: visual field editor. Only schema-driven forms can be
        # edited field-by-field; legacy pydantic forms fall back to the
        # existing read-only detail page.
        from form_manager.services import schema_editor as se
        editor_available = bool(has_spec)
        draft_pending = editor_available and se.has_draft(form_def)

        ctx.update({
            "user": USER,
            "form_def": form_def,
            "version_history": version_history,
            "can_manage": _user_can_manage(u, form_def),
            "is_shared": form_def.is_shared,
            # CORE-25
            "windows": windows,
            "current_window": current_window,
            "current_fy": current_fy,
            # CORE-22
            "scoping": scoping,
            "scoped_org_count": scoped_org_count,
            "org_type_labels": org_type_labels,
            "all_org_types": OrgType.choices,
            # STAFF-MP-13 schema-driven runtime (just the bits the page header needs)
            "form_runtime_on": runtime_on,
            "first_entry_id": first_entry_id,
            # STAFF-MP-14 visual field editor
            "editor_available": editor_available,
            "draft_pending": draft_pending,
        })
        return ctx


# ============================================================
# SUBMISSION WINDOW EDIT (CORE-25)
# ============================================================

class SubmissionWindowEditView(FeatureRequiredMixin, StaffRequiredMixin, View):
    feature_key = "form_builder"

    """POST handler: create or update a SubmissionWindow.

    Form fields:
      fiscal_year    -- e.g. "FY26"
      opens_at       -- YYYY-MM-DD
      closes_at      -- YYYY-MM-DD

    Uses update_or_create so the same FY just overwrites.
    """

    def post(self, request, form_def_id):
        form_def = get_object_or_404(FormDefinition, pk=form_def_id)
        if not _user_can_manage(request.user, form_def):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied()

        fy = (request.POST.get("fiscal_year") or "").strip()
        opens_s = (request.POST.get("opens_at") or "").strip()
        closes_s = (request.POST.get("closes_at") or "").strip()

        if not (fy and opens_s and closes_s):
            messages.error(request, "Fiscal year + opens + closes are all required.")
            return redirect(reverse("staff_review:form_builder_detail", kwargs={"form_def_id": form_def.id}))

        try:
            opens_at = datetime.fromisoformat(opens_s).replace(tzinfo=dt_tz.utc)
            closes_at = datetime.fromisoformat(closes_s).replace(tzinfo=dt_tz.utc)
        except ValueError:
            messages.error(request, "Dates must be YYYY-MM-DD format.")
            return redirect(reverse("staff_review:form_builder_detail", kwargs={"form_def_id": form_def.id}))

        if closes_at <= opens_at:
            messages.error(request, "Close date must be after open date.")
            return redirect(reverse("staff_review:form_builder_detail", kwargs={"form_def_id": form_def.id}))

        window, created = SubmissionWindow.objects.update_or_create(
            form_definition=form_def,
            fiscal_year=fy,
            defaults={"opens_at": opens_at, "closes_at": closes_at},
        )
        action = "created" if created else "updated"
        messages.success(request, f"{fy} submission window {action} -- status: {window.get_status_display() if hasattr(window, 'get_status_display') else window.status}.")
        return redirect(reverse("staff_review:form_builder_detail", kwargs={"form_def_id": form_def.id}))


# ============================================================
# FORM SCOPING EDIT (CORE-22)
# ============================================================

class FormScopingEditView(FeatureRequiredMixin, StaffRequiredMixin, View):
    feature_key = "form_builder"

    """POST handler: update org-type scoping on a FormDefinition.

    Form fields:
      org_types[]   -- multi-select of OrgType values

    Idempotent: replaces the scope_to_org_types list outright.
    Explicit-org additions/removals are a separate UI (deferred).
    """

    def post(self, request, form_def_id):
        form_def = get_object_or_404(FormDefinition, pk=form_def_id)
        if not _user_can_manage(request.user, form_def):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied()

        org_types = request.POST.getlist("org_types")
        valid = {c[0] for c in OrgType.choices}
        org_types = [t for t in org_types if t in valid]

        scoping, _ = FormScoping.objects.update_or_create(
            form_definition=form_def,
            defaults={"scope_to_org_types": org_types},
        )

        count = scoping.in_scope_org_count()
        type_labels = [dict(OrgType.choices).get(t, t) for t in org_types]
        messages.success(
            request,
            f"Org scoping updated: {', '.join(type_labels) or '(none)'} "
            f"-- now {count} org{'s' if count != 1 else ''} in scope.",
        )
        return redirect(reverse("staff_review:form_builder_detail", kwargs={"form_def_id": form_def.id}))


# ============================================================
# PUBLISH NEW VERSION (CORE-23, CORE-24)
# ============================================================

class PublishNewVersionView(FeatureRequiredMixin, StaffRequiredMixin, TemplateView):
    feature_key = "form_builder"

    """GET: render the publish form. POST: execute the publish service.

    The form shows the proposed new version (defaults to source's
    bumped-minor), the impact (count of in-progress submissions that
    will be auto-closed), and inheritance toggles for scoping + window.
    """

    template_name = "staff_review/form_builder_publish.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        fd_id = kwargs.get("form_def_id")
        form_def = get_object_or_404(FormDefinition, pk=fd_id)

        if not _user_can_manage(self.request.user, form_def):
            messages.error(
                self.request,
                f"You are not assigned to manage forms in the "
                f"{form_def.program.code if form_def.program else '(unscoped)'} program.",
            )

        try:
            default_minor = bump_minor(str(form_def.variant))
        except PublishError:
            default_minor = ""
        try:
            default_major = bump_major(str(form_def.variant))
        except PublishError:
            default_major = ""

        affected_count = FormEntry.objects.filter(
            form_definition=form_def, status__in=IN_PROGRESS_STATUSES,
        ).count()

        has_scoping = hasattr(form_def, "scoping")
        has_current_fy_window = form_def.submission_windows.filter(fiscal_year="FY26").exists()

        from form_manager.services import schema_editor as se

        ctx.update({
            "user": USER,
            "form_def": form_def,
            "can_manage": _user_can_manage(self.request.user, form_def),
            "default_minor": default_minor,
            "default_major": default_major,
            "affected_count": affected_count,
            "has_scoping": has_scoping,
            "has_current_fy_window": has_current_fy_window,
            # STAFF-MP-14: flag that publishing will consume an unpublished draft.
            "has_draft": se.has_draft(form_def),
        })
        return ctx

    def post(self, request, form_def_id):
        form_def = get_object_or_404(FormDefinition, pk=form_def_id)
        if not _user_can_manage(request.user, form_def):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied()

        new_variant = (request.POST.get("new_variant") or "").strip()
        notes = (request.POST.get("notes") or "").strip()
        clone_scoping = request.POST.get("clone_scoping") == "on"
        clone_window = request.POST.get("clone_window") == "on"

        try:
            new_fd, affected = publish_new_version(
                source_form_def=form_def,
                new_variant=new_variant,
                actor=request.user if request.user.is_authenticated else None,
                notes=notes,
                clone_scoping=clone_scoping,
                clone_current_window=clone_window,
            )
        except PublishError as e:
            messages.error(request, str(e))
            return redirect(reverse(
                "staff_review:form_builder_publish",
                kwargs={"form_def_id": form_def.id},
            ))

        toast = (
            f"Published {new_fd.name} v{new_fd.variant}. "
            f"Previous version v{form_def.variant} deprecated. "
            + (f"{affected} in-progress submission{'s' if affected != 1 else ''} auto-closed."
               if affected else "No in-progress submissions affected.")
        )
        messages.success(request, toast)
        return redirect(reverse(
            "staff_review:form_builder_detail", kwargs={"form_def_id": new_fd.id},
        ))


# ============================================================
# VISUAL FIELD EDITOR (STAFF-MP-14)
# ============================================================
class FormBuilderEditView(FeatureRequiredMixin, StaffRequiredMixin, View):
    """Non-technical drag-free field editor for schema-driven forms.

    GET  -> render the editor against the current draft (seeded from the
            published schema on first visit).
    POST -> dispatch on `action`, mutate the draft via schema_editor, lint,
            persist, and redirect back (post/redirect/get).

    All edits land on `FormDefinition.draft_schema`; the published `schema`
    (and therefore every existing submission) is untouched until the staff
    user clicks "Publish new version".
    """

    feature_key = "form_builder"

    def _load(self, request, form_def_id):
        form_def = get_object_or_404(FormDefinition, pk=form_def_id)
        if not _user_can_manage(request.user, form_def):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied()
        # Editor only applies to schema-driven (formspec) forms.
        if not (isinstance(form_def.schema, dict) and form_def.schema.get("$formspec")):
            raise Http404("This form is not schema-driven and can't be edited field-by-field.")
        return form_def

    def get(self, request, form_def_id):
        from form_manager.services import schema_editor as se

        form_def = self._load(request, form_def_id)
        draft = se.get_draft_schema(form_def)

        # Build a display model so the template stays logic-light.
        sections = []
        for s in se.sections(draft):
            fields = []
            for child in s.get("children", []) or []:
                if child.get("type") == "field":
                    fields.append({
                        "key": child["key"],
                        "label": child.get("label", ""),
                        "type_key": se.field_type_of(child),
                        "type_label": se.field_type_label(se.field_type_of(child)),
                        "help": se.field_help(child),
                        "option_set": child.get("optionSet", ""),
                        "is_field": True,
                    })
                else:
                    # display / non-field items rendered read-only.
                    fields.append({
                        "key": child.get("key", ""),
                        "label": child.get("label", ""),
                        "type_label": "Instructional text",
                        "is_field": False,
                    })
            sections.append({
                "key": s["key"],
                "label": s.get("label", ""),
                "fields": fields,
            })

        ctx = {
            "user": USER,
            "form_def": form_def,
            "sections": sections,
            "field_types": se.FIELD_TYPES,
            "option_sets": se.option_set_keys(draft),
            "draft_pending": se.has_draft(form_def),
            "draft_updated_at": form_def.draft_updated_at,
            "can_manage": _user_can_manage(request.user, form_def),
        }
        from django.shortcuts import render
        return render(request, "staff_review/form_builder_edit.html", ctx)

    def post(self, request, form_def_id):
        from form_manager.services import schema_editor as se

        form_def = self._load(request, form_def_id)
        action = (request.POST.get("action") or "").strip()
        p = request.POST.get
        back = redirect(reverse(
            "staff_review:form_builder_edit", kwargs={"form_def_id": form_def.id},
        ))

        # Discard short-circuits -- no schema mutation.
        if action == "discard_draft":
            se.discard_draft(form_def)
            messages.success(request, "Draft changes discarded. Back to the published form.")
            return back

        draft = se.get_draft_schema(form_def)
        section_key = (p("section_key") or "").strip()
        field_key = (p("field_key") or "").strip()

        if action == "add_field":
            draft = se.add_field(
                draft, section_key,
                label=p("label") or "Untitled field",
                type_key=p("field_type") or "short_text",
                help_text=p("help") or "",
                option_set=p("option_set") or "",
            )
            note = "Field added."
        elif action == "update_field":
            draft = se.update_field(
                draft, section_key, field_key,
                label=p("label") or "Untitled field",
                type_key=p("field_type") or "short_text",
                help_text=p("help") or "",
                option_set=p("option_set") or "",
            )
            note = "Field updated."
        elif action == "remove_field":
            draft = se.remove_field(draft, section_key, field_key)
            note = "Field removed."
        elif action == "move_field":
            draft = se.move_field(draft, section_key, field_key, p("direction") or "up")
            note = "Field moved."
        elif action == "add_section":
            draft = se.add_section(draft, p("label") or "New section")
            note = "Section added."
        elif action == "update_section":
            draft = se.update_section(draft, section_key, p("label") or "")
            note = "Section renamed."
        elif action == "remove_section":
            draft = se.remove_section(draft, section_key)
            note = "Section removed."
        elif action == "move_section":
            draft = se.move_section(draft, section_key, p("direction") or "up")
            note = "Section moved."
        else:
            messages.error(request, f"Unknown action: {action!r}")
            return back

        ok, report = se.save_draft(form_def, draft, user=request.user)
        if not ok:
            first = report.errors[0].message if report.errors else "unknown error"
            messages.error(request, f"Couldn't save that change: {first}")
        else:
            messages.success(request, note)
        return back
