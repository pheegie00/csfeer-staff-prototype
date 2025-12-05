import semver
from django.core.exceptions import ValidationError
from django.db import models


class SemVerField(models.CharField):

    def to_python(self, value):
        """Convert input value to Python string, validating semver format."""
        if value is None:
            return None
        if not value:
            return ""
        return str(value)

    def validate(self, value, model_instance):
        """Validate that the value is a valid semantic version."""
        super().validate(value, model_instance)
        if value is None or value == "":
            return
        try:
            semver.VersionInfo.parse(value)
        except ValueError as e:
            raise ValidationError(
                f"Invalid semantic version: {value}. Error: {str(e)}",
                code="invalid_semver",
            )

    def get_prep_value(self, value):
        """Prepare the value for database storage."""
        if value is None:
            return None
        return str(value)
