"""Form field definitions."""

from enum import Enum
from typing import Annotated

from pydantic import EmailStr, Field
from pydantic.config import JsonDict

BASE_FIELD_OPTIONS: JsonDict = {"subtype": ""}

type BaseTextField = Annotated[
    str,
    Field(json_schema_extra=BASE_FIELD_OPTIONS),
]
type BaseFloatField = Annotated[float, Field(json_schema_extra=BASE_FIELD_OPTIONS)]
type BaseEnumField = Annotated[Enum, Field(json_schema_extra=BASE_FIELD_OPTIONS)]


type TextField = Annotated[
    BaseTextField,
    Field(
        json_schema_extra={
            "minLength": 0,
            "maxLength": 255,
        }
    ),
]

type TextareaField = Annotated[
    str,
    Field(
        json_schema_extra={
            "minLength": 0,
            "maxLength": 0,
            "pattern": None,
            "subtype": "longText",
        }
    ),
]

type MoneyField = Annotated[
    BaseFloatField,
    Field(
        json_schema_extra={
            "currencySymbol": "$",
            "currencyCode": "USD",
            "subtype": "currency",
        }
    ),
]

type PhoneNumberField = Annotated[
    str,
    Field(
        json_schema_extra={
            "subtype": "telephone",
            "pattern": "\\d{3}-\\d{3}-\\d{4}",
        }
    ),
]

type EmailField = Annotated[
    EmailStr,
    Field(
        json_schema_extra={
            "subtype": "email",
            "pattern": "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*$",
        }
    ),
]


type BooleanField = Annotated[bool, Field()]


type ComputedField = Annotated[
    BaseFloatField, Field(json_schema_extra={"subType": "computed", "fields": []})
]

type ChoiceField = Annotated[Enum, Field()]


ALL_FIELD_TYPES = (
    TextField
    | TextareaField
    | MoneyField
    | PhoneNumberField
    | EmailField
    | BooleanField
    | ChoiceField
    | ComputedField
)
