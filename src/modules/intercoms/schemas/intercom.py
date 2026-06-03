from uuid import UUID

from pydantic import Field

from src.common.schemas import CoreSchema


class IntercomStartedVisit(CoreSchema):
    visit_sid: UUID
    hello_message_audio_path: str


class IntercomAnswer(CoreSchema):
    answer_message_audio_path: str
    dialogue_finished: bool = False


class IntercomAnswerWithText(IntercomAnswer):
    answer_message_text: str


class Decision(CoreSchema):
    open: bool | None


class PhotoProcessingResult(CoreSchema):
    detected_employee: bool = False
    message_audio_path: str | None = Field(
        default=None, description="Sets if person was identified"
    )
