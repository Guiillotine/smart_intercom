from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.common.models import CoreModel
from src.common.repositories.postgres.constants import SchemaNamesEnum
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

    arrival_datetime: Mapped[datetime] = mapped_column(DateTime())

    decision_datetime: Mapped[datetime | None] = mapped_column(
        DateTime(),
        nullable=True,
    )

    status: Mapped[int] = mapped_column()

    purpose: Mapped[str | None] = mapped_column(
        nullable=True, comment="Purpose of the visit detected by bot",
    )

    decision_by_user_sid: Mapped[UUID | None] = mapped_column(
        ForeignKey("UserModel.sid"),
        nullable=True,
    )


class VisitPersonModel(CoreModel):
    __table_args__ = table_args(schema=SchemaNamesEnum.VISITS)

    sid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    detected_sex: Mapped[int | None] = mapped_column(nullable=True)

    detected_age: Mapped[int | None] = mapped_column(nullable=True)

    person_sid: Mapped[UUID] = mapped_column(ForeignKey("PersonInfoModel.sid"))

    visit_sid: Mapped[UUID] = mapped_column(ForeignKey("VisitModel.sid"))

    photo: Mapped[str] = mapped_column(comment="S3 path to photo of the visit")
