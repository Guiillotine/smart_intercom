from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.models import CoreModel
from src.common.adapters.repositories.postgres.constants import SchemaNamesEnum
from src.common.utils import table_args

if TYPE_CHECKING:
    from src.modules.messages.models import MessageModel
    from src.modules.persons.models import PersonModel


class VisitModel(CoreModel):
    __table_args__ = table_args(schema=SchemaNamesEnum.VISITS)

    sid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    granted_access: Mapped[bool | None] = mapped_column(
        nullable=True,
        comment="User's decision to grant access",
    )

    bot_granted_access: Mapped[bool | None] = mapped_column(
        nullable=True,
        comment="Bot's recommendation to grant access",
    )

    start_datetime: Mapped[datetime] = mapped_column(DateTime())

    finish_datetime: Mapped[datetime] = mapped_column(DateTime(), nullable=True,)

    status: Mapped[int] = mapped_column()

    visitor_goal: Mapped[str | None] = mapped_column(
        nullable=True, comment="Purpose of the visit detected by bot",
    )

    dialogue_lang: Mapped[str] = mapped_column(comment="Visit dialogue language")

    photo_s3_path: Mapped[str | None] = mapped_column(
        nullable=True,
        comment="S3 path to photo of the visit",
    )

    finish_reason: Mapped[int | None] = mapped_column(
        comment="Why visit was finished",
        nullable=True,
    )

    handoff_reason: Mapped[int | None] = mapped_column(
        comment="Why employee was called",
        nullable=True,
    )

    decision_by_user_sid: Mapped[UUID | None] = mapped_column(
        ForeignKey(f"{SchemaNamesEnum.USERS.value}.user.sid"),
        nullable=True,
    )

    # Relationships

    messages: Mapped[list["MessageModel"]] = relationship(back_populates="visit")

    visitors: Mapped[list["VisitPersonModel"]] = relationship(back_populates="visit")


class VisitPersonModel(CoreModel):
    __table_args__ = table_args(schema=SchemaNamesEnum.VISITS)

    sid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    detected_sex: Mapped[int | None] = mapped_column(nullable=True)

    detected_age: Mapped[int | None] = mapped_column(nullable=True)

    crop_coords: Mapped[list[int]] = mapped_column(
        JSONB,
        comment="Visitor face coords on photo: y1, y2, x1, x2"
    )

    person_sid: Mapped[UUID | None] = mapped_column(
        ForeignKey(f"{SchemaNamesEnum.PERSONS.value}.person.sid"), nullable=True
    )

    visit_sid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{SchemaNamesEnum.VISITS.value}.visit.sid"),
    )

    # Relationships

    visit: Mapped["VisitModel"] = relationship(back_populates="visitors")

    person: Mapped["PersonModel | None"] = relationship()
