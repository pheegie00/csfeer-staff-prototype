import semver
from django.core.exceptions import ValidationError
from django.db import models


class SemVerField(models.CharField):
    """Creating a custom field to use the same semantic versioning
    package that pydantic uses."""

    def from_db_value(self, value, *_):
        return semver.Version.parse(value)

    def to_python(self, value):

        value = super().to_python(value)

        try:
            return semver.Version.parse(value)
        except ValueError as err:
            raise ValidationError(str(err))

    def get_prep_value(self, value: semver.Version):
        """Convert the Version object into a string for db insertion."""
        value = super().get_prep_value(value)

        return str(value)
