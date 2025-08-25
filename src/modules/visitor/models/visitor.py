from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.common.models import CoreModel
from src.common.repositories.postgres.constants import SchemaNamesEnum


class VisitorModel(CoreModel):
    __table_args__ = {
        "schema": SchemaNamesEnum.VISITS.value
    }

    sid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    full_name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    photo: Mapped[str]
