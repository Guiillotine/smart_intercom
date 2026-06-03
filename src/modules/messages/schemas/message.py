from datetime import datetime
from uuid import UUID

from src.common.constants.enums import MessageAuthorRoleEnum
from src.common.decorators import partial_schema
from src.common.schemas import CoreSchema


class MessageBase(CoreSchema):
    visit_sid: UUID
    content: str


class MessageVisitorCreate(MessageBase):
    pass


class MessageBotCreate(MessageBase):
    audio: bytes


class MessageCreate(MessageBase):
    role: MessageAuthorRoleEnum
    time: datetime
    audio_s3_path: str | None = None


@partial_schema
class MessageUpdate(CoreSchema):
    audio_s3_path: str


class Message(MessageBase):
    sid: UUID
    role: MessageAuthorRoleEnum
    time: datetime
    audio_s3_path: str | None = None


class MessageInHistory(CoreSchema):
    time: datetime
    role: MessageAuthorRoleEnum
    content: str
