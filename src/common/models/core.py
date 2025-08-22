from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from src.common.utils import CustomDatetime


class CoreModel(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(), default=CustomDatetime.get_utc_datetime
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        default=CustomDatetime.get_utc_datetime,
        onupdate=CustomDatetime.get_utc_datetime,
    )

    @classmethod
    @declared_attr
    def __tablename__(cls):
        name = cls.__name__.replace("Model", "")
        snake_case_name = [name[0].lower()]
        for c in name[1:]:
            snake_case_name.append("_" + c.lower() if c.isupper() else c)

        return "".join(snake_case_name)
