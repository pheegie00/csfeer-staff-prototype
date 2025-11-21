"""Layout schema definitions for CSFEER forms."""

from typing import Optional, Self

from pydantic import BaseModel


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
