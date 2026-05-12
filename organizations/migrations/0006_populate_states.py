from django.db import migrations

STATE_NAME_TO_CODE = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Connecticut": "CT",
    "Idaho": "ID",
    "Louisiana": "LA",
    "Maine": "ME",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Montana": "MT",
    "Nebraska": "NE",
    "New Mexico": "NM",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Texas": "TX",
    "Washington": "WA",
    "Wyoming": "WY",
}

STATE_REGION_DATA = [
    ("Connecticut", "Region 1"),
    ("Maine", "Region 1"),
    ("Massachusetts", "Region 1"),
    ("Rhode Island", "Region 1"),
    ("Alaska", "Region 10"),
    ("Idaho", "Region 10"),
    ("Oregon", "Region 10"),
    ("Washington", "Region 10"),
    ("Alabama", "Region 4"),
    ("North Carolina", "Region 4"),
    ("South Carolina", "Region 4"),
    ("Michigan", "Region 5"),
    ("Louisiana", "Region 6"),
    ("New Mexico", "Region 6"),
    ("Oklahoma", "Region 6"),
    ("Texas", "Region 6"),
    ("Nebraska", "Region 7"),
    ("Montana", "Region 8"),
    ("North Dakota", "Region 8"),
    ("South Dakota", "Region 8"),
    ("Wyoming", "Region 8"),
    ("Arizona", "Region 9"),
]


def populate_states(apps, schema_editor):
    State = apps.get_model("organizations", "State")
    for state_name, region in STATE_REGION_DATA:
        State.objects.get_or_create(
            code=STATE_NAME_TO_CODE[state_name],
            defaults={"region": region},
        )


def depopulate_states(apps, schema_editor):
    State = apps.get_model("organizations", "State")
    codes = [STATE_NAME_TO_CODE[name] for name, _ in STATE_REGION_DATA]
    State.objects.filter(code__in=codes).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0005_alter_userorganizationmembership_user_state"),
    ]

    operations = [
        migrations.RunPython(populate_states, reverse_code=depopulate_states),
    ]
