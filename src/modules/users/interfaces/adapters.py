from abc import ABC

from src.common.interfaces import IPostgresBaseRepo
from src.modules.users.models import RoleModel
from src.modules.users.schemas import RoleCreate, RoleUpdate


class IRolePostgresRepo(IPostgresBaseRepo[RoleModel, RoleCreate, RoleUpdate], ABC):
    """
    Interface for user role repository operations.

    Extends base PostgreSQL repository with additional role-specific operations.
    """
    pass
