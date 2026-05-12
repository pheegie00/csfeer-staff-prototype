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

ORGANIZATION_DATA = [
    ("Eastern Pequot Tribal Nation", "Connecticut"),
    ("Passamaquoddy Tribe - Pleasant Point", "Maine"),
    ("Mashpee Wampanoag Tribe", "Massachusetts"),
    ("Narragansett Indian Tribe", "Rhode Island"),
    ("Central Council of Tlingit and Haida Indian Tribes of Alaska", "Alaska"),
    ("Cook Inlet Tribal Council, Inc.", "Alaska"),
    ("Fairbanks Native Association", "Alaska"),
    ("Kawerak, Inc.", "Alaska"),
    ("Kenaitze Indian Tribe", "Alaska"),
    ("Kodiak Area Native Association", "Alaska"),
    ("Sitka Tribe of Alaska", "Alaska"),
    ("Sun'aq Tribe of Kodiak", "Alaska"),
    ("Tanana Chiefs Conference", "Alaska"),
    ("Shoshone-Bannock Tribes of the Fort Hall Reservation", "Idaho"),
    ("Confederated Tribes of Grand Ronde", "Oregon"),
    ("Klamath Indian Tribes", "Oregon"),
    ("Lummi Nation", "Washington"),
    ("Nooksack Indian Tribe", "Washington"),
    ("South Puget Intertribal Planning Agency", "Washington"),
    ("Suquamish Indian Tribe of the Port Madison Reservation", "Washington"),
    ("Swinomish Indian Tribal Community", "Washington"),
    ("Ma-Chis Lower Creek Indian Tribe", "Alabama"),
    ("Mowa Band of Choctaw Indians", "Alabama"),
    ("Poarch Band of Creek Indians", "Alabama"),
    ("Coharie Intra-Tribal Council, Inc.", "North Carolina"),
    ("Lumbee Tribe of North Carolina", "North Carolina"),
    ("Catawba Indian Nation", "South Carolina"),
    ("Inter-Tribal Council of Michigan, Inc.", "Michigan"),
    ("Keweenaw Bay Indian Community of Michigan", "Michigan"),
    ("Sault Ste. Marie Tribe of Chippewa Indians", "Michigan"),
    ("Institute for Indian Development", "Louisiana"),
    ("Pueblo of Jemez", "New Mexico"),
    ("Pueblo of Zuni", "New Mexico"),
    ("Cherokee Nation", "Oklahoma"),
    ("Cheyenne and Arapaho Tribes of Oklahoma", "Oklahoma"),
    ("Chickasaw Nation", "Oklahoma"),
    ("Choctaw Nation of Oklahoma", "Oklahoma"),
    ("Citizen Potawatomi Nation", "Oklahoma"),
    ("Delaware Nation of Oklahoma", "Oklahoma"),
    ("Kaw Nation", "Oklahoma"),
    ("Osage Nation of Oklahoma", "Oklahoma"),
    ("Pawnee Nation of Oklahoma", "Oklahoma"),
    ("Quapaw Tribe of Oklahoma", "Oklahoma"),
    ("Seminole Nation of Oklahoma", "Oklahoma"),
    ("United Keetoowah Band of Cherokee Indians in Oklahoma", "Oklahoma"),
    ("Wichita and Affiliated Tribes", "Oklahoma"),
    ("Wyandotte Nation", "Oklahoma"),
    ("Alabama-Coushatta Tribe of Texas", "Texas"),
    ("Ponca Tribe of Nebraska", "Nebraska"),
    ("Blackfeet Nation", "Montana"),
    ("Chippewa Cree Tribe of the Rocky Boy's Reservation", "Montana"),
    ("Confederated Salish and Kootenai Tribes", "Montana"),
    ("Fort Belknap Indian Community", "Montana"),
    ("Fort Peck Assiniboine and Sioux Tribes", "Montana"),
    ("Spirit Lake Tribe", "North Dakota"),
    ("Turtle Mountain Band of Chippewa Indians", "North Dakota"),
    ("Oglala Sioux Tribe", "South Dakota"),
    ("Rosebud Sioux Tribe", "South Dakota"),
    ("Sisseton Wahpeton Oyate of the Lake Traverse Reservation", "South Dakota"),
    ("Yankton Sioux Tribe", "South Dakota"),
    ("Northern Arapaho Tribe", "Wyoming"),
    ("Navajo Nation", "Arizona"),
    ("Quechan Indian Tribe", "Arizona"),
    ("San Carlos Apache Tribe", "Arizona"),
    ("White Mountain Apache Tribe", "Arizona"),
]


def populate_organizations(apps, schema_editor):
    OrganizationProfile = apps.get_model("organizations", "OrganizationProfile")
    State = apps.get_model("organizations", "State")

    state_cache = {}
    for org_name, state_name in ORGANIZATION_DATA:
        code = STATE_NAME_TO_CODE[state_name]
        if code not in state_cache:
            state_cache[code] = State.objects.get(code=code)
        OrganizationProfile.objects.get_or_create(
            name=org_name,
            defaults={"state": state_cache[code]},
        )


def depopulate_organizations(apps, schema_editor):
    OrganizationProfile = apps.get_model("organizations", "OrganizationProfile")
    names = [name for name, _ in ORGANIZATION_DATA]
    OrganizationProfile.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0007_organizationprofile_state"),
    ]

    operations = [
        migrations.RunPython(populate_organizations, reverse_code=depopulate_organizations),
    ]
