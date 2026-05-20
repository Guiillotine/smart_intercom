import logging
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.client.storages.deps import get_db
from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes_enums
from src.common.logger.deps import get_message_logger
from src.modules.messages.adapters.repositories.constants import (
    MessageRepoConsts,
    MessageRepoEnums,
)
from src.modules.messages.adapters.repositories.constants.deps import (
    get_message_repo_consts,
    get_message_repo_enums,
)
from src.modules.messages.adapters.repositories.message import MessagePostgresRepo
from src.modules.messages.interfaces import IMessagePostgresRepo


async def get_message_pg_repo(
    db: Annotated[AsyncSession, Depends(get_db)],
    logger: Annotated[logging.Logger, Depends(get_message_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    enums: Annotated[MessageRepoEnums, Depends(get_message_repo_enums)],
    consts: Annotated[MessageRepoConsts, Depends(get_message_repo_consts)],
) -> IMessagePostgresRepo:
    return MessagePostgresRepo(
        db=db,
        logger=logger,
        errors=error_codes,
        enums=enums,
        consts=consts,
    )
