from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.common.models import CoreModel
from src.common.repositories.postgres.constants import SchemaNamesEnum


class VisitModel(CoreModel):
    __table_args__ = (
        CheckConstraint(
            "((employee_sid IS NOT NULL OR visitor_sid IS NOT NULL)"
            "AND (employee_sid IS NULL OR visitor_sid IS NULL))",
            name='employee_xor_visitor_fk'
        ),
        {"schema": SchemaNamesEnum.VISITS.value}
    )

    sid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    photo: Mapped[str]

    detected_sex: Mapped[int] = mapped_column()

    detected_age: Mapped[int] = mapped_column()

    granted_access: Mapped[bool] = mapped_column(default=False)

    arrival_time: Mapped[datetime] = mapped_column(DateTime())

    decision_time: Mapped[datetime] = mapped_column(DateTime())

    employee_sid: Mapped[UUID | None] = mapped_column(
        ForeignKey("EmployeeModel.sid"), nullable=True
    )

    visitor_sid: Mapped[UUID | None] = mapped_column(
        ForeignKey("VisitorModel.sid"), nullable=True
    )

    decision_by_user_sid: Mapped[UUID | None] = mapped_column(
        ForeignKey("UserModel.sid"), nullable=True
    )
