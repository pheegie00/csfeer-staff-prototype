"""Layout schema definitions for CSFEER forms."""

import abc
import contextlib
import logging
from typing import Any, ClassVar, Literal, Self, cast

from django.forms.boundfield import BoundField
from django.forms.renderers import TemplatesSetting
from django.forms.utils import RenderableMixin
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from pydantic import BaseModel, PrivateAttr

from form_manager.schema.fields import ACFField

logger = logging.getLogger(__name__)


class RenderableBaseModel[T, S](RenderableMixin, BaseModel, abc.ABC):
    """A special Pydantic BaseModel that utilizes the Django forms rendering API
    for template rendering"""

    _global_context: dict[str, Any] = PrivateAttr(default_factory=dict)
    renderer: ClassVar[TemplatesSetting] = TemplatesSetting()
    children: list[T] | None = None
    template_name: S | None = None
    review_template_name: str | None = None

    def set_extra_context(self, **kwargs: Any) -> None:
        """Set global context that will also be made available to any descendant nodes."""
        self._global_context = kwargs
        for child in getattr(self, "children", []) or []:
            child.set_extra_context(**self._global_context)

    def get_context(self) -> dict[str, Any]:
        """Overloaded to inject global context and local variables into this
        node's template context"""
        context = {}

        field_context = {
            field_name: getattr(self, field_name, None)
            for field_name in self.__class__.model_fields
        } | {
            "component": self,
        }

        context = context | field_context | self._global_context

        return context

    def as_review_block(self, template_name: str | None = None):

        if template_name:
            return self.render(template_name)

        if self.review_template_name:
            return self.render(self.review_template_name)

        logger.warning(
            f"You're trying to call `as_review_block` on {self.__class__.__name__} "
            "without specifying a `review_template_name` property."
        )

        return ""

    @classmethod
    def has_field_blocks(cls, node) -> bool:
        """Return True if the node has any descendant FieldBlocks. Otherwise, False."""
        for child in node.children or []:

            if isinstance(child, FieldBlock):
                return True

            if cls.has_field_blocks(child):
                return True

        return False


class StepBlock(RenderableBaseModel):
    """Represents a step in a multi-step form UI. It is tied to an item
    in a USWDS step indicator component.
    """

    type: str = "step"
    title: str | None = None
    children: list[Self | "SectionBlock" | "PageBlock" | "PermanentPageBlock"] | None = None


class AbstractPageBlock(RenderableBaseModel, abc.ABC):
    """Represents a page in a multi-page form UI. A Page is a child of a step
    and represents a single page within that step."""

    type: Literal["page", "permanent-page"]
    title: str | None = None
    subtitle: str | None = None
    children: list[Self | "FieldBlock" | "SectionBlock" | "FieldGroupBlock"] | None = None
    template_name: str = "form_manager/page.html"


class PageBlock(AbstractPageBlock):
    """A PageBlock represents a single page within a step of a multi-page form."""

    type: Literal["page", "permanent-page"] = "page"


class PermanentPageBlock(AbstractPageBlock):
    """A PermanentPageBlock is a special type of PageBlock that is always
    included in the form, regardless of any conditional logic that may
    be applied to other pages."""

    type: Literal["page", "permanent-page"] = "permanent-page"


class SectionBlock(RenderableBaseModel):
    """Represents a block of the UI (i.e. div, section, etc)"""

    type: str = "section"
    title: str | None = None
    description: str | None = None
    children: list[Self | "FieldBlock" | "FieldGroupBlock" | "ReviewSubheadingBlock"] | None = None
    template_name: str = "form_manager/section.html"


class FieldGroupBlock(RenderableBaseModel):
    """Represents a group of fields surrounded by a border
    with an explanatory note."""

    type: str = "field-group"
    description: str | None = None
    children: list[Self | "FieldBlock"] | None = None
    template_name: str = "form_manager/field_group.html"


class FieldBlock(RenderableBaseModel):
    """Represents the rendering of a specific form field"""

    type: str = "field"
    field_name: str
    template_name: str = "form_manager/forms/field.html"
    review_template_name: str | None = "form_manager/forms/field_review.html"

    def get_context(self):
        context = super().get_context()
        form = context.get("form")
        if form:
            bound_field = form[self.field_name]
            context.update(
                {
                    "field": bound_field,
                }
            )
        return context

    def as_review_block(self, template_name: str | None = None):
        """This will automatically search for a template name like `[field_name]_review.html`
        and use that template to render it, if it exists."""

        def find_template():

            if hasattr(self, "field") and self.field:

                field_class = self.field.field.__class__.__name__

                field_class = field_class.replace("ACF", "").replace("Field", "")

                try:
                    _review_template_name = f"form_manager/forms/{field_class.lower()}_review.html"
                    get_template(_review_template_name)
                    return _review_template_name
                except TemplateDoesNotExist:
                    pass

        if template_name:
            pass

        elif (
            self.review_template_name != self.__class__.model_fields["review_template_name"].default
        ):
            template_name = self.review_template_name

        elif find_template():
            template_name = find_template()

        else:
            template_name = self.review_template_name

        return super().as_review_block(template_name=template_name)

    @property
    def field(self) -> BoundField | None:
        context = self.get_context()
        field = context.get("field")
        return field

    @property
    def unbound_field(self) -> ACFField | None:
        if not self.field:
            return None

        return cast(ACFField, self.field.field)

    @property
    def title(self):
        return self.unbound_field.title if self.unbound_field else None

    @property
    def value(self) -> Any:
        return self.field.value if self.field else None

    @property
    def errors(self) -> Any:
        return self.field.errors if self.field else None

    @property
    def review_title(self) -> str | None:
        return self.unbound_field.review_title if self.unbound_field else None

    @property
    def display_title(self) -> str | None:
        """Returns review_title if available, otherwise falls back to title"""
        return self.review_title or self.title


class ReviewSubheadingBlock(RenderableBaseModel):
    """Represents a subheading that will only be rendered on the review page."""

    type: str = "review-subheading"
    title: str | None = None
    description: str | None = None
    template_name: str = "form_manager/review_subheading.html"
