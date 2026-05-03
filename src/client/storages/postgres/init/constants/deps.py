from typing import Annotated

from fastapi import Depends

from src.client.storages.postgres.init.constants import PostgresInitEnums
from src.modules.users.constants import UserEnums
from src.modules.users.constants.deps import get_user_common_enums


async def get_postgres_init_enums(
    user_common_enums: Annotated[UserEnums, Depends(get_user_common_enums)],
) -> PostgresInitEnums:
    return PostgresInitEnums(user_common_enums=user_common_enums)
