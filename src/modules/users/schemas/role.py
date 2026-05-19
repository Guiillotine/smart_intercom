from src.common.decorators import partial_schema
from src.common.schemas import CoreSchema


class RoleBase(CoreSchema):
    id: int
    name: str


class RoleCreate(RoleBase):
    description: str | None = None


@partial_schema
class RoleUpdate(RoleBase):
    description: str | None = None


class Role(RoleBase):
    description: str | None = None
