from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.common.models import CoreModel
from src.common.repositories.postgres.constants import SchemaNamesEnum
from src.config.settings.deps import get_settings

settings = get_settings()


class PersonInfoModel(CoreModel):
    __table_args__ = {"schema": SchemaNamesEnum.PERSONS.value}

    sid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    full_name: Mapped[str] = mapped_column(String(100))

    photo: Mapped[str] = mapped_column(comment="S3 path to person photo")

    face_embedding: Mapped[list[float]] = mapped_column(
        Vector(get_settings().postgres.DIMENTION)
    )

    person_type: Mapped[int] = mapped_column(comment="Employee or Visitor")

    is_archived: Mapped[bool]
