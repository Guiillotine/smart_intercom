from sqlalchemy.orm import Mapped, mapped_column

from src.common.models import CoreModel
from src.common.adapters.repositories.postgres.constants import SchemaNamesEnum
from src.common.utils import table_args


class RoleModel(CoreModel):
    __table_args__ = table_args(schema=SchemaNamesEnum.USERS)

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(comment="User role name")

    description: Mapped[str | None]
