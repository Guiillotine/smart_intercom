from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.common.repositories.postgres.constants import SchemaNamesEnum


class EmployeeModel(DeclarativeBase):
    __table_args__ = {
        "schema": SchemaNamesEnum.VISITS.value
    }

    sid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    full_name: Mapped[str] = mapped_column(String(100))

    photo: Mapped[str] # TODO: см

    is_deleted: Mapped[bool] = mapped_column(default=False)
