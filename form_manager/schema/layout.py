"""Layout schema definitions for CSFEER forms."""

import abc
import logging
from typing import Annotated, Any, ClassVar, Literal, Self, cast

from django.forms import MultiValueField
from django.forms.boundfield import BoundField
from django.forms.renderers import TemplatesSetting
from django.forms.utils import RenderableMixin
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from django.utils.safestring import SafeString, mark_safe
from pydantic import BaseModel, Field, PrivateAttr

from form_manager.schema.fields import ACFField

logger = logging.getLogger(__name__)


class _SubFieldBlock:
    """Minimal object satisfying the interface review templates expect from a FieldBlock.

    Used to render individual sub-fields of a MultiValueField (e.g. YesNoDisplayField)
    through the same per-field review templates as top-level fields.
    """

    def __init__(self, display_title: str | None, value: Any) -> None:
        self.display_title = display_title
        self.value = value
        self.errors: list = []

    @staticmethod
    def render_for(subfield: Any, value: Any) -> SafeString:
        title = getattr(subfield, "review_title", None) or getattr(subfield, "title", None)
        field_class = subfield.__class__.__name__.replace("ACF", "").replace("Field", "").lower()
        template_path = f"form_manager/forms/{field_class}_review.html"
        try:
            get_template(template_path)
        except TemplateDoesNotExist:
            template_path = "form_manager/forms/field_review.html"
        return mark_safe(
            get_template(template_path).render({"component": _SubFieldBlock(title, value)})
        )


class RenderableBaseModel[T, S](RenderableMixin, BaseModel, abc.ABC):
    """A special Pydantic BaseModel that utilizes the Django forms rendering API
    for template rendering"""

    _global_context: dict[str, Any] = PrivateAttr(default_factory=dict)
    renderer: ClassVar[TemplatesSetting] = TemplatesSetting()
    children: Annotated[
        list[T] | None,
        Field(description="Child layout nodes rendered inside this component"),
    ] = None
    template_name: Annotated[
        S | None,
        Field(description="Django template used to render this component"),
    ] = None
    review_template_name: Annotated[
        str | None,
        Field(description="Django template used when rendering in review mode"),
    ] = None

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
    """Represents a step in a multi-step form UI."""

    type: str = "step"
    title: Annotated[
        str | None,
        Field(description="Display title shown in the step navigation"),
    ] = None
    disabled_reason: Annotated[
        str | None,
        Field(description="Text displayed in the navigation when the step is disabled"),
    ] = None
    children: Annotated[
        list["AbstractPageBlock"] | None,
        Field(description="Pages contained within this step"),
    ] = None


class AbstractPageBlock(RenderableBaseModel, abc.ABC):
    """Represents a page in a multi-page form UI. A Page is a child of a step
    and represents a single page within that step."""

    type: Literal["page", "permanent-page"]
    title: Annotated[
        str | None,
        Field(description="Heading displayed at the top of the page"),
    ] = None
    subtitle: Annotated[
        str | None,
        Field(description="Secondary heading displayed below the title"),
    ] = None
    children: Annotated[
        list[
            Self
            | "FieldBlock"
            | "SectionBlock"
            | "FieldGroupBlock"
            | "CardGroupBlock"
            | "PageTitleBlock"
            | "PageSubtitleBlock"
            | "AlertBoxBlock"
            | "TextBlock"
            | "AccordionBlock"
        ]
        | None,
        Field(description="Content blocks rendered on this page"),
    ] = None
    template_name: Annotated[
        str,
        Field(description="Django template used to render this page"),
    ] = "form_manager/page.html"


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
    title: Annotated[
        str | None,
        Field(description="Heading displayed at the top of the section"),
    ] = None
    description: Annotated[
        str | None,
        Field(description="Descriptive text shown below the section title"),
    ] = None
    children: Annotated[
        list[Self | "FieldBlock" | "FieldGroupBlock" | "ReviewSubheadingBlock" | "ConditionalBlock"]
        | None,
        Field(description="Content blocks rendered inside this section"),
    ] = None
    alpine_controller_field: Annotated[
        str | None,
        Field(description="Name of the radio field that drives Alpine.js conditional visibility"),
    ] = None
    template_name: Annotated[
        str,
        Field(description="Django template used to render this section"),
    ] = "form_manager/section.html"


class FieldGroupBlock(RenderableBaseModel):
    """Represents a group of fields surrounded by a border
    with an explanatory note."""

    type: str = "field-group"
    description: Annotated[
        str | None,
        Field(description="Explanatory note shown inside the group border"),
    ] = None
    children: Annotated[
        list[Self | "FieldBlock" | "ReviewSubheadingBlock"] | None,
        Field(description="Fields rendered inside this group"),
    ] = None
    template_name: Annotated[
        str,
        Field(description="Django template used to render this field group"),
    ] = "form_manager/field_group.html"


class CardBlock(RenderableBaseModel):
    """Represents a USWDS card. Renders a title/subtitle header and its children
    in the card body. When `show_when_field` is set, the card only renders if the
    form's value for that field matches `show_when_value` — evaluated server-side,
    so it works across steps (unlike ConditionalBlock, which is Alpine-scoped)."""

    type: str = "card"
    title: str | None = None
    subtitle: str | None = None
    grid_layout: str = "tablet:grid-col-6"
    show_when_field: str | None = None
    show_when_value: str | list[str] | None = None
    children: list["FieldBlock | ReviewSubheadingBlock"] | None = None
    template_name: str = "form_manager/card.html"

    @property
    def should_render(self) -> bool:
        if not self.show_when_field:
            return True
        form = self._global_context.get("form")
        if form is None:
            return True
        try:
            value = form[self.show_when_field].value()
        except KeyError:
            return True
        if self.show_when_value is None:
            return bool(value)
        values = (
            [self.show_when_value]
            if isinstance(self.show_when_value, str)
            else self.show_when_value
        )
        return value in values


class CardGroupBlock(RenderableBaseModel):
    """Represents a USWDS card group — a horizontal row of CardBlocks."""

    type: str = "card-group"
    children: list[CardBlock] | None = None
    template_name: str = "form_manager/card_group.html"


class ConditionalBlock(RenderableBaseModel):
    """A block whose children are conditionally shown based on a sibling field's value.
    Requires the parent SectionBlock to have alpine_controller_field set to the
    controlling radio field name."""

    type: str = "conditional"
    title: Annotated[
        str | None,
        Field(description="Optional inline heading rendered above the block's children"),
    ] = None
    show_when: Annotated[
        str | list[str],
        Field(description="The field value(s) that trigger showing this block's children"),
    ] = "yes"
    children: Annotated[
        list["FieldBlock | ReviewSubheadingBlock | SectionBlock | DateRangePickerBlock"] | None,
        Field(description="Content blocks shown when the condition is met"),
    ] = None
    template_name: Annotated[
        str,
        Field(description="Django template used to render this conditional block"),
    ] = "form_manager/conditional_block.html"

    @property
    def show_when_expression(self) -> str:
        values = [self.show_when] if isinstance(self.show_when, str) else self.show_when
        quoted = ", ".join(f"'{v}'" for v in values)
        return f"[{quoted}].includes(checked)"


class FieldBlock(RenderableBaseModel):
    """Represents the rendering of a specific form field"""

    type: str = "field"
    field_name: Annotated[
        str,
        Field(description="Name of the Django form field to render"),
    ]
    template_name: Annotated[
        str,
        Field(description="Django template used to render this field"),
    ] = "form_manager/forms/field.html"
    review_template_name: Annotated[
        str | None,
        Field(description="Django template used when rendering this field in review mode"),
    ] = "form_manager/forms/field_review.html"

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

    @property
    def sub_review_blocks(self) -> list[SafeString]:
        """For MultiValueFields (e.g. YesNoDisplayField), returns rendered review HTML for
        each sub-field after the radio button, delegating to the sub-field's own review
        template so that new sub-field types are handled automatically."""
        if not self.field or not isinstance(self.field.field, MultiValueField):
            return []

        value = self.field.value()
        if not isinstance(value, (list, tuple)):
            value = self.field.field.widget.decompress(value) if value else []

        return [
            _SubFieldBlock.render_for(subfield, value[i] if i < len(value) else None)
            for i, subfield in enumerate(self.field.field.fields[1:], 1)
        ]


class DateRangePickerBlock(RenderableBaseModel):
    """Renders two DateField children as a USWDS date range picker — the two
    pickers are linked so that selecting a start date constrains the end date's
    minimum, and vice versa."""

    type: str = "date-range-picker"
    children: list["FieldBlock"] | None = None
    template_name: str = "form_manager/date_range_picker.html"


class ReviewSubheadingBlock(RenderableBaseModel):
    """Represents a subheading that will only be rendered on the review page."""

    type: str = "review-subheading"
    title: Annotated[
        str | None,
        Field(description="Subheading text displayed on the review page"),
    ] = None
    description: Annotated[
        str | None,
        Field(description="Descriptive text shown below the subheading on the review page"),
    ] = None
    template_name: Annotated[
        str,
        Field(description="Django template used to render this review subheading"),
    ] = "form_manager/review_subheading.html"


class PageTitleBlock(RenderableBaseModel):
    """Represents a page title that can be positioned anywhere in the page children."""

    type: str = "page-title"
    title: Annotated[
        str,
        Field(description="Title text to display"),
    ]
    subtitle: Annotated[
        str | None,
        Field(description="Secondary text displayed below the title"),
    ] = None
    template_name: Annotated[
        str,
        Field(description="Django template used to render this page title"),
    ] = "form_manager/page_title.html"


class PageSubtitleBlock(RenderableBaseModel):
    """Represents a page subtitle that can be positioned anywhere in the page children."""

    type: str = "page-subtitle"
    subtitle: Annotated[
        str,
        Field(description="Subtitle text to display"),
    ]
    template_name: Annotated[
        str,
        Field(description="Django template used to render this page subtitle"),
    ] = "form_manager/page_subtitle.html"


class AlertBoxBlock(RenderableBaseModel):
    """Represents an alert/notification box that can be positioned anywhere in the page."""

    type: str = "alert"
    alert_type: Annotated[
        Literal["info", "warning", "error", "success"],
        Field(description="Alert severity level"),
    ] = "info"
    heading: Annotated[
        str | None,
        Field(description="Optional bold heading displayed above the message"),
    ] = None
    message: Annotated[
        str,
        Field(description="Alert body text"),
    ]
    slim: Annotated[
        bool,
        Field(description="Whether to render the compact slim alert variant"),
    ] = False
    template_name: Annotated[
        str,
        Field(description="Django template used to render this alert"),
    ] = "form_manager/alert.html"


class TextBlock(RenderableBaseModel):
    """Represents plain long-form text content that is not an alert."""

    type: str = "text"
    heading: Annotated[
        str | None,
        Field(description="Optional heading displayed above the text"),
    ] = None
    text: Annotated[
        str,
        Field(description="Body text content"),
    ]
    bordered: Annotated[
        bool,
        Field(description="Whether to render the block with a surrounding border"),
    ] = False
    template_name: Annotated[
        str,
        Field(description="Django template used to render this text block"),
    ] = "form_manager/text_block.html"


class AccordionItem(RenderableBaseModel):
    """Represents a single accordion item with a heading and text content."""

    type: str = "accordion-item"
    heading: Annotated[
        str,
        Field(description="Heading text for the accordion toggle button"),
    ]
    text: Annotated[
        str,
        Field(description="Body content revealed when the item is expanded"),
    ]
    is_expanded: Annotated[
        bool,
        Field(description="Whether the item is expanded by default"),
    ] = False


class AccordionBlock(RenderableBaseModel):
    """Represents a USWDS accordion content block."""

    type: str = "accordion"
    items: Annotated[
        list[AccordionItem],
        Field(description="Accordion items to render"),
    ]
    multiselectable: Annotated[
        bool,
        Field(description="Whether multiple items can be open simultaneously"),
    ] = True
    bordered: Annotated[
        bool,
        Field(description="Whether to render the accordion with a surrounding border"),
    ] = False
    template_name: Annotated[
        str,
        Field(description="Django template used to render this accordion"),
    ] = "form_manager/accordion_block.html"
