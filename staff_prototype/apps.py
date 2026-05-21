from django.apps import AppConfig


class StaffPrototypeConfig(AppConfig):
    """
    Federal-staff workflow prototype.

    Bundle from Claude Design (claude.ai/design) handoff -- hi-fi React
    prototype of the staff review/return/edit-on-behalf/determination flow.
    Served as static assets through Django so it lives in the real app and
    can be demoed via `make start-local` without standing up a separate
    server.

    Phase 2: each screen here translates to a Django template using
    csfeer/templates/patterns/ USWDS Cotton components and wires to real
    Submission models. Track migration progress in this app's README.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "staff_prototype"
    verbose_name = "Staff Workflow Prototype"
