import logging
from uuid import UUID

from src.common.constants.enums import MessageAuthorRoleEnum
from src.common.interfaces import ICustomDateTime
from src.common.schemas import PaginationResult, Pagination, SortBase, ListResult
from src.common.schemas.constants.enums import SortDirectionEnum
from src.config.settings import Settings
from src.modules.messages.filters import MessageFilter
from src.modules.messages.interfaces import IMessagePostgresRepo, IMessageSrv, \
    IMessageS3Repo
from src.modules.messages.schemas import (
    Message,
    MessageBotCreate,
    MessageCreate,
    MessageInHistory,
    MessageVisitorCreate, MessageUpdate,
)
from src.modules.messages.services.constants import MessageSrvConsts, MessageSrvEnums


class MessageSrv(IMessageSrv):
    def __init__(
        self,
        logger: logging.Logger,
        enums: MessageSrvEnums,
        consts: MessageSrvConsts,
        settings: Settings,
        custom_datetime: ICustomDateTime,
        message_s3_repo: IMessageS3Repo,
        message_postgres_repo: IMessagePostgresRepo,
    ):
        self._logger = logger
        self._enums = enums
        self._consts = consts
        self._settings = settings
        self._custom_datetime = custom_datetime
        self._message_s3_repo = message_s3_repo
        self._message_postgres_repo = message_postgres_repo

    async def create_visitor_message(
        self, message_in: MessageVisitorCreate
    ) -> Message:
        return Message.model_validate(
            await self._message_postgres_repo.create(
                obj_in=MessageCreate(
                    role=MessageAuthorRoleEnum.USER,
                    time=self._custom_datetime.get_utc_datetime(),
                    content=message_in.content,
                    visit_sid=message_in.visit_sid,
                )
            )
        )

    async def create_bot_message(
        self,
        message_in: MessageBotCreate,
    ) -> Message:
        created_message = await self._message_postgres_repo.create(
            obj_in=MessageCreate(
                role=MessageAuthorRoleEnum.ASSISTANT,
                time=self._custom_datetime.get_utc_datetime(),
                content=message_in.content,
                visit_sid=message_in.visit_sid,
            )
        )

        audio_s3_path = await self._message_s3_repo.put_object(
            key=self._get_bot_message_key(message_in.visit_sid, created_message.sid),
            data=message_in.audio,
            bucket=self._settings.s3.S3_BOT_MESSAGE_BUCKET_NAME,
        )

        return Message.model_validate(
            await self._message_postgres_repo.update(
                db_obj=created_message,
                obj_in=MessageUpdate(audio_s3_path=audio_s3_path),
            )
        )

    async def get_messages(
        self,
        visit_sid: UUID,
        sort_params: SortBase | None = None,
    ) -> ListResult[Message]:
        if not sort_params:
            sort_params = SortBase(
                sort_field="time",
                direction=self._enums.Schema.SortDirection.ASC,
            )

        messages = await self._message_postgres_repo.get_all(
            filters=MessageFilter(visit_sid=visit_sid),
            sort_params=sort_params,
        )

        return ListResult[Message](items=messages)

    async def get_message_history(
        self,
        visit_sid: UUID,
        pagination_params: Pagination,
    ) -> PaginationResult[MessageInHistory]:
        messages, total = await self._message_postgres_repo.get_all_paginated(
            filters=MessageFilter(visit_sid=visit_sid),
            sort_params=SortBase(
                sort_field="time",
                direction=self._enums.Schema.SortDirection.ASC,
            ),
            pagination_params=pagination_params,
        )

        return PaginationResult[MessageInHistory](
            items=messages,
            limit=pagination_params.limit,
            offset=pagination_params.offset,
            total=total,
        )

    def _get_bot_message_key(
        self,
        sid: UUID,
        visit_sid: UUID,
    ) -> str:
        return f"{self._enums.Common.S3Prefix.BOT_MESSAGE}/{visit_sid}/{sid}"
