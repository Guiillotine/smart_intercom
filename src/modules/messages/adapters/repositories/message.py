import logging
from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.adapters.repositories.postgres import PostgresBaseRepo
from src.common.constants import ErrorCodesEnums
from src.modules.messages.interfaces import IMessagePostgresRepo
from src.modules.messages.models import MessageModel
from src.modules.messages.schemas import MessageCreate, MessageUpdate
from src.modules.messages.adapters.repositories.constants import (
    MessageRepoConsts,
    MessageRepoEnums,
)


class MessagePostgresRepo(
    PostgresBaseRepo[MessageModel, MessageCreate, MessageUpdate],
    IMessagePostgresRepo,
):
    def __init__(
        self,
        db: AsyncSession,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
        enums: MessageRepoEnums,
        consts: MessageRepoConsts,
    ):
        super().__init__(db=db, model=MessageModel, errors=errors, logger=logger)
        self._enums = enums
        self._consts = consts

    async def get_by_visit_sid(self, visit_sid: UUID) -> Sequence[MessageModel]:
        query = (
            select(MessageModel)
            .where(MessageModel.visit_sid == visit_sid)
            .order_by(MessageModel.time.asc())
        )
        return await self._get_all_results(query)
