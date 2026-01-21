from functools import lru_cache
from typing import cast

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest
from django.utils.module_loading import import_string
from django.views.generic.base import ContextMixin
from django.views.generic.detail import (
    SingleObjectMixin,
    SingleObjectTemplateResponseMixin,
)
from django.views.generic.edit import FormMixin, ProcessFormView

from form_manager.models import FormEntry
from form_manager.schema.forms.utils import import_form_schema
from form_manager.utils import user_can_edit, user_can_submit, user_can_view


class BaseFormUpdateView(
    SingleObjectTemplateResponseMixin, FormMixin, SingleObjectMixin, ProcessFormView
):
    """
    A special base view that's similar to the built-in BaseUpdateView, except
    this one is compatible with a basic django form instead of a ModelForm.
    """

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class BaseSingleFormView(BaseFormUpdateView):
    """A base view that provides common logic for csfeer forms."""

    model = FormEntry
    object: FormEntry
    queryset = FormEntry.objects.select_related("organization")
    request: HttpRequest
    context_object_name = "entry"

    def get_form_schema(self):

        self.object = cast(FormEntry, getattr(self, "object", None) or self.get_object())

        return import_form_schema(self.object.form_definition.schema_class)

    def get_form_class(self):
        """Return the form class to use."""

        schema_class = self.get_form_schema()

        return schema_class.get_form_fields_class()

    def get_initial(self):

        if self.object:
            return self.object.data
        return {}

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        return super().get_form_kwargs()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        schema_class = self.get_form_schema()

        context.update(
            {
                "form": self.get_form(),
                "ui_components": schema_class.dump_ui_definition_from_json_schema(),
            }
        )

        return context


class BaseFormPermissionMixin(ContextMixin, PermissionRequiredMixin):

    request: HttpRequest
    object: FormEntry

    def is_locked(self):
        return self.object.locked

    def can_edit(self):

        return user_can_edit(self.request.user, self.object.organization) and not self.is_locked()

    def can_submit(self):

        return user_can_submit(self.request.user, self.object.organization) and not self.is_locked()

    def can_view(self):

        return user_can_view(self.request.user, self.object.organization)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update(
            {
                "can_edit": self.can_edit(),
                "can_submit": self.can_submit(),
                "can_view": self.can_view(),
            }
        )

        return context


class FormPermissionMixin(LoginRequiredMixin, BaseFormPermissionMixin):
    pass
