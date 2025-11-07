from django.core.management.base import BaseCommand

from form_manager.models import FormDefinition
from form_manager.schema.forms.base import BaseFormSchema

from ...utils import get_form_definitions


class Command(BaseCommand):
    help = "Load initial form definitions from bundled JSON files"

    def handle(self, *args, **options):
        form_definitions = get_form_definitions()

        created = 0
        updated = 0

        for definition in form_definitions:

            if type(definition) == BaseFormSchema:
                continue

            schema = definition.model_json_schema()

            def default_or_constraint(field_item):

                return field_item.get("const") or field_item.get("default")

            code = default_or_constraint(schema["properties"]["id"])
            version = default_or_constraint(schema["properties"]["version"])
            title = default_or_constraint(schema["properties"]["name"])

            if not code:
                self.stdout.write(
                    self.style.NOTICE(
                        f"Could not import {definition.__name__} because it does not have an ID defined"
                    )
                )
                continue

            obj, was_created = FormDefinition.objects.update_or_create(
                code=code,
                version=version,
                defaults={
                    "title": title,
                    "description": None,
                    "schema": schema,
                    "is_active": True,
                },
            )
            created += 1 if was_created else 0
            updated += 0 if was_created else 1
            self.stdout.write(self.style.SUCCESS(f"Imported {definition.__name__}: {obj}"))
        self.stdout.write(self.style.SUCCESS(f"Done. Created={created} Updated={updated}"))
