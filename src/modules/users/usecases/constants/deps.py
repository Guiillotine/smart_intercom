from typing import Annotated

from fastapi.params import Depends

from src.common.constants import TokenEnums
from src.common.constants.deps import get_token_enums
from src.modules.users.constants import UserEnums
from src.modules.users.constants.deps import get_user_common_enums
from src.modules.users.usecases.constants import UserUCConsts, UserUCEnums, AuthUCEnums
from src.modules.users.usecases.constants.consts import AuthUCConsts


def get_user_uc_enums() -> UserUCEnums:
    return UserUCEnums()


def get_auth_uc_enums(
    token_enums: Annotated[TokenEnums, Depends(get_token_enums)],
    user_common_enums: Annotated[UserEnums, Depends(get_user_common_enums)],
) -> AuthUCEnums:
    return AuthUCEnums(
        token_enums=token_enums,
        user_common_enums=user_common_enums,
    )


def get_user_uc_consts() -> UserUCConsts:
    return UserUCConsts()


def get_auth_uc_consts() -> AuthUCConsts:
    return AuthUCConsts()
