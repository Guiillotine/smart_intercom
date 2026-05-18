from uuid import UUID

from src.common.schemas import CoreSchema


class IntercomStartedVisit(CoreSchema):
    visit_sid: UUID
    hello_message_audio_path: str


class IntercomAnswer(CoreSchema):
    answer_message_audio_path: str
    dialog_finished: bool = False


class Decision(CoreSchema):
    open: bool
