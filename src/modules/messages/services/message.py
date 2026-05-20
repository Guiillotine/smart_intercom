import logging
from uuid import UUID

from src.common.constants.enums import MessageAuthorRoleEnum
from src.modules.messages.interfaces import IMessagePostgresRepo, IMessageSrv
from src.modules.messages.schemas import (
    Message,
    MessageBotCreate,
    MessageCreate,
    MessageInHistory,
    MessageVisitorCreate,
)
from src.modules.messages.services.constants import MessageSrvConsts, MessageSrvEnums


class MessageSrv(IMessageSrv):
    def __init__(
        self,
        logger: logging.Logger,
        enums: MessageSrvEnums,
        consts: MessageSrvConsts,
        message_repo: IMessagePostgresRepo,
    ):
        self._logger = logger
        self._enums = enums
        self._consts = consts
        self._message_repo = message_repo

    async def create_visitor_message(
        self, message_in: MessageVisitorCreate
    ) -> Message:
        return await self._create(
            MessageCreate(
                visit_sid=message_in.visit_sid,
                content=message_in.content,
                role=MessageAuthorRoleEnum.USER,
            )
        )

    async def create_bot_message(self, message_in: MessageBotCreate) -> Message:
        return await self._create(
            MessageCreate(
                visit_sid=message_in.visit_sid,
                content=message_in.content,
                role=MessageAuthorRoleEnum.ASSISTANT,
                audio=message_in.audio_s3_path,
            )
        )

    async def get_messages(self, visit_sid: UUID) -> list[Message]:
        return [
            Message.model_validate(message)
            for message in await self._message_repo.get_by_visit_sid(visit_sid)
        ]

    async def get_message_history(self, visit_sid: UUID) -> list[MessageInHistory]:
        return [
            MessageInHistory.model_validate(message)
            for message in await self._message_repo.get_by_visit_sid(visit_sid)
        ]

    async def _create(self, message_in: MessageCreate) -> Message:
        return Message.model_validate(await self._message_repo.create(obj_in=message_in))
