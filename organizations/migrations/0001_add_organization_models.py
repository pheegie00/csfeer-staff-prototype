import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("form_manager", "0002_remove_redundant_timestamp_fields"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name="OrganizationProfile",
                    fields=[
                        (
                            "id",
                            models.UUIDField(
                                default=uuid.uuid4,
                                editable=False,
                                primary_key=True,
                                serialize=False,
                            ),
                        ),
                        ("created_at", models.DateTimeField(auto_now_add=True)),
                        ("updated_at", models.DateTimeField(auto_now=True)),
                        ("name", models.CharField(max_length=255)),
                        ("address", models.TextField(blank=True)),
                        ("contact_email", models.EmailField(blank=True, max_length=254)),
                        ("contact_phone", models.CharField(blank=True, max_length=30)),
                    ],
                    options={
                        "abstract": False,
                    },
                ),
                migrations.CreateModel(
                    name="UserOrganizationMembership",
                    fields=[
                        (
                            "id",
                            models.UUIDField(
                                default=uuid.uuid4,
                                editable=False,
                                primary_key=True,
                                serialize=False,
                            ),
                        ),
                        ("created_at", models.DateTimeField(auto_now_add=True)),
                        ("updated_at", models.DateTimeField(auto_now=True)),
                        (
                            "role",
                            models.CharField(
                                choices=[
                                    ("admin", "Administrator"),
                                    ("editor", "Editor"),
                                    ("viewer", "Viewer"),
                                ],
                                default="editor",
                                max_length=20,
                            ),
                        ),
                        (
                            "organization",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                to="organizations.organizationprofile",
                            ),
                        ),
                        (
                            "user",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                to=settings.AUTH_USER_MODEL,
                            ),
                        ),
                    ],
                    options={
                        "unique_together": {("user", "organization")},
                    },
                ),
            ],
            database_operations=[
                migrations.RunSQL(
                    sql="ALTER TABLE form_manager_organizationprofile RENAME TO organizations_organizationprofile",
                    reverse_sql="ALTER TABLE organizations_organizationprofile RENAME TO form_manager_organizationprofile",
                ),
                migrations.RunSQL(
                    sql="ALTER TABLE form_manager_userorganizationmembership RENAME TO organizations_userorganizationmembership",
                    reverse_sql="ALTER TABLE organizations_userorganizationmembership RENAME TO form_manager_userorganizationmembership",
                ),
            ],
        ),
    ]
