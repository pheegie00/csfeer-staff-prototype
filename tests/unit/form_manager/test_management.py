import pytest
from django.core.management import call_command

from form_manager.models import FormDefinition
from form_manager.schema.forms import ALL_FORM_SCHEMAS
from form_manager.utils import get_form_definitions

MODULE_PATH = "form_manager.management.commands.load_initial_forms"


@pytest.mark.django_db
def test_correctly_loads_form_schemas_in_db(django_db_setup):
    """Ensure the load_initial_forms command loads successfully."""

    call_command("load_initial_forms")

    assert FormDefinition.objects.count() == len(
        ALL_FORM_SCHEMAS
    ), "Failed to load all form schemas"

    for schema in get_form_definitions():

        schema_instance = schema.model_construct()

        form_definition_qs = FormDefinition.objects.filter(
            family=schema_instance.family,
            name=schema_instance.name,
            variant=schema_instance.variant,
        )

        assert form_definition_qs.count() == 1, f"Failed to load {schema_instance.name} schema"

        form_definition = form_definition_qs.first()

        import ipdb

        ipdb.set_trace()

        assert form_definition.schema_class == schema.__name__

        assert form_definition and (
            form_definition.schema == schema.model_json_schema()
        ), f"{schema.__name__} schema differs in db"
