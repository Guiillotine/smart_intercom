import logging
from typing import Annotated

from fastapi import Depends

from src.common.constants import TokenEnums
from src.common.constants.deps import get_token_enums
from src.common.helpers import TokenHelper, CustomDateTime
from src.common.interfaces import ICustomDateTime, ITokenHelper
from src.common.logger.deps import get_base_logger
from src.config.settings import Settings
from src.config.settings.deps import get_settings


def get_custom_datetime(
    settings: Annotated[Settings, Depends(get_settings)],
) -> ICustomDateTime:
    """
    Dependency provider for ICustomDateTime.

    This function provides an instance of the `CustomDateTime` class, which offers
    methods for retrieving the current datetime either in a naive
    (timezone-unaware) form or in a timezone-aware form based on the application
    configuration.

    :return: An instance of CustomDateTime.
    """

    return CustomDateTime(settings=settings)


def get_token_helper(
    enums: Annotated[TokenEnums, Depends(get_token_enums)],
    logger: Annotated[logging.Logger, Depends(get_base_logger)],
    settings: Annotated[Settings, Depends(get_settings)],
    custom_datetime: Annotated[ICustomDateTime, Depends(get_custom_datetime)],
) -> ITokenHelper:
    """
    Dependency provider for the token management helper.

    Creates and returns a configured TokenHelper instance that handles
    JWT token creation, decoding, validation (access and refresh tokens),
    and supports token blacklist management via Redis.

    :param enums: Injected AuthHlpEnums instance with necessary enums.
    :param logger: Logger instance for logging token operations.
    :param settings: Application settings required for token configuration.
    :param custom_datetime: Custom datetime provider for token expiration handling.
    :return: Initialized TokenHelper.
    """

    return TokenHelper(
        enums=enums,
        logger=logger,
        settings=settings,
        custom_datetime=custom_datetime,
    )
