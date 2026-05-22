from uuid import UUID

from fastapi_filter.contrib.sqlalchemy import Filter

from src.common.schemas import SQLFilterBase
from src.modules.messages.models import MessageModel


class MessageFilter(SQLFilterBase):
    visit_sid: UUID | None = None

    class Constants(Filter.Constants):
        model = MessageModel
