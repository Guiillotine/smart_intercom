from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.common.models import CoreModel
from src.common.adapters.repositories.postgres.constants import SchemaNamesEnum
from src.common.utils import table_args


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

    purpose: Mapped[str | None] = mapped_column(
        nullable=True, comment="Purpose of the visit detected by bot",
    )

    finish_reason: Mapped[str | None] = mapped_column(
        nullable=True, comment="The reason the visit was finished",
    )

    dialog_lang: Mapped[int] = mapped_column(comment="Visit dialog language")

    photo: Mapped[str] = mapped_column(comment="S3 path to photo of the visit")

    decision_by_user_sid: Mapped[UUID | None] = mapped_column(
        ForeignKey(f"{SchemaNamesEnum.USERS.value}.user.sid"),
        nullable=True,
    )


class VisitPersonModel(CoreModel):
    __table_args__ = table_args(schema=SchemaNamesEnum.VISITS)

    sid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    detected_sex: Mapped[int | None] = mapped_column(nullable=True)

    detected_age: Mapped[int | None] = mapped_column(nullable=True)

    photo: Mapped[str] = mapped_column(
        comment="S3 path to photo of a person taken during a visit"
    )

    person_sid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{SchemaNamesEnum.PERSONS.value}.person.sid"),
    )

    visit_sid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{SchemaNamesEnum.VISITS.value}.visit.sid"),
    )
