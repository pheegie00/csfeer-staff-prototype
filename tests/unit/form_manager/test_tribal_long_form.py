"""Unit tests for TribalLongForm schema definition."""

import pytest
from django.core.management import call_command
from pydantic_extra_types.semantic_version import SemanticVersion

from form_manager.constants import CSBGAnnualReportForms, FormFamilies
from form_manager.models import FormDefinition
from form_manager.schema.fields import acf_fields
from form_manager.schema.forms import ALL_FORM_SCHEMAS
from form_manager.schema.forms.tribal_long_form import TribalLongForm, TribalLongFormFields
from form_manager.schema.layout import AlertBoxBlock, PageTitleBlock


def test_tribal_long_form_schema_structure():
    """Verify TribalLongForm has correct metadata."""
    schema_instance = TribalLongForm.model_construct()

    assert schema_instance.family == FormFamilies.CSBG_ANNUAL_REPORT
    assert schema_instance.name == CSBGAnnualReportForms.TRIBAL_ANNUAL_REPORT_3_0
    assert schema_instance.variant == SemanticVersion(3, 0, 4)


def test_tribal_long_form_has_four_steps():
    """Verify TribalLongForm has exactly 4 steps including demographic step."""
    ui_definition = TribalLongForm.dump_ui_definition_from_json_schema()

    assert len(ui_definition) == 4

    step_titles = [step["title"] for step in ui_definition]
    expected_titles = [
        "Basic Information",
        "Expenditure categories",
        "Expenditure details",
        "Demographic information",
    ]

    assert step_titles == expected_titles


def test_tribal_long_form_extension_and_fax_not_required():
    """Verify extension and fax fields are optional."""
    form = TribalLongFormFields()

    assert form.fields["extension"].required is False
    assert form.fields["fax"].required is False


def test_tribal_long_form_has_alert_and_title_blocks():
    """Verify TribalLongForm expenditure categories page uses AlertBoxBlock and PageTitleBlock."""
    schema = TribalLongForm.model_construct()

    assert schema.ui is not None
    assert len(schema.ui) > 1

    expenditure_step = schema.ui[1]
    assert expenditure_step.title == "Expenditure categories"
    assert expenditure_step.children is not None

    first_page = expenditure_step.children[0]
    assert first_page.children is not None
    assert len(first_page.children) > 0

    alert_blocks = [child for child in first_page.children if isinstance(child, AlertBoxBlock)]
    assert (
        len(alert_blocks) == 1
    ), "Expected exactly one AlertBoxBlock in expenditure categories page"

    alert = alert_blocks[0]
    assert alert.alert_type == "info"
    assert alert.heading == "How to select expenditure categories"
    assert "select a category" in alert.message.lower()

    title_blocks = [child for child in first_page.children if isinstance(child, PageTitleBlock)]
    assert (
        len(title_blocks) == 1
    ), "Expected exactly one PageTitleBlock in expenditure categories page"

    title = title_blocks[0]
    assert title.title == "Expenditure categories"


@pytest.mark.django_db
def test_tribal_long_form_loads_into_database(django_db_setup):
    """Verify TribalLongForm can be loaded into database."""
    assert TribalLongForm in ALL_FORM_SCHEMAS

    call_command("load_initial_forms")

    schema_instance = TribalLongForm.model_construct()
    form_def = FormDefinition.objects.get(
        family=schema_instance.family,
        name=schema_instance.name,
        variant=str(schema_instance.variant),
    )

    assert form_def.schema_class == "TribalLongForm"
    assert form_def.schema == TribalLongForm.model_json_schema()
