from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "users"

    def ready(self):

        from users.signals import create_permission_groups  # noqa
