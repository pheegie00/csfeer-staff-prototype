import pytest
from django.core.exceptions import ValidationError

from form_manager.models import FormDefinition
from form_manager.models.fields import SemVerField


@pytest.mark.parametrize(
    "value",
    [
        "0.0.1",
        "1.0.0",
        "3.0.4",
        "10.20.30",
        "1.0.0-alpha",
        "1.0.0-alpha.1",
        "1.0.0+build.1",
        "1.0.0-rc.1+build.5",
    ],
)
def test_semver_field_accepts_valid_versions(value):
    """Valid semantic versions pass validation."""
    field = SemVerField(max_length=20)
    field.validate(value, FormDefinition())


@pytest.mark.parametrize(
    "value",
    [
        "1.0",
        "v1.0.0",
        "1.0.0.0",
        "abc",
        "1",
        "1.a.0",
    ],
)
def test_semver_field_rejects_invalid_versions(value):
    """Invalid semantic versions raise ValidationError with code 'invalid_semver'."""
    field = SemVerField(max_length=20)
    with pytest.raises(ValidationError) as exc_info:
        field.validate(value, FormDefinition())
    assert exc_info.value.code == "invalid_semver"


def test_semver_field_skips_validation_for_none_and_empty():
    """None and empty strings do not raise — base CharField handles required-ness."""
    field = SemVerField(max_length=20, blank=True, null=True)
    field.validate(None, FormDefinition())
    field.validate("", FormDefinition())


def test_semver_field_to_python_returns_string():
    """to_python normalizes input to a string and preserves None."""
    field = SemVerField(max_length=20)
    assert field.to_python("1.2.3") == "1.2.3"
    assert field.to_python(None) is None
    assert field.to_python("") == ""


def test_semver_field_get_prep_value_returns_string():
    """get_prep_value coerces to str for DB storage and preserves None."""
    field = SemVerField(max_length=20)
    assert field.get_prep_value("1.2.3") == "1.2.3"
    assert field.get_prep_value(None) is None
