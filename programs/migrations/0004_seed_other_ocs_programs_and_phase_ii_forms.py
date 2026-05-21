"""Seed Phase II CSBG state/territory forms + 6 other OCS programs.

Per PWS p9 (D01 FA - Attachment 1 - PWS CSFEER_v2.pdf):
    Phase II: scaling up to states and territories. Forms include:
      - CSBG Eligible Entity List
      - CSBG State and Territory Plan
      - CSBG Annual Report 3.0 (states variant)

User direction (May 2026): also add sample data for the other OCS
programs so the Form Templates view reflects the full OCS portfolio:
    LIHEAP, LIHWAP, AFI (dormant), CED, RCD, SSBG.

This migration is purely additive seed data. FormDefinitions get
realistic OMB-derived families, sensible cycle_types, basic
scope_to_org_types matching each program's recipient mix, and FY26
submission windows that demonstrate Open / Upcoming / Past Due states.

Schemas are placeholders ({}) pending design work referenced from the
original CSBG Tribal Plan Figma. The Form Builder UI will surface
each template so program admins can review the lifecycle metadata
while the schemas evolve.
"""

from datetime import datetime, timezone as dt_tz

from django.db import migrations


# (program_code, program_name, description, is_active)
NEW_PROGRAMS = [
    ("LIHEAP", "Low Income Home Energy Assistance Program",
     "Helps low-income households meet immediate home energy needs (heating, cooling, weatherization).", True),
    ("LIHWAP", "Low Income Household Water Assistance Program",
     "One-time funding to help low-income households with drinking water and wastewater costs.", True),
    ("AFI", "Assets for Independence",
     "Matched-savings IDA program for low-income individuals. Currently dormant; historical reports only.", False),
    ("CED", "Community Economic Development",
     "Discretionary grants to CDCs for job creation in low-income communities.", True),
    ("RCD", "Rural Community Development",
     "Technical assistance and training for rural communities lacking access to water and waste services.", True),
    ("SSBG", "Social Services Block Grant",
     "Flexible block grant to states for social services that prevent abuse, achieve self-sufficiency.", True),
]


# (form_def_name, family_omb, cycle_type, org_types_in_scope, program_code,
#  fy26_window_opens, fy26_window_closes_or_None)
NEW_FORM_DEFINITIONS = [
    # ===== CSBG Phase II (states / territories) =====
    ("CSBG State Plan", "0970-0382", "annual",
     ["state"], "CSBG",
     datetime(2026, 8, 1, tzinfo=dt_tz.utc), datetime(2026, 10, 31, 23, 59, tzinfo=dt_tz.utc)),
    ("CSBG Territory Plan", "0970-0382", "annual",
     ["territory"], "CSBG",
     datetime(2026, 8, 1, tzinfo=dt_tz.utc), datetime(2026, 10, 31, 23, 59, tzinfo=dt_tz.utc)),
    ("CSBG Annual Report 3.0 (States)", "0970-0492", "annual",
     ["state"], "CSBG",
     datetime(2026, 9, 1, tzinfo=dt_tz.utc), datetime(2026, 12, 31, 23, 59, tzinfo=dt_tz.utc)),
    ("CSBG Annual Report 3.0 (Eligible Entities)", "0970-0492", "annual",
     ["cbo", "state"], "CSBG",
     datetime(2026, 9, 1, tzinfo=dt_tz.utc), datetime(2026, 12, 31, 23, 59, tzinfo=dt_tz.utc)),
    ("CSBG Eligible Entity List", "0970-0408", "ad_hoc",
     ["state", "territory"], "CSBG",
     None, None),  # no fixed window -- updated as-needed

    # ===== LIHEAP =====
    ("LIHEAP Model State / Tribal Plan", "0970-0080", "annual",
     ["state", "territory", "tribe", "tribal_org"], "LIHEAP",
     datetime(2026, 6, 1, tzinfo=dt_tz.utc), datetime(2026, 9, 1, 23, 59, tzinfo=dt_tz.utc)),
    ("LIHEAP Performance Data Form", "0970-0080", "annual",
     ["state", "territory", "tribe", "tribal_org"], "LIHEAP",
     datetime(2026, 10, 1, tzinfo=dt_tz.utc), datetime(2026, 12, 31, 23, 59, tzinfo=dt_tz.utc)),
    ("LIHEAP Household Report", "0970-0080", "annual",
     ["state", "territory"], "LIHEAP",
     datetime(2026, 10, 1, tzinfo=dt_tz.utc), datetime(2027, 1, 31, 23, 59, tzinfo=dt_tz.utc)),

    # ===== LIHWAP =====
    ("LIHWAP Performance Data Form", "0970-0567", "annual",
     ["state", "territory", "tribe"], "LIHWAP",
     datetime(2026, 1, 1, tzinfo=dt_tz.utc), datetime(2026, 3, 31, 23, 59, tzinfo=dt_tz.utc)),
    ("LIHWAP Quarterly Drawdown Report", "0970-0567", "quarterly",
     ["state", "territory", "tribe"], "LIHWAP",
     datetime(2026, 4, 1, tzinfo=dt_tz.utc), datetime(2026, 4, 30, 23, 59, tzinfo=dt_tz.utc)),

    # ===== AFI (dormant) =====
    ("AFI Annual Report", "0970-0202", "annual",
     ["cbo", "tribal_org", "faith_based"], "AFI",
     None, None),
    ("AFI Project Application", "0970-0202", "ad_hoc",
     ["cbo", "tribal_org", "faith_based"], "AFI",
     None, None),

    # ===== CED =====
    ("CED Project Application", "0970-0386", "ad_hoc",
     ["cbo"], "CED",
     datetime(2026, 3, 1, tzinfo=dt_tz.utc), datetime(2026, 5, 30, 23, 59, tzinfo=dt_tz.utc)),
    ("CED Performance Progress Report", "0970-0386", "annual",
     ["cbo"], "CED",
     datetime(2026, 10, 1, tzinfo=dt_tz.utc), datetime(2026, 12, 31, 23, 59, tzinfo=dt_tz.utc)),
    ("CED Final Performance Report", "0970-0386", "ad_hoc",
     ["cbo"], "CED",
     None, None),

    # ===== RCD =====
    ("RCD Project Application", "0970-RCD", "ad_hoc",
     ["cbo", "tribal_org"], "RCD",
     datetime(2026, 4, 1, tzinfo=dt_tz.utc), datetime(2026, 5, 30, 23, 59, tzinfo=dt_tz.utc)),
    ("RCD Annual Performance Report", "0970-RCD", "annual",
     ["cbo", "tribal_org"], "RCD",
     datetime(2026, 10, 1, tzinfo=dt_tz.utc), datetime(2026, 12, 31, 23, 59, tzinfo=dt_tz.utc)),

    # ===== SSBG =====
    ("SSBG Annual Report (SF-PPR)", "0970-0234", "annual",
     ["state", "territory"], "SSBG",
     datetime(2026, 10, 1, tzinfo=dt_tz.utc), datetime(2026, 12, 31, 23, 59, tzinfo=dt_tz.utc)),
    ("SSBG Pre-Expenditure Report", "0970-0234", "annual",
     ["state", "territory"], "SSBG",
     datetime(2026, 7, 1, tzinfo=dt_tz.utc), datetime(2026, 8, 31, 23, 59, tzinfo=dt_tz.utc)),
]


def seed_programs_and_forms(apps, schema_editor):
    ACFOffice = apps.get_model("programs", "ACFOffice")
    Program = apps.get_model("programs", "Program")
    FormDefinition = apps.get_model("form_manager", "FormDefinition")
    SubmissionWindow = apps.get_model("programs", "SubmissionWindow")
    FormScoping = apps.get_model("programs", "FormScoping")

    ocs = ACFOffice.objects.get(code="OCS")

    # 1. Programs
    prog_by_code = {p.code: p for p in Program.objects.all()}
    for code, name, desc, active in NEW_PROGRAMS:
        if code not in prog_by_code:
            prog_by_code[code] = Program.objects.create(
                code=code, name=name, description=desc, office=ocs, is_active=active,
            )

    # 2. FormDefinitions + Scoping + Windows
    for (name, family, cycle, org_types, program_code,
         opens, closes) in NEW_FORM_DEFINITIONS:
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
        ("programs", "0003_formscoping_submissionwindow"),
        ("form_manager", "0009_alter_formdefinition_family_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_programs_and_forms, reverse_seed),
    ]
