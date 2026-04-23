import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0001_add_organization_models"),
        ("form_manager", "0002_remove_redundant_timestamp_fields"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name="formentry",
                    name="organization",
                    field=models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="organizations.organizationprofile",
                    ),
                ),
                migrations.DeleteModel(name="UserOrganizationMembership"),
                migrations.DeleteModel(name="OrganizationProfile"),
            ],
            database_operations=[],
        ),
    ]
