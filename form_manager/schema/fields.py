"""Form field definitions."""

from __future__ import annotations

from enum import Enum
from typing import Annotated, Any

from pydantic import (
    EmailStr,
    Field,
    WithJsonSchema,
)
from pydantic.config import JsonDict
from pydantic_extra_types.phone_numbers import PhoneNumber


def SpecificTypedField(field_type: str, *args, **kwargs) -> Any:
    """A field with a specific field type in its JSON schema"""

    json_schema_extra = kwargs.get("json_schema_extra", {})
    json_schema_extra.update({"fieldType": field_type})

    kwargs = kwargs | {"json_schema_extra": json_schema_extra}

    return Field(*args, **kwargs)


BaseTextField = Annotated[str, SpecificTypedField("TextField", min_length=0, max_length=255)]
BaseFloatField = Annotated[float, SpecificTypedField("FloatField")]
BaseEnumField = Annotated[Enum, SpecificTypedField("EnumField")]


TextField = BaseTextField

TextareaField = Annotated[
    BaseTextField,
    SpecificTypedField(
        "TextareaField",
        min_length=0,
        max_length=0,
    ),
]

CurrencyField = Annotated[
    BaseFloatField,
    SpecificTypedField(
        "CurrencyField",
        json_schema_extra={
            "currencySymbol": "$",
            "currencyCode": "USD",
        },
    ),
]


class USPhoneFieldType(PhoneNumber):
    default_region_code = "US"
    supported_regions = ["US"]
    phone_format = "NATIONAL"


PhoneNumberField = Annotated[
    USPhoneFieldType,
    SpecificTypedField(
        "PhoneNumberField",
        json_schema_extra={
            "pattern": "\\d{3}-\\d{3}-\\d{4}",
        },
    ),
]

EmailField = Annotated[
    EmailStr,
    SpecificTypedField(
        "EmailField",
        json_schema_extra={
            "pattern": "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*$",
        },
    ),
]


BooleanField = Annotated[bool, Field()]


ComputedField = Annotated[
    BaseFloatField, SpecificTypedField("ComputedField", json_schema_extra={"fields": []})
]

ChoiceField = Annotated[Enum, Field()]


ALL_FIELD_TYPES = (
    TextField
    | TextareaField
    | CurrencyField
    | PhoneNumberField
    | EmailField
    | BooleanField
    | ChoiceField
    | ComputedField
)
