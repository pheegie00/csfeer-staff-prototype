"""Unit tests for TribalShortForm schema definition."""

import pytest
from django.core.management import call_command
from pydantic_extra_types.semantic_version import SemanticVersion

from form_manager.constants import CSBGAnnualReportForms, FormFamilies
from form_manager.models import FormDefinition
from form_manager.schema.forms import ALL_FORM_SCHEMAS
from form_manager.schema.forms.tribal_short_form import TribalShortForm, TribalShortFormFields


def test_tribal_short_form_schema_structure():
    """Verify TribalShortForm has correct metadata."""
    schema_instance = TribalShortForm.model_construct()

    assert schema_instance.family == FormFamilies.CSBG_ANNUAL_REPORT
    assert schema_instance.name == CSBGAnnualReportForms.TRIBAL_ANNUAL_REPORT_3_0_SHORT
    assert schema_instance.variant == SemanticVersion(3, 0, 0)


def test_tribal_short_form_has_correct_fields():
    """Verify TribalShortForm has expected fields (no demographics)."""
    form = TribalShortFormFields()
    field_names = list(form.fields.keys())

    # Should have basic + expenditure + descriptions (26 fields)
    assert len(field_names) == 26

    # Verify demographic fields are NOT present
    demographic_fields = [
        "total_individuals_served",
        "total_individuals_served_over_18",
        "male_individuals_served",
        "female_individuals_served",
        "total_individuals_served_by_sex",
        "employment__full_time",
        "employment__part_time",
        "employment__migrant_seasonal",
        "employment__unemployed_short_term",
        "employment__unemployed_long_term",
        "employment__permanently_unemployed",
        "employment__retired",
        "employment__unknown",
        "employment__total",
    ]

    for field in demographic_fields:
        assert field not in field_names, f"Demographic field {field} should not be in short form"

    # Verify required fields ARE present
    required_fields = [
        "org_name",
        "contact_name",
        "contact_title",
        "phone",
        "extension",
        "email",
        "fax",
        "applicable_topics",
        "employment_expenditure",
        "childcare_expenditure",
        "asset_building_expenditure",
        "housing_expenditure",
        "health_expenditure",
        "civic_expenditure",
        "transportation_expenditure",
        "partnerships_expenditure",
        "other_expenditure",
        "total_expenditures",
        "administration_expenditure",
        "employment_related_services_description",
        "education_related_service_description",
        "income_services_description",
        "housing_services_description",
        "health_services_description",
        "civic_services_description",
        "transportation_services_description",
    ]

    for field in required_fields:
        assert field in field_names, f"Required field {field} missing from short form"


def test_tribal_short_form_has_three_steps():
    """Verify TribalShortForm has exactly 3 steps (no demographic step)."""
    ui_definition = TribalShortForm.dump_ui_definition_from_json_schema()

    # Should have 3 steps (Basic Info, Expenditure categories, Expenditure details)
    assert len(ui_definition) == 3

    step_titles = [step["title"] for step in ui_definition]
    expected_titles = ["Basic Information", "Expenditure categories", "Expenditure details"]

    assert step_titles == expected_titles
    assert "Demographic information" not in step_titles


@pytest.mark.django_db
def test_tribal_short_form_loads_into_database(django_db_setup):
    """Verify TribalShortForm can be loaded into database."""
    # Verify it's in the list
    assert TribalShortForm in ALL_FORM_SCHEMAS

    # Load forms
    call_command("load_initial_forms")

    # Verify it was created
    schema_instance = TribalShortForm.model_construct()
    form_def = FormDefinition.objects.get(
        family=schema_instance.family,
        name=schema_instance.name,
        variant=str(schema_instance.variant),
    )

    assert form_def.schema_class == "TribalShortForm"
    assert form_def.schema == TribalShortForm.model_json_schema()


def test_tribal_short_form_json_schema():
    """Verify TribalShortForm generates valid JSON schema."""
    schema = TribalShortForm.model_json_schema()

    assert "properties" in schema
    assert "family" in schema["properties"]
    assert "name" in schema["properties"]
    assert "variant" in schema["properties"]
    assert "form_fields" in schema["properties"]
    assert "ui" in schema["properties"]


def test_tribal_short_form_filter_fields():
    """Verify TribalShortForm filter field functionality."""
    form = TribalShortFormFields()

    # Should have filter fields
    assert form.has_filter_fields is True

    # Test with specific selection
    form_with_selection = TribalShortFormFields(
        initial={
            "applicable_topics": ["employment_expenditure,employment_related_services_description"]
        }
    )

    excluded_fields = form_with_selection.fields_to_exclude

    # Fields from non-selected topics should be in exclusion list
    assert "childcare_expenditure" in excluded_fields
    assert "housing_expenditure" in excluded_fields
    assert "education_related_service_description" in excluded_fields


def test_tribal_short_form_calculated_fields():
    """Verify calculated fields sum correctly."""
    # Initialize form without data to get field access
    form = TribalShortFormFields()

    # Verify total_expenditures is a CalculatedCurrencyField
    from form_manager.schema.fields import acf_fields

    assert isinstance(form.fields["total_expenditures"], acf_fields.CalculatedCurrencyField)

    # Verify it has the correct source fields
    calc_field = form.fields["total_expenditures"]
    expected_fields = [
        "employment_expenditure",
        "childcare_expenditure",
        "asset_building_expenditure",
        "housing_expenditure",
        "health_expenditure",
        "civic_expenditure",
        "transportation_expenditure",
        "partnerships_expenditure",
        "other_expenditure",
    ]
    assert calc_field.fields == expected_fields
