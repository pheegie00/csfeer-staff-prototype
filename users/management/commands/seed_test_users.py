from typing import TYPE_CHECKING, cast

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from organizations.models import OrganizationProfile, State, UserOrganizationMembership

if TYPE_CHECKING:
    from users.models import CoreUser

from tests.fixtures.users import TEST_USERS


class Command(BaseCommand):
    """Django management command to seed test users for end-to-end and local testing."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            type=str,
            help="The email of the test-user to seed. Seed all test users if empty.",
        )

    def handle(self, *args, **options):

        UserModel = cast("CoreUser", get_user_model())

        target_email = options.get("email")

        for user_info in TEST_USERS.values():

            email: str | None = user_info.get("email")
            roles = user_info.get("roles", [])

            if target_email and email != target_email:
                continue

            try:
                user = UserModel.objects.get(email=email)
                self.stdout.write(
                    self.style.NOTICE(  # pyright: ignore
                        f"User with email '{email}' already exists."
                    )
                )
            except UserModel.DoesNotExist:
                user = UserModel.objects.create_user(
                    email=email,
                    password=user_info["password"],
                    is_staff="csfeer_admin" in roles,
                    is_superuser="csfeer_admin" in roles,
                )

                self.stdout.write(self.style.SUCCESS(f"Created user '{email}'."))  # pyright: ignore

            self._create_org(user, roles)

    def _create_org(self, user: "CoreUser", roles: list[str] | None = None):
        """Create a per-user demo organization and associate the user with the provided roles."""
        assert user is not None

        org_name = f"Demo Organization ({user.email})"

        # Create or get the organization
        org, created = OrganizationProfile.objects.get_or_create(
            name=org_name, defaults={"state": State.objects.get(code="MA")}
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created organization '{org_name}'.")  # pyright: ignore
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Using existing organization '{org_name}'.")  # pyright: ignore
            )

        # Add the user to the organization
        membership, m_created = UserOrganizationMembership.objects.get_or_create(
            user=user,
            organization=org,
        )

        # Add the user to the correct permissions groups
        membership.groups.add(*list(Group.objects.filter(name__in=roles or [])))

        # mypy/pyright: user is asserted above
        action = "Created" if m_created else "Ensured"
        self.stdout.write(
            self.style.SUCCESS(  # pyright: ignore
                f"{action} membership: user='{user.email}' ↔ org='{org.name}'"
            )
        )
