from typing import Annotated
from uuid import UUID

from fastapi import Depends

from src.common.constants import ErrorCodesEnums, TokenEnums
from src.common.constants.deps import get_token_enums, get_error_codes_enums
from src.common.deps import oauth2_scheme

from src.common.errors import BackendException
from src.common.helpers.deps import get_token_helper
from src.common.interfaces import ITokenHelper
from src.modules.users.constants.enums import RoleEnum


async def get_user_sid(
    token_credentials: Annotated[str, Depends(oauth2_scheme)],
    enums: Annotated[TokenEnums, Depends(get_token_enums)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    token_helper: Annotated[ITokenHelper, Depends(get_token_helper)],
):
    """
    Extract and validate the user session ID (SID) from the Authorization header.

    :param token_credentials: Incoming JWT token credentials from headers.
    :param enums: TokenEnums instance containing payload field names.
    :param error_codes: ErrorCodesEnums with application error codes.
    :param token_helper: Service for decoding and validating JWT tokens.
    :return: User session ID.
    """

    try:
        payload = token_helper.decode_token(token_credentials)

    except Exception as err:
        raise BackendException(error_codes.Auth.INVALID_ACCESS_TOKEN) from err
    return UUID(payload[enums.AuthPayloadFields.SUB])


async def get_token_data(
    token_credentials: Annotated[str, Depends(oauth2_scheme)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    token_helper: Annotated[ITokenHelper, Depends(get_token_helper)],
) -> dict:
    """
    Extract and validate the user data from the Authorization header.

    :param token_credentials: Incoming JWT token credentials from headers.
    :param error_codes: ErrorCodesEnums with application error codes.
    :param token_helper: Service for decoding and validating JWT tokens.
    :return: Dict with current user data.
    """

    try:
        payload = token_helper.decode_token(token_credentials)

    except Exception as err:
        raise BackendException(error_codes.Auth.INVALID_ACCESS_TOKEN) from err
    return payload


async def get_user_role(
    token_data: Annotated[dict, Depends(get_token_data)],
    enums: Annotated[TokenEnums, Depends(get_token_enums)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
) -> RoleEnum:
    try:
        return RoleEnum(token_data[enums.AuthPayloadFields.STATUS])
    except (KeyError, TypeError, ValueError) as err:
        raise BackendException(error_codes.Auth.INVALID_ACCESS_TOKEN) from err


async def require_admin(
    user_sid: Annotated[UUID, Depends(get_user_sid)],
    role: Annotated[RoleEnum, Depends(get_user_role)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
) -> UUID:
    if role not in RoleEnum.get_admin_roles():
        raise BackendException(error=error_codes.Common.FORBIDDEN)
    return user_sid
