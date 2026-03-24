from typing import TYPE_CHECKING, cast

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

if TYPE_CHECKING:
    from users.models import CoreUser

from tests.fixtures.users import TEST_USERS


class Command(BaseCommand):
    """Django management command to seed test users for end-to-end testing."""

    def handle(self, *args, **options):

        UserModel = cast("CoreUser", get_user_model())

        for user_info in TEST_USERS.values():
            email: str | None = user_info.get("email")
            if user_info["username"] == "admin":
                continue

            if UserModel.objects.filter(email=email).exists():
                self.stdout.write(self.style.NOTICE(f"User with email '{email}' already exists."))
                continue

            UserModel.objects.create_user(
                email=email,
                password=user_info["password"],
            )
            self.stdout.write(self.style.SUCCESS(f"Created user '{email}'."))
