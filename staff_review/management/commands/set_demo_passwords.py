"""set_demo_passwords -- give the seeded demo personas usable passwords.

For Fly.io / non-Keycloak deployments. The local stack uses Keycloak +
unusable Django passwords (set_unusable_password), but the deployed
demo needs a way to sign in via Django auth until Keycloak is wired
up.

Reads the password from the DEMO_PASSWORD env var (default 'core-demo')
and applies it to every persona seeded by `seed_demo_users`.

Idempotent: rerun anytime to rotate the password across all personas.

Usage:
    uv run python manage.py set_demo_passwords
    DEMO_PASSWORD=mySecret uv run python manage.py set_demo_passwords
"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from staff_review.management.commands.seed_demo_users import (
    RECIPIENT_PERSONAS,
    STAFF_PERSONAS,
)

User = get_user_model()


class Command(BaseCommand):
    help = "Apply DEMO_PASSWORD to every seeded demo persona."

    def handle(self, *args, **options):
        password = os.environ.get("DEMO_PASSWORD", "core-demo")
        emails = [p[0] for p in STAFF_PERSONAS] + [p[0] for p in RECIPIENT_PERSONAS]

        n_updated = 0
        for email in emails:
            u = User.objects.filter(email=email).first()
            if u is None:
                self.stdout.write(self.style.WARNING(
                    f"  {email}: not seeded yet, skipping"
                ))
                continue
            u.set_password(password)
            u.save(update_fields=["password"])
            n_updated += 1
            self.stdout.write(f"  {email}: password set")

        self.stdout.write(self.style.SUCCESS(
            f"\nSet password on {n_updated} of {len(emails)} demo personas. "
            f"Password is the value of DEMO_PASSWORD env var (default 'core-demo')."
        ))
