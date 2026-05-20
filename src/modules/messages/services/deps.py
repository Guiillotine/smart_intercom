import logging
from typing import Annotated

from fastapi import Depends

from src.common.logger.deps import get_message_logger
from src.modules.messages.adapters.repositories.deps import get_message_pg_repo
from src.modules.messages.interfaces import IMessagePostgresRepo, IMessageSrv
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
    message_repo: Annotated[IMessagePostgresRepo, Depends(get_message_pg_repo)],
) -> IMessageSrv:
    return MessageSrv(
        logger=logger,
        enums=enums,
        consts=consts,
        message_repo=message_repo,
    )
