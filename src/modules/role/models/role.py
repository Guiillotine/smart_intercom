from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.common.models import CoreModel
from src.common.repositories.postgres.constants import SchemaNamesEnum


class RoleModel(CoreModel):
    __table_args__ = {
        "schema": SchemaNamesEnum.USERS.value
    }

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(50), unique=True)
