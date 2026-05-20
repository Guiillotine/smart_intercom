from typing import Annotated

from fastapi import Depends

from src.common.constants import ErrorCodesEnums, TokenEnums
from src.common.constants.deps import get_error_codes_enums, get_token_enums
from src.config.settings import Settings
from src.config.settings.deps import get_settings
from src.modules.users.interfaces import IAuthUC, IUserSrv, IUserUC
from src.modules.users.services.deps import get_user_service
from src.modules.users.usecases.constants import UserUCConsts, UserUCEnums
from src.modules.users.usecases.constants.deps import (
    get_user_uc_consts,
    get_user_uc_enums,
)
from src.modules.users.usecases.user import AuthUC, UserUC


async def get_user_usecase(
    enums: Annotated[UserUCEnums, Depends(get_user_uc_enums)],
    consts: Annotated[UserUCConsts, Depends(get_user_uc_consts)],
    user_service: Annotated[IUserSrv, Depends(get_user_service)],
) -> IUserUC:
    return UserUC(enums=enums, consts=consts, user_service=user_service)


async def get_auth_usecase(
    errors: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    token_enums: Annotated[TokenEnums, Depends(get_token_enums)],
    enums: Annotated[UserUCEnums, Depends(get_user_uc_enums)],
    consts: Annotated[UserUCConsts, Depends(get_user_uc_consts)],
    settings: Annotated[Settings, Depends(get_settings)],
    user_service: Annotated[IUserSrv, Depends(get_user_service)],
) -> IAuthUC:
    return AuthUC(
        errors=errors,
        token_enums=token_enums,
        enums=enums,
        consts=consts,
        settings=settings,
        user_service=user_service,
    )
