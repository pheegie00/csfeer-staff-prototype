"""Form field definitions."""

from __future__ import annotations

from enum import Enum
from functools import lru_cache
from typing import TYPE_CHECKING, Annotated, Any, NewType, Union, get_args, get_origin

from pydantic import (
    Field,
)
from pydantic_extra_types.phone_numbers import PhoneNumber

if TYPE_CHECKING:

    class EmailStr(str):
        pass

else:
    from pydantic import EmailStr


def SpecificTypedField(field_type: str, *args, **kwargs) -> Any:
    """A field with a specific field type in its JSON schema"""

    json_schema_extra = kwargs.get("json_schema_extra", {})
    json_schema_extra.update({"fieldType": field_type})

    kwargs = kwargs | {"json_schema_extra": json_schema_extra}

    return Field(*args, **kwargs)


TextField = Annotated[
    NewType("TextField", str),
    SpecificTypedField(field_type="TextField", min_length=0, max_length=255),
]

TextareaField = Annotated[
    NewType("TextareaField", str),
    SpecificTypedField(
        "TextareaField",
        min_length=0,
        max_length=0,
    ),
]

CurrencyField = Annotated[
    NewType("CurrencyField", float),
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
    NewType("PhoneNumberField", USPhoneFieldType),
    SpecificTypedField(
        "PhoneNumberField",
        json_schema_extra={
            "pattern": "\\d{3}-\\d{3}-\\d{4}",
        },
    ),
]

EmailField = Annotated[
    NewType("EmailField", EmailStr),
    SpecificTypedField(
        "EmailField",
        json_schema_extra={
            "pattern": "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*$",
        },
    ),
]


BooleanField = Annotated[NewType("BooleanField", bool), Field()]


CalculatedField = Annotated[
    NewType("CalculatedField", float),
    SpecificTypedField("CalculatedField", json_schema_extra={"fields": []}),
]

CalculatedCurrencyField = Annotated[
    NewType("CalculatedCurrencyField", float),
    SpecificTypedField("CalculatedCurrencyField", json_schema_extra={"fields": []}),
]


class ChoiceField(Enum):
    pass


ALL_FIELD_TYPES = (
    TextField
    | TextareaField
    | CurrencyField
    | PhoneNumberField
    | EmailField
    | BooleanField
    | ChoiceField
    | CalculatedCurrencyField
    | CalculatedField
)


def get_base_origin(t):
    """Return the base type of a type."""

    if get_origin(t) == Union:
        t = get_args(t)[0]

    while True:

        _next = get_origin(t)

        if not _next:
            return t

        t = _next


@lru_cache
def get_allowed_field_types() -> list[Any]:
    """Return a list of possible base field types."""

    allowed_field_types = []

    for _type in get_args(ALL_FIELD_TYPES):

        allowed_field_types.append(get_base_origin(_type))

    return allowed_field_types
