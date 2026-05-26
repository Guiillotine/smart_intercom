from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, field_validator, ConfigDict
from pydantic.alias_generators import to_camel


class CoreSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        json_encoders={
            UUID: lambda v: str(v),
            datetime: lambda v: v.isoformat() + "Z",
        },
    )

    @field_validator("*", mode="after")
    @classmethod
    def timezone_validate(cls, v: Any) -> Any:
        if isinstance(v, datetime) and v.tzinfo is not None:
            v = v.replace(tzinfo=None)
        return v
