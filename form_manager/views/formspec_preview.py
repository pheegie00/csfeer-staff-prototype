"""Formspec-driven recipient-side form rendering (STAFF-MP-13 Phase 2 + 3).

This is a PARALLEL recipient route to the existing multi-step
form_edit pipeline. It does not replace form_edit. Instead it gives
us a single-page Formspec-rendered version of any FormDefinition
whose `schema` field holds a real formspec doc (today: just the
CSBG Tribal Plan, populated by seed_demo_data).

Why a parallel route:
  - form_edit is a deep pipeline (multi-step navigation, page-level
    save/resume, Pydantic schema execution) that the upstream csfeer
    team built. Replacing it wholesale is multi-day work and high
    risk for the prototype.
  - A parallel route ships in hours and gives us a real end-to-end
    Formspec demo. Once the team is happy with how Formspec renders,
    we can graduate it to the canonical recipient route.

GET  /forms/<entry_id>/formspec-preview/
       Renders the Formspec web component, hydrated with the spec
       from FormDefinition.schema and any saved FormEntry.data.

POST /forms/<entry_id>/formspec-preview/
       Receives a JSON payload (the response), validates it through
       formspec-py (Phase 3 -- defense in depth), and persists to
       FormEntry.data. Returns JSON with validation result.

Both gated by the `formspec_runtime` feature flag and login.
"""

import json

from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from form_manager.models import FormDefinition, FormEntry
from form_manager.services.formspec_service import (
    lint_definition,
    validate_response,
)
from staff_review.feature_flags import is_enabled


@login_required
def formspec_preview(request, pk):
    """Render the Formspec web component for a FormEntry, or accept a submit."""
    if not is_enabled("form_runtime"):
        raise Http404("Form runtime is disabled.")

    entry = get_object_or_404(FormEntry.objects.select_related("form_definition", "organization"), pk=pk)
    spec = entry.form_definition.schema or {}

    if not isinstance(spec, dict) or not spec.get("$formspec"):
        raise Http404(
            "This form does not have a schema-driven definition yet. "
            "Only forms with a real spec in FormDefinition.schema can be rendered live."
        )

    # POST = submit the response payload
    if request.method == "POST":
        return _accept_submit(request, entry, spec)

    # GET = render the form
    lint_report = lint_definition(spec, mode="strict")
    return render(request, "form_manager/formspec_preview.html", {
        "entry": entry,
        "form_def": entry.form_definition,
        "spec_json": json.dumps(spec),
        "saved_data_json": json.dumps(entry.data or {}),
        "lint_clean": lint_report.is_clean,
        "lint_errors": lint_report.errors,
        "submit_url": request.build_absolute_uri(),
    })


@login_required
def formspec_draft_preview(request, form_def_id):
    """Render the DRAFT schema of a FormDefinition (STAFF-MP-14).

    Read-only preview so staff can see in-progress field edits the way a
    recipient would, before publishing. No FormEntry exists, so there's
    nothing to save -- the template hides the save button when
    `draft_preview` is set.
    """
    if not is_enabled("form_runtime"):
        raise Http404("Form runtime is disabled.")

    form_def = get_object_or_404(FormDefinition, pk=form_def_id)

    # Prefer the draft; fall back to the published schema if no draft yet.
    spec = form_def.draft_schema if form_def.draft_schema is not None else (form_def.schema or {})
    if not isinstance(spec, dict) or not spec.get("$formspec"):
        raise Http404("This form does not have a schema-driven definition yet.")

    return render(request, "form_manager/formspec_preview.html", {
        "entry": None,
        "form_def": form_def,
        "spec_json": json.dumps(spec),
        "saved_data_json": json.dumps({}),
        "lint_clean": True,
        "lint_errors": [],
        "submit_url": "",
        "draft_preview": True,
    })


@method_decorator(csrf_exempt, name="dispatch")
def _accept_submit(request, entry, spec):
    """Handle POST of a Formspec response payload.

    Phase 3: re-validate server-side via formspec-py. This is defense in
    depth -- the web component already validated client-side, but we
    never trust the client.
    """
    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError as exc:
        return JsonResponse({"ok": False, "error": f"Invalid JSON: {exc}"}, status=400)

    data = payload.get("data", payload)  # accept either {data: {...}} or {...}
    result = validate_response(spec, data)

    # Persist the normalized data even if validation reports issues -- the
    # prototype treats this as a draft save, not a final submit. Real CORE
    # would split draft-save from final-submit and only allow final on valid.
    entry.data = result.data or data
    entry.save(update_fields=["data", "updated_at"])

    return JsonResponse({
        "ok": True,
        "valid": result.valid,
        "item_count": result.item_count,
        "message": (
            "Saved. Response is fully valid."
            if result.valid
            else "Saved as draft. Response has validation gaps; review before submitting."
        ),
    })
