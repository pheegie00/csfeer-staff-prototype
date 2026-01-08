from typing import cast

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from form_manager.models import (
    FormDefinition,
    OrganizationProfile,
    UserOrganizationMembership,
)
from form_manager.schema.forms.base import BaseFormSchema, SchemaValidationError
from form_manager.utils import get_form_definitions
from users.models import CoreUser


class Command(BaseCommand):
    help = "Load initial form definitions from official schemas"

    def add_arguments(self, parser):
        """Add arguments to the command"""

        parser.add_argument(
            "--force",
            action="store_true",
            default=False,
            help="Overwrite existing form schemas, even if one already exists",
        )

    def handle(self, *args, **options):

        force = options["force"]

        form_definitions = get_form_definitions()

        created = 0

        for definition in form_definitions:

            if type(definition) == BaseFormSchema:
                continue

            try:
                schema = definition.model_json_schema()
            except SchemaValidationError as err:
                self.stdout.write(self.style.ERROR(str(err)))
                continue

            def default_or_constraint(field_item):

                return field_item.get("const") or field_item.get("default")

            family = default_or_constraint(schema["properties"]["family"])
            variant = default_or_constraint(schema["properties"]["variant"])
            name = default_or_constraint(schema["properties"]["name"])

            if not force and FormDefinition.objects.filter(variant=variant, name=name).exists():
                self.stdout.write(
                    self.style.NOTICE(
                        f"A form definition named {name} with variant {variant} already exists."
                    )
                )
                continue

            obj, created_bool = FormDefinition.objects.update_or_create(
                variant=variant,
                name=name,
                defaults={
                    "family": family,
                    "schema": schema,
                    "is_active": True,
                    "schema_class": definition.__name__,
                },
            )

            if created_bool:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Imported {definition.__name__}: {obj}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Updated {definition.__name__}: {obj}"))

        self.stdout.write(self.style.SUCCESS(f"Done. Created={created}"))

        # Ensure all users have an organization
        User = get_user_model()
        users = User.objects.all()
        for user in users:
            user = cast(CoreUser, user)
            if not UserOrganizationMembership.objects.filter(user=user).exists():
                org_name = f"{user.email}'s Organization"
                org = OrganizationProfile.objects.create(name=org_name, contact_email=user.email)
                UserOrganizationMembership.objects.create(user=user, organization=org, role="admin")
                self.stdout.write(self.style.SUCCESS(f"Created organization for user {user.email}"))
