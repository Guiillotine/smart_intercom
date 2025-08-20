
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.common.models import CoreModel


class UserModel(CoreModel):
    sid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    middle_name: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    role_sid: Mapped[UUID] = mapped_column(
        ForeignKey(), # TODO
    )
    is_active: Mapped[bool] = mapped_column(default=True)
