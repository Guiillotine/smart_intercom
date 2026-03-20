from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, field_validator, ConfigDict
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        validate_by_name = True


class CoreSchema(CamelModel):
    @field_validator("*", mode="after")
    def timezone_validate(cls, v: Any) -> Any:
        if isinstance(v, datetime) and v.tzinfo is not None:
            v = v.replace(tzinfo=None)
        return v

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            UUID: lambda v: str(v),
            datetime: lambda v: v.isoformat() + "Z",
        },
        populate_by_name=True,
    )
