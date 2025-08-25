from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.models import CoreModel
from src.common.repositories.postgres.constants import SchemaNamesEnum

if TYPE_CHECKING:
    from src.modules.role.models import RoleModel


class UserModel(CoreModel):
    __table_args__ = {
        "schema": SchemaNamesEnum.USERS.value
    }

    sid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    first_name: Mapped[str] = mapped_column()

    last_name: Mapped[str] = mapped_column()

    middle_name: Mapped[str] = mapped_column(nullable=True)

    email: Mapped[str] = mapped_column(unique=True)

    password_hash: Mapped[str] = mapped_column()

    role_sid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{SchemaNamesEnum.USERS.value}.role.sid")
    )

    is_active: Mapped[bool] = mapped_column(default=True)

    # relationships

    role: Mapped["RoleModel"] = relationship(
        "RoleModel", lazy="joined", viewonly=True
    )
