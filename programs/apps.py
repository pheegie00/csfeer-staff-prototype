from django.apps import AppConfig


class ProgramsConfig(AppConfig):
    """ACF program registry.

    Models the ACF Office -> Program hierarchy so each FormDefinition
    can be attributed to a specific program, and staff permissions can
    be scoped per program (STAFF-MP-01, STAFF-MP-04).

    Seed data covers CSBG (OCS, active), TANF (OFA, active),
    Tribal TANF (OFA, active), HMRF (OFA, active), HPOG (OFA, inactive).
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "programs"
    verbose_name = "ACF Programs"
