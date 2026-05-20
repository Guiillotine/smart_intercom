from typing import Generic, TypeVar

from src.common.schemas.core_schema import CoreSchema

ListItemSchema = TypeVar("ListItemSchema")


class ListResult(CoreSchema, Generic[ListItemSchema]):
    items: list[ListItemSchema]
