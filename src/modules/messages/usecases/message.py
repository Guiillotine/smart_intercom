from uuid import UUID

from src.common.schemas import Pagination, PaginationResult
from src.modules.messages.interfaces import IMessageSrv, IMessageUC
from src.modules.messages.schemas import MessageInHistory
from src.modules.messages.usecases.constants import MessageUCConsts, MessageUCEnums


class MessageUC(IMessageUC):
    def __init__(
        self,
        enums: MessageUCEnums,
        consts: MessageUCConsts,
        message_service: IMessageSrv,
    ):
        self._enums = enums
        self._consts = consts
        self._message_service = message_service

    async def get_message_history(
        self,
        user_sid: UUID,
        visit_sid: UUID,
        pagination_params: Pagination,
    ) -> PaginationResult[MessageInHistory]:
        # TODO: pagination
        return await self._message_service.get_message_history(
            visit_sid=visit_sid
        )
