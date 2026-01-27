"""
API schemas for form_manager.
"""

from datetime import datetime

from ninja import Schema
from pydantic import ConfigDict, Field


class OrganizationSchema(Schema):
    id: int
    name: str
    address: str
    contact_email: str
    contact_phone: str


class FormDefinitionSchema(Schema):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    family: str
    name: str
    variant: str
    description: str | None = None
    form_schema: dict = Field(..., alias="schema")
    schema_class: str
    is_active: bool
    created_at: datetime


class FormDefinitionListSchema(Schema):
    """Simplified schema for listing forms."""

    id: int
    family: str
    name: str
    variant: str
    description: str | None = None
    is_active: bool


class FormEntrySchema(Schema):
    id: int
    form_definition: FormDefinitionListSchema
    organization: OrganizationSchema
    created_by_id: int | None = None
    data: dict
    version_number: int
    status: str
    submitted_at: datetime | None = None
    updated_at: datetime
    locked: bool
    is_archived: bool


class FormEntryListSchema(Schema):
    """Simplified schema for listing entries."""

    id: int
    form_definition_name: str
    form_definition_variant: str
    organization_name: str
    version_number: int
    status: str
    submitted_at: datetime | None = None
    updated_at: datetime
    locked: bool


class AuditTrailSchema(Schema):
    id: int
    user_id: int | None = None
    action: str
    timestamp: datetime
    notes: str


class AuditDetailSchema(Schema):
    id: int
    user_id: int | None = None
    field_name: str
    old_value: str
    new_value: str
    timestamp: datetime
    timestamp: datetime
    timestamp: datetime
    timestamp: datetime
