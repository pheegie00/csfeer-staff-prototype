from django.core.management.base import BaseCommand

from form_manager.models import (
    FormAuditDetail,
    FormAuditTrail,
    FormDefinition,
    FormEntry,
)


class Command(BaseCommand):
    help = "Delete all FormEntry, FormDefinition, and related audit records"

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-input",
            action="store_true",
            help="Skip confirmation prompt",
        )

    def handle(self, *args, **options):
        if not options["no_input"]:
            confirm = input(
                "This will delete ALL FormEntry, FormDefinition, and audit records. "
                "Are you sure? (yes/no): "
            )
            if confirm.lower() != "yes":
                self.stdout.write(self.style.WARNING("Aborted."))
                return

        # Delete in order due to foreign key constraints
        audit_detail_count = FormAuditDetail.objects.count()
        FormAuditDetail.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(f"Deleted {audit_detail_count} FormAuditDetail records")
        )

        audit_count = FormAuditTrail.objects.count()
        FormAuditTrail.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {audit_count} FormAuditTrail records"))

        entry_count = FormEntry.objects.count()
        FormEntry.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {entry_count} FormEntry records"))

        definition_count = FormDefinition.objects.count()
        FormDefinition.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {definition_count} FormDefinition records"))

        self.stdout.write(self.style.SUCCESS("✓ All form data nuked successfully"))
