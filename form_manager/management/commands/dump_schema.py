import json

from django.core.management.base import BaseCommand, CommandError

from form_manager.schema.forms import BaseFormSchema
from form_manager.utils import get_form_definitions


class Command(BaseCommand):
    help = "Dumps a form schema in JSON Schema format."

    def add_arguments(self, parser):
        """Add arguments to the command"""

        parser.add_argument(
            "--name",
            type=str,
            action="store",
            default=BaseFormSchema.__name__,
            help="The name of the form schema to dump (default: base)",
        )

        parser.add_argument(
            "--list",
            action="store_true",
            default=False,
            help="List available form schemas to dump",
        )

    def handle(self, *args, **options) -> None:
        """Command execution handler"""

        do_list = options["list"]

        if do_list:
            return self._handle_list()

        return self._handle_dump(*args, **options)

    def _handle_list(self):
        """Handles listing of available forms"""

        out = "Forms available to dump:\n"

        available_forms = get_form_definitions()

        for form in available_forms:

            out += f"  - {form.__name__}\n"

        self.stdout.write(self.style.SUCCESS(out))

    def _handle_dump(self, *args, **options):
        """Handles dumping of forms"""

        form_name = options["name"]

        available_forms = get_form_definitions()

        form_class = None

        for cls in available_forms:

            if cls.__name__ == form_name:
                form_class = cls
                break

        if not form_class:
            raise CommandError(f"Form with name {form_name} is not available to be dumpted")

        schema = form_class.model_json_schema()

        self.stdout.write(self.style.SUCCESS(json.dumps(schema, indent=2)))
