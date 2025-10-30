from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Generate ER diagram from database schema and save with versioned filename"

    def add_arguments(self, parser):
        parser.add_argument(
            "apps",
            nargs="*",
            help="Apps to include in diagram (default: all apps if none specified)",
        )
        parser.add_argument(
            "--output-dir",
            type=str,
            default="docs/app/erds",
            help="Directory to save schema diagrams (default: docs/app/erds)",
        )
        parser.add_argument(
            "--format",
            type=str,
            default="png",
            choices=["png", "svg", "pdf", "dot"],
            help="Output format (default: png)",
        )

    def handle(self, *args, **options):
        try:
            from django_extensions.management.commands import graph_models  # noqa: F401
        except ImportError:
            self.stdout.write(self.style.ERROR("django-extensions not installed. Run: uv sync"))
            return

        try:
            import pydotplus  # noqa: F401
        except ImportError:
            self.stdout.write(
                self.style.ERROR("graphviz not installed. Run: brew install graphviz && uv sync")
            )
            return

        output_dir = Path(options["output_dir"])
        output_dir.mkdir(parents=True, exist_ok=True)

        db_name = connection.settings_dict["NAME"]
        schema_name = Path(db_name).stem if "/" in db_name else db_name

        apps = options.get("apps", [])

        # Append app names to filename if specific apps provided
        if apps:
            app_suffix = "_" + "_".join(apps)
            filename = f"{schema_name}{app_suffix}.{options['format']}"
        else:
            filename = f"{schema_name}.{options['format']}"

        output_file = output_dir / filename

        from django.core.management import call_command

        try:
            if apps:
                call_command(
                    "graph_models",
                    *apps,
                    output=str(output_file),
                    group_models=True,
                    verbose_names=True,
                    inheritance=True,
                )
            else:
                call_command(
                    "graph_models",
                    "--all",
                    output=str(output_file),
                    group_models=True,
                    verbose_names=True,
                    inheritance=True,
                )

            self.stdout.write(self.style.SUCCESS(f"ER diagram saved to: {output_file.absolute()}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error generating diagram: {e}"))
