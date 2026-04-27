from typing import TYPE_CHECKING, cast

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError

from organizations.models import OrganizationProfile, UserOrganizationMembership

if TYPE_CHECKING:
    from users.models import CoreUser


class Command(BaseCommand):
    help = (
        "Create a 'Demo Organization' and link it to an existing Django user as editor "
        "(non-admin). Users must be created via OIDC login; this command will not create users."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            type=str,
            default="demo",
            help="Email to link to the demo organization (default: 'demo').",
        )
        parser.add_argument(
            "--org-name",
            type=str,
            default="Demo Organization",
            help="Name of the organization to create or reuse.",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            default=False,
            help="Seed this demo org for all django users",
        )

    def handle(self, *args, **options):
        seed_all = options.get("all")
        org_name: str = options.get("org_name") or "Demo Organization"

        UserModel = cast("CoreUser", get_user_model())

        if seed_all:
            for user in UserModel.objects.all():
                self._create_org(user, org_name)
        else:
            email: str | None = options.get("username")

            try:
                user = UserModel.objects.get(email=email)
            except UserModel.DoesNotExist as err:
                raise CommandError(
                    f"User '{email}' not found. Have them sign in via "
                    "OIDC first to provision the Django user."
                ) from err

            self._create_org(user, org_name)

    def _create_org(self, user: "CoreUser", org_name: str):

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
        )

        membership.groups.add(Group.objects.get(name="Recipient Authorized Official"))

        # mypy/pyright: user is asserted above
        action = "Created" if m_created else "Ensured"
        self.stdout.write(
            self.style.SUCCESS(f"{action} membership: user='{user.username}' ↔ org='{org.name}'")
        )
