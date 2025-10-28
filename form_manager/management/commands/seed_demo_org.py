from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from form_manager.models import OrganizationProfile, UserOrganizationMembership


class Command(BaseCommand):
    help = (
        "Create a 'Demo Organization' and link it to an existing Django user as editor (non-admin). "
        "Users must be created via OIDC login; this command will not create users."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            type=str,
            default="demo",
            help="Username to link to the demo organization (default: 'demo').",
        )
        parser.add_argument(
            "--org-name",
            type=str,
            default="Demo Organization",
            help="Name of the organization to create or reuse.",
        )

    def handle(self, *args, **options):
        User = get_user_model()
        username: str | None = options.get("username")
        org_name: str = options.get("org_name") or "Demo Organization"
        # No local user creation here; user must already exist via OIDC login

        # Resolve user
        user = None
        if username:
            user = User.objects.filter(username=username).first()
            if not user:
                raise CommandError(
                    f"User '{username}' not found. Have them sign in via OIDC first to provision the Django user."
                )
        else:
            # With defaulting to 'demo', we should practically never hit this branch.
            raise CommandError("No username resolved. Specify --username.")

        # At this point user must be resolved
        assert user is not None

        # Create or get the organization
        org, created = OrganizationProfile.objects.get_or_create(name=org_name)
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created organization '{org_name}'."))
        else:
            self.stdout.write(self.style.WARNING(f"Using existing organization '{org_name}'."))

        # Link membership as editor (non-admin)
        membership, m_created = UserOrganizationMembership.objects.get_or_create(
            user=user,
            organization=org,
            defaults={"role": "editor"},
        )
        if not m_created and membership.role != "editor":
            membership.role = "editor"
            membership.save(update_fields=["role"])
            self.stdout.write(self.style.SUCCESS(f"Updated role for '{user.username}' to editor."))

        # mypy/pyright: user is asserted above
        action = "Created" if m_created else "Ensured"
        self.stdout.write(
            self.style.SUCCESS(
                f"{action} membership: user='{user.username}' ↔ org='{org.name}' (role=editor)"
            )
        )
