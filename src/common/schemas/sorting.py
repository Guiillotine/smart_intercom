import re
from typing import Generic, TypeVar

from pydantic import computed_field, model_validator

from src.common.schemas import CoreSchema
from src.common.schemas.constants.enums import SortDirectionEnum

FieldsEnum = TypeVar("FieldsEnum")


def camel_to_snake(name: str) -> str:
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


class SortBase(CoreSchema, Generic[FieldsEnum]):
    sort_field: FieldsEnum | None = None
    direction: SortDirectionEnum = SortDirectionEnum.ASC

    @computed_field
    @property
    def sort_field_snake(self) -> str | None:
        return camel_to_snake(self.sort_field) if self.sort_field else None

    @model_validator(mode="after")
    def convert_sort_field(self) -> "SortBase":
        if self.sort_field:
            self.sort_field = camel_to_snake(self.sort_field)
        return self

    def to_mongo_sort(self) -> tuple[str, int] | None:
        if not self.sort_field_snake:
            return None
        return (
            self.sort_field_snake,
            1 if self.direction == SortDirectionEnum.ASC else -1,
        )
