"""Seed the 5 known ACF programs + backfill existing FormDefinitions to CSBG.

Data migration -- runs after the program/office tables are created
(0001_initial). Safe to re-run on existing databases; uses get_or_create.

If/when more programs come online (e.g., a new HMRF cycle, a Tribal TANF
+ Child Welfare Coordination NOFO), add them as separate data
migrations rather than mutating this one -- migrations are immutable
once shipped.
"""

from django.db import migrations


SEED = [
    # (office_code, office_name, [(program_code, program_name, is_active), ...])
    ("OCS", "Office of Community Services", [
        ("CSBG", "Community Services Block Grant", True),
    ]),
    ("OFA", "Office of Family Assistance", [
        ("TANF", "Temporary Assistance for Needy Families", True),
        ("TRIBAL_TANF", "Tribal TANF", True),
        ("HMRF", "Healthy Marriage and Responsible Fatherhood", True),
        ("HPOG", "Health Profession Opportunity Grants", False),  # dormant
    ]),
]


def seed_programs(apps, schema_editor):
    ACFOffice = apps.get_model("programs", "ACFOffice")
    Program = apps.get_model("programs", "Program")
    FormDefinition = apps.get_model("form_manager", "FormDefinition")

    # 1. Offices + programs
    csbg = None
    for office_code, office_name, programs in SEED:
        office, _ = ACFOffice.objects.get_or_create(
            code=office_code, defaults={"name": office_name},
        )
        for program_code, program_name, is_active in programs:
            prog, _ = Program.objects.get_or_create(
                code=program_code,
                defaults={"name": program_name, "office": office, "is_active": is_active},
            )
            if program_code == "CSBG":
                csbg = prog

    # 2. Backfill: every existing FormDefinition with program=NULL -> CSBG
    if csbg:
        FormDefinition.objects.filter(program__isnull=True).update(program=csbg)


def reverse_seed(apps, schema_editor):
    # No-op on reverse -- programs may have downstream FKs we don't want
    # to cascade-delete. Manual cleanup if you really need to roll back.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("programs", "0001_initial"),
        ("form_manager", "0008_formdefinition_cycle_type_formdefinition_is_shared_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_programs, reverse_seed),
    ]
