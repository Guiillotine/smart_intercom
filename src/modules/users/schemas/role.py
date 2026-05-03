from src.common.decorators import partial_schema
from src.common.schemas import CoreSchema


class RoleBase(CoreSchema):
    id: int
    name: str
    description: str | None = None


class RoleCreate(RoleBase):
    pass


@partial_schema
class RoleUpdate(RoleBase):
    pass


class Role(RoleBase):
    pass
