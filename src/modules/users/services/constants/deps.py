from typing import Annotated

from fastapi import Depends

from src.common.constants import TokenEnums
from src.common.constants.deps import get_token_enums
from src.modules.users.services.constants import UserSrvConsts, UserSrvEnums
from src.modules.users.services.constants.enums import AuthSrvEnums


def get_user_srv_enums() -> UserSrvEnums:
    return UserSrvEnums()


def get_user_srv_consts() -> UserSrvConsts:
    return UserSrvConsts()


def get_auth_srv_enums(
    token_enums: Annotated[TokenEnums, Depends(get_token_enums)],
) -> AuthSrvEnums:
    return AuthSrvEnums(token_enums=token_enums)
