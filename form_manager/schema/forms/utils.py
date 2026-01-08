from django.utils.module_loading import import_string


def import_form_schema(schema_class_name: str):

    return import_string("form_manager.schema.forms." + schema_class_name)
