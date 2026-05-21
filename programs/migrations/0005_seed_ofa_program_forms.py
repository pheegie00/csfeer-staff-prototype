"""Seed placeholder form templates for OFA programs.

The Phase II migration (0004) attributed all newly-seeded forms to OCS
programs. With per-office admin roles landing in this batch (Phase 4
Step 7), an OFA-scoped Program Admin would log in to an empty Form
Builder list -- there are TANF / Tribal TANF / HMRF / HPOG programs
but no FormDefinitions hung off them.

This migration adds 8 placeholder OFA forms so the OFA admin view is
meaningful for demo / testing. Schemas remain `{}` -- design work for
OFA forms is out of scope for this prototype.

Like 0004, this is purely additive seed data:
- FormDefinitions get realistic OMB families + sensible cycle_types
- Each gets a FormScoping with org_types matching the program's
  recipient mix (TANF = state + territory, Tribal TANF = tribe, etc.)
- FY26 submission windows demonstrate Open / Upcoming / Past Due
"""

from datetime import datetime, timezone as dt_tz

from django.db import migrations


# (form_def_name, family_omb, cycle_type, org_types_in_scope, program_code,
#  fy26_window_opens, fy26_window_closes_or_None)
OFA_FORM_DEFINITIONS = [
    # ===== TANF =====
    ("TANF ACF-196R Financial Report", "0970-0338", "quarterly",
     ["state", "territory"], "TANF",
     datetime(2026, 1, 1, tzinfo=dt_tz.utc), datetime(2026, 1, 31, 23, 59, tzinfo=dt_tz.utc)),
    ("TANF ACF-199 Data Report", "0970-0338", "quarterly",
     ["state", "territory"], "TANF",
     datetime(2026, 4, 1, tzinfo=dt_tz.utc), datetime(2026, 5, 15, 23, 59, tzinfo=dt_tz.utc)),
    ("TANF MOE Annual Report", "0970-0338", "annual",
     ["state", "territory"], "TANF",
     datetime(2026, 10, 1, tzinfo=dt_tz.utc), datetime(2026, 12, 31, 23, 59, tzinfo=dt_tz.utc)),

    # ===== Tribal TANF =====
    ("Tribal TANF Data Report (ACF-343)", "0970-0345", "quarterly",
     ["tribe", "tribal_org"], "TRIBAL_TANF",
     datetime(2026, 4, 1, tzinfo=dt_tz.utc), datetime(2026, 5, 15, 23, 59, tzinfo=dt_tz.utc)),
    ("Tribal TANF Plan", "0970-0345", "ad_hoc",
     ["tribe", "tribal_org"], "TRIBAL_TANF",
     None, None),

    # ===== HMRF =====
    ("HMRF Performance Progress Report", "0970-0460", "annual",
     ["cbo", "faith_based", "tribe", "workforce_agency", "higher_ed"], "HMRF",
     datetime(2026, 10, 1, tzinfo=dt_tz.utc), datetime(2026, 11, 30, 23, 59, tzinfo=dt_tz.utc)),
    ("HMRF Final Performance Report", "0970-0460", "ad_hoc",
     ["cbo", "faith_based", "tribe", "workforce_agency", "higher_ed"], "HMRF",
     None, None),

    # ===== HPOG (dormant) =====
    ("HPOG Performance Progress Report", "0970-0394", "annual",
     ["higher_ed", "workforce_agency", "tribe", "state", "cbo"], "HPOG",
     None, None),
]


def seed_ofa_forms(apps, schema_editor):
    Program = apps.get_model("programs", "Program")
    FormDefinition = apps.get_model("form_manager", "FormDefinition")
    SubmissionWindow = apps.get_model("programs", "SubmissionWindow")
    FormScoping = apps.get_model("programs", "FormScoping")

    prog_by_code = {p.code: p for p in Program.objects.all()}

    for (name, family, cycle, org_types, program_code,
         opens, closes) in OFA_FORM_DEFINITIONS:
        program = prog_by_code.get(program_code)
        if program is None:
            continue

        fd, _ = FormDefinition.objects.get_or_create(
            name=name, variant="1.0.0",
            defaults={
                "family": family,
                "description": f"Seeded form template for {program_code}: {name}.",
                "schema": {},
                "schema_class": f"{program_code.replace('-', '_')}_{name.split()[0]}_Schema",
                "is_active": True,
                "program": program,
                "cycle_type": cycle,
            },
        )
        # Idempotent attribution
        if fd.program_id != program.id:
            fd.program = program
            fd.save(update_fields=["program"])

        # Scoping (1:1)
        FormScoping.objects.update_or_create(
            form_definition=fd,
            defaults={"scope_to_org_types": list(org_types)},
        )

        # FY26 submission window if defined
        if opens is not None and closes is not None:
            SubmissionWindow.objects.update_or_create(
                form_definition=fd, fiscal_year="FY26",
                defaults={"opens_at": opens, "closes_at": closes},
            )


def reverse_seed(apps, schema_editor):
    # No-op: avoid cascading data loss on rollback.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("programs", "0004_seed_other_ocs_programs_and_phase_ii_forms"),
        ("form_manager", "0010_extend_form_name_choices_for_ofa"),
    ]

    operations = [
        migrations.RunPython(seed_ofa_forms, reverse_seed),
    ]
