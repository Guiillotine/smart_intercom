from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.models import CoreModel
from src.common.repositories.postgres.constants import SchemaNamesEnum

if TYPE_CHECKING:
    from src.modules.users.models import RoleModel


class UserModel(CoreModel):
    __table_args__ = {
        "schema": SchemaNamesEnum.USERS.value
    }

    sid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    first_name: Mapped[str]

    last_name: Mapped[str]

    middle_name: Mapped[str | None] = mapped_column(nullable=True)

    email: Mapped[str] = mapped_column(unique=True)

    password_hash: Mapped[str]

    role_sid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{SchemaNamesEnum.USERS.value}.role.sid")
    )

    is_active: Mapped[bool] = mapped_column(default=True)

    # Relationships

    role: Mapped["RoleModel"] = relationship(
        "RoleModel", lazy="joined", viewonly=True
    )
