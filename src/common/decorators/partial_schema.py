from copy import deepcopy
from typing import Any

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo


def partial_schema(model: type[BaseModel]):
    """
    Creates a new Pydantic model class based on the given model,
    making all fields optional by setting their default to None and
    updating their type annotation to be nullable.

    :param model: The Pydantic BaseModel class to create a partial version of.
    :return: A new Pydantic model class with all fields optional.
    """

    def make_field_optional(
        field: FieldInfo,
        default: Any = None,
    ) -> tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = field.annotation | None
        return new.annotation, new

    return create_model(
        f"Partial{model.__name__}",
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.model_fields.items()
        },
    )
