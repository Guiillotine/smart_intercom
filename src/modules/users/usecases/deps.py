import logging
from typing import Annotated

from fastapi import Depends

from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes_enums
from src.common.helpers.deps import get_password_helper
from src.common.interfaces import IPasswordHelper
from src.common.logger.deps import get_user_logger
from src.config.settings import Settings
from src.config.settings.deps import get_settings
from src.modules.users.interfaces import IAuthUC, IUserSrv, IUserUC, IAuthSrv, \
    ITokenProviderSrv
from src.modules.users.services.deps import get_user_service, get_auth_service, \
    get_token_provider_service
from src.modules.users.usecases.constants import UserUCConsts, UserUCEnums, AuthUCEnums
from src.modules.users.usecases.constants.consts import AuthUCConsts
from src.modules.users.usecases.constants.deps import (
    get_user_uc_consts,
    get_user_uc_enums, get_auth_uc_enums,
)
from src.modules.users.usecases import AuthUC, UserUC


async def get_user_usecase(
    enums: Annotated[UserUCEnums, Depends(get_user_uc_enums)],
    consts: Annotated[UserUCConsts, Depends(get_user_uc_consts)],
    user_service: Annotated[IUserSrv, Depends(get_user_service)],
) -> IUserUC:
    return UserUC(enums=enums, consts=consts, user_service=user_service)


async def get_auth_usecase(
    logger: Annotated[logging.Logger, Depends(get_user_logger)],
    errors: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    enums: Annotated[AuthUCEnums, Depends(get_auth_uc_enums)],
    consts: Annotated[AuthUCConsts, Depends(get_user_uc_consts)],
    settings: Annotated[Settings, Depends(get_settings)],
    user_service: Annotated[IUserSrv, Depends(get_user_service)],
    auth_service: Annotated[IAuthSrv, Depends(get_auth_service)],
    password_helper: Annotated[IPasswordHelper, Depends(get_password_helper)],
    token_provider_service: Annotated[
        ITokenProviderSrv, Depends(get_token_provider_service),
    ],
) -> IAuthUC:
    return AuthUC(
        logger=logger,
        errors=errors,
        enums=enums,
        consts=consts,
        settings=settings,
        password_helper=password_helper,
        user_service=user_service,
        auth_service=auth_service,
        token_provider_service=token_provider_service,
    )
