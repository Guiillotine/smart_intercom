from uuid import UUID

from src.common.constants.enums import MessageAuthorRoleEnum
from src.common.schemas import CoreSchema


class MessageBase(CoreSchema):
  visit_sid: UUID
  content: str


class MessageVisitorCreate(MessageBase):
  pass


class MessageBotCreate(MessageBase):
  audio_s3_path: str


class MessageCreate(MessageBase):
  role: MessageAuthorRoleEnum


class MessageUpdate(CoreSchema):
  pass


class Message(MessageBase):
  role: MessageAuthorRoleEnum
  audio_s3_path: str | None = None
