from django.apps import AppConfig


class StaffReviewConfig(AppConfig):
    """
    Federal-staff workflow (production).

    Per-screen translation of the staff_prototype React bundle into real
    Django templates backed by Submission models. Mounted at /staff/.

    Migration plan tracked in staff_review/README.md.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "staff_review"
    verbose_name = "Staff Review (production)"

    def ready(self):
        # Wire audit signal handlers (CORE-21, CORE-36).
        # Importing the module is enough -- decorators register the receivers.
        from staff_review import signals  # noqa: F401
