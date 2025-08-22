from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.common.models import CoreModel
from src.common.repositories.postgres.constants import SchemaNamesEnum



class MessageModel(CoreModel):
    __table_args__ = {
        "schema": SchemaNamesEnum.VISITS.value
    }

    sid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    content: Mapped[str] = mapped_column()

    role: Mapped[int] = mapped_column(String(50))

    time: Mapped[datetime] = mapped_column(DateTime())

    visit_sid: Mapped[UUID] = mapped_column(ForeignKey("visit.sid")) # TODO
