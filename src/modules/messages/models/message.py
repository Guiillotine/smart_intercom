from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.common.models import CoreModel
from src.common.adapters.repositories.postgres.constants import SchemaNamesEnum
from src.common.utils import table_args


class MessageModel(CoreModel):
    __table_args__ = table_args(schema=SchemaNamesEnum.MESSAGES)

    sid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    content: Mapped[str] = mapped_column()

    role: Mapped[int] = mapped_column(String(50))

    time: Mapped[datetime] = mapped_column(DateTime())

    audio: Mapped[str | None] = mapped_column(
        nullable=True, comment="S3 path to audio file"
    )

    visit_sid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{SchemaNamesEnum.VISITS.value}.visit.sid")
    )
