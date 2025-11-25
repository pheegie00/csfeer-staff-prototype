from django.core.management.base import BaseCommand

from form_manager.models import FormDefinition
from form_manager.schema.forms.base import BaseFormSchema, SchemaValidationError

from ...utils import get_form_definitions


class Command(BaseCommand):
    help = "Load initial form definitions from official schemas"

    def handle(self, *args, **options):
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

            if FormDefinition.objects.filter(variant=variant, name=name).exists():
                self.stdout.write(
                    self.style.NOTICE(
                        f"A form definition named {name} with variant {variant} already exists."
                    )
                )
                continue

            obj = FormDefinition.objects.create(
                family=family,
                variant=variant,
                name=name,
                schema=schema,
                is_active=True,
            )
            created += 1
            self.stdout.write(self.style.SUCCESS(f"Imported {definition.__name__}: {obj}"))

        self.stdout.write(self.style.SUCCESS(f"Done. Created={created}"))
