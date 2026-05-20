import re
from typing import Generic, TypeVar

from pydantic import computed_field, model_validator
from src.common.schemas.core_schema import CoreSchema
from src.common.schemas.constants.enums import SortDirectionEnum

FieldsEnum = TypeVar("FieldsEnum")


def camel_to_snake(name: str) -> str:
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def snake_to_camel(name: str) -> str:
    parts = name.split("_")
    return parts[0] + "".join(part.capitalize() for part in parts[1:])


class SortBase(CoreSchema, Generic[FieldsEnum]):
    sort_field: FieldsEnum | None = None
    direction: SortDirectionEnum = SortDirectionEnum.ASC

    @computed_field
    @property
    def sort_field_camel(self) -> str | None:
        return snake_to_camel(self.sort_field) if self.sort_field else None

    @model_validator(mode="after")
    def convert_sort_field(self) -> "SortBase":
        if self.sort_field:
            self.sort_field = camel_to_snake(self.sort_field)
        return self
