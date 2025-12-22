"""Layout schema definitions for CSFEER forms."""

from collections.abc import Mapping
from typing import Any, ClassVar, Optional, Self, cast

from django.forms.renderers import TemplatesSetting
from django.forms.utils import RenderableMixin
from pydantic import BaseModel


class RenderableBaseModel[T](RenderableMixin, BaseModel):
    """A special Pydantic BaseModel that utilizes the Django forms rendering API
    for template rendering"""

    _global_context = {}
    renderer: ClassVar[TemplatesSetting] = TemplatesSetting()
    children: Optional[list[T]] = None

    def set_extra_context(self, **kwargs: dict) -> None:
        self._global_context = kwargs

    def get_context(self) -> dict[str, Any]:
        context = {}

        field_context = {
            field_name: getattr(self, field_name, None)
            for field_name in self.__class__.model_fields.keys()
        }

        context = context | field_context | self._global_context

        if getattr(self, "children", None):
            if self.children:
                for child in self.children:
                    child = cast(Self, child)
                    try:
                        child.set_extra_context(**self._global_context)
                    except Exception as err:
                        print(err)

        return context


class StepBlock(BaseModel):
    """Represents a step in a multi-step form UI. It is tied to an item
    in a USWDS step indicator component.
    """

    type: str = "step"
    title: Optional[str] = None
    children: Optional[list[Self | "SectionBlock" | "PageBlock"]] = None


class PageBlock(RenderableBaseModel):
    """Represents a page in a multi-page form UI. A Page is a child of a step
    and represents a single page within that step."""

    type: str = "page"
    title: Optional[str] = None
    subtitle: Optional[str] = None
    children: Optional[list[Self | "FieldBlock" | "SectionBlock"]] = None
    template_name: ClassVar[str] = "form_manager/page.html"


class SectionBlock(RenderableBaseModel):
    """Represents a block of the UI (i.e. div, section, etc)"""

    type: str = "section"
    title: Optional[str] = None
    description: Optional[str] = None
    children: Optional[list[Self | "FieldBlock"]] = None
    template_name: ClassVar[str] = "form_manager/section.html"


class FieldBlock(RenderableBaseModel):
    """Represents the rendering of a specific form field"""

    type: str = "field"
    field_name: str
    template_name: ClassVar[str] = "form_manager/forms/field.html"

    def get_context(self):
        context = super().get_context()
        form = context.get("form")
        if form:
            context.update({"field": form.fields.get(self.field_name)})
        return context
