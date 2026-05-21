import logging
from typing import Annotated

from fastapi import Depends

from src.common.helpers.deps import get_custom_datetime
from src.common.interfaces import ICustomDateTime
from src.common.logger.deps import get_message_logger
from src.config.settings import Settings
from src.config.settings.deps import get_settings
from src.modules.messages.adapters.repositories.postgres.deps import get_message_postgres_repo
from src.modules.messages.adapters.repositories.s3.deps import get_message_s3_repo
from src.modules.messages.interfaces import IMessagePostgresRepo, IMessageSrv, \
    IMessageS3Repo
from src.modules.messages.services.message import MessageSrv
from src.modules.messages.services.constants import MessageSrvConsts, MessageSrvEnums
from src.modules.messages.services.constants.deps import (
    get_message_srv_consts,
    get_message_srv_enums,
)


async def get_message_service(
    logger: Annotated[logging.Logger, Depends(get_message_logger)],
    enums: Annotated[MessageSrvEnums, Depends(get_message_srv_enums)],
    consts: Annotated[MessageSrvConsts, Depends(get_message_srv_consts)],
    settings: Annotated[Settings, Depends(get_settings)],
    message_s3_repo: Annotated[IMessageS3Repo, Depends(get_message_s3_repo)],
    message_postgres_repo: Annotated[
        IMessagePostgresRepo, Depends(get_message_postgres_repo)
    ],
    custom_datetime: Annotated[ICustomDateTime, Depends(get_custom_datetime)],
) -> IMessageSrv:
    return MessageSrv(
        logger=logger,
        enums=enums,
        consts=consts,
        settings=settings,
        custom_datetime=custom_datetime,
        message_s3_repo=message_s3_repo,
        message_postgres_repo=message_postgres_repo,
    )
