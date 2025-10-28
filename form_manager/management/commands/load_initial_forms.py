import json
from pathlib import Path

from django.core.management.base import BaseCommand

from form_manager.models import FormDefinition


class Command(BaseCommand):
    help = "Load initial form definitions from bundled JSON files"

    def handle(self, *args, **options):
        base = Path(__file__).resolve().parents[3] / "form_manager" / "form_configs"
        if not base.exists():
            self.stdout.write(self.style.WARNING(f"No form_configs directory found at {base}"))
            return
        created = 0
        updated = 0
        for p in base.glob("*.json"):
            with p.open() as f:
                payload = json.load(f)
            code = payload.get("code")
            title = payload.get("title")
            version = payload.get("version", "1.0")
            description = payload.get("description", "")
            schema = payload.get("schema", {})
            obj, was_created = FormDefinition.objects.update_or_create(
                code=code,
                version=version,
                defaults={
                    "title": title,
                    "description": description,
                    "schema": schema,
                    "is_active": True,
                },
            )
            created += 1 if was_created else 0
            updated += 0 if was_created else 1
            self.stdout.write(self.style.SUCCESS(f"Imported {p.name}: {obj}"))
        self.stdout.write(self.style.SUCCESS(f"Done. Created={created} Updated={updated}"))
