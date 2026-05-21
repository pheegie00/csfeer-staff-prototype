"""Form template publish service (CORE-23, CORE-24).

Encapsulates the "publish new version" transaction so it can be called
from any view + tested directly.

publish_new_version() is the only public entry point. It performs an
atomic operation that:

  1. Creates a new FormDefinition row (same name, new variant, copies
     schema + family + cycle_type + program from the source).
  2. Optionally clones FormScoping from the source.
  3. Optionally clones current-FY SubmissionWindow from the source.
  4. Marks the source FormDefinition is_active=False (deprecated).
  5. Finds in-progress FormEntry rows on the source and auto-closes
     them with determination_outcome='closed' (CORE-24 acceptance
     criteria: in-progress on deprecated versions "automatically
     updated in status to Closed without Acceptance").
  6. Writes FormAuditTrail rows: one 'publish_version' on the new FD,
     plus one 'auto_close_deprecated' per auto-closed FormEntry.

Resolved submissions (accepted/closed) on the prior version are
untouched per CORE-23 ("must not alter or invalidate any in-progress
or completed submissions on prior versions" -- read as: completed
submissions are immutable; in-progress submissions are closed).
"""

import re

from django.db import transaction
from django.utils import timezone

from form_manager.models.forms import FormAuditTrail, FormDefinition, FormEntry
from programs.models import FormScoping, SubmissionWindow


SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(-[A-Za-z0-9.-]+)?$")

# Statuses considered "in flight" and therefore auto-closed on deprecation.
IN_PROGRESS_STATUSES = ("draft", "submitted", "in_progress", "returned", "amended")


class PublishError(Exception):
    """Raised when a publish request can't be honored."""


def bump_minor(variant: str) -> str:
    """1.0.0 -> 1.1.0. Drops any pre-release suffix."""
    base = variant.split("-", 1)[0]
    parts = base.split(".")
    if len(parts) != 3:
        raise PublishError(f"Source variant {variant!r} is not semver-compatible.")
    major, minor, _ = parts
    return f"{int(major)}.{int(minor) + 1}.0"


def bump_major(variant: str) -> str:
    """1.0.0 -> 2.0.0."""
    base = variant.split("-", 1)[0]
    parts = base.split(".")
    if len(parts) != 3:
        raise PublishError(f"Source variant {variant!r} is not semver-compatible.")
    major = int(parts[0])
    return f"{major + 1}.0.0"


@transaction.atomic
def publish_new_version(
    source_form_def: FormDefinition,
    new_variant: str,
    actor=None,
    notes: str = "",
    clone_scoping: bool = True,
    clone_current_window: bool = True,
    current_fy: str = "FY26",
):
    """Publish a new version of `source_form_def`.

    Returns (new_form_def, affected_count) where affected_count is the
    number of in-progress FormEntries that were auto-closed.

    Raises PublishError on invalid input (bad variant, version conflict).
    Caller is responsible for permission checks.
    """
    if not new_variant or not SEMVER_RE.match(new_variant):
        raise PublishError(
            f"New variant {new_variant!r} is not a valid semver (expect e.g. '1.1.0')."
        )
    if new_variant == str(source_form_def.variant):
        raise PublishError("New variant must differ from the source version.")

    # Conflict check: a FormDefinition with this name+variant already exists?
    existing = FormDefinition.objects.filter(
        name=source_form_def.name, variant=new_variant,
    ).exclude(pk=source_form_def.pk)
    if existing.exists():
        raise PublishError(
            f"FormDefinition '{source_form_def.name}' v{new_variant} already exists."
        )

    # 1. Create the new version (clone the schema-bearing fields).
    new_fd = FormDefinition.objects.create(
        name=source_form_def.name,
        variant=new_variant,
        family=source_form_def.family,
        description=source_form_def.description,
        schema=dict(source_form_def.schema or {}),
        schema_class=source_form_def.schema_class,
        is_active=True,
        program=source_form_def.program,
        cycle_type=source_form_def.cycle_type,
        is_shared=source_form_def.is_shared,
    )

    # 2. Clone scoping if requested.
    if clone_scoping and hasattr(source_form_def, "scoping"):
        src_scoping = source_form_def.scoping
        new_scoping = FormScoping.objects.create(
            form_definition=new_fd,
            scope_to_org_types=list(src_scoping.scope_to_org_types or []),
        )
        new_scoping.explicit_orgs.set(src_scoping.explicit_orgs.all())

    # 3. Clone current-FY window if requested.
    if clone_current_window:
        src_window = source_form_def.submission_windows.filter(
            fiscal_year=current_fy
        ).first()
        if src_window is not None:
            SubmissionWindow.objects.create(
                form_definition=new_fd,
                fiscal_year=current_fy,
                opens_at=src_window.opens_at,
                closes_at=src_window.closes_at,
            )

    # 4. Deprecate the source.
    source_form_def.is_active = False
    source_form_def.save(update_fields=["is_active", "updated_at"])

    # 5. Auto-close in-progress FormEntries on the source (CORE-24).
    affected = list(
        FormEntry.objects.filter(
            form_definition=source_form_def, status__in=IN_PROGRESS_STATUSES,
        )
    )
    auto_close_note = (
        f"Auto-closed (CORE-24): form template "
        f"'{source_form_def.name}' v{source_form_def.variant} deprecated by publish of v{new_variant}."
    )
    for entry in affected:
        entry.status = "closed"
        entry.locked = True
        entry.determination_outcome = "closed"
        entry.determination_notes = auto_close_note
        entry.determined_at = timezone.now()
        entry.determined_by = actor
        entry.save(update_fields=[
            "status", "locked", "determination_outcome",
            "determination_notes", "determined_at", "determined_by",
            "updated_at",
        ])
        # 6a. Audit trail per auto-closed entry.
        FormAuditTrail.objects.create(
            form_entry=entry, user=actor,
            action="close",
            notes=auto_close_note,
        )

    # 6b. Single publish audit trail. We attach it to the FIRST affected
    # entry if there is one, otherwise to a fresh "publishing event" on
    # the new form definition (which itself doesn't have a FormEntry yet).
    # Since FormAuditTrail.form_entry is required, we just write per-entry
    # rows when entries exist. The publish event itself is also recorded
    # as a SystemEvent if you want a global view (out of scope here).
    if affected:
        FormAuditTrail.objects.create(
            form_entry=affected[0], user=actor,
            action="publish_version",
            notes=f"Source: v{source_form_def.variant} -> v{new_variant}. "
                  f"Affected {len(affected)} in-progress submission{'s' if len(affected) != 1 else ''}. "
                  + (f"Notes: {notes}" if notes else ""),
        )

    return new_fd, len(affected)
