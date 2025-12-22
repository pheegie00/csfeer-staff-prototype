"""Layout schema definitions for CSFEER forms."""

from typing import Optional, Self

from pydantic import BaseModel


class StepBlock(BaseModel):
    """Represents a step in a multi-step form UI. It is tied to an item
    in a USWDS step indicator component.
    """

    type: str = "step"
    title: Optional[str] = None
    children: Optional[list[Self | "SectionBlock" | "PageBlock"]] = None


class PageBlock(BaseModel):
    """Represents a page in a multi-page form UI. A Page is a child of a step
    and represents a single page within that step."""

    type: str = "page"
    title: Optional[str] = None
    subtitle: Optional[str] = None
    children: Optional[list[Self | "FieldBlock" | "SectionBlock"]] = None


class SectionBlock(BaseModel):
    """Represents a block of the UI (i.e. div, section, etc)"""

    type: str = "section"
    title: Optional[str] = None
    description: Optional[str] = None
    children: Optional[list[Self | "FieldBlock"]] = None


class FieldBlock(BaseModel):
    """Represents the rendering of a specific form field"""

    type: str = "field"
    field_name: str
