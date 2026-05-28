from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.models import CoreModel
from src.common.adapters.repositories.postgres.constants import SchemaNamesEnum
from src.common.utils import table_args

if TYPE_CHECKING:
    from src.modules.visits.models import VisitModel


class MessageModel(CoreModel):
    __table_args__ = table_args(schema=SchemaNamesEnum.MESSAGES)

    sid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    content: Mapped[str] = mapped_column()

    role: Mapped[int] = mapped_column(String(50))

    time: Mapped[datetime] = mapped_column(DateTime())

    audio_s3_path: Mapped[str | None] = mapped_column(
        nullable=True, comment="S3 path to audio file"
    )

    visit_sid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{SchemaNamesEnum.VISITS.value}.visit.sid")
    )

    # Relationships

    visit: Mapped["VisitModel"] = relationship(back_populates="messages")
