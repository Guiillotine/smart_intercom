from fastapi_filter.contrib.sqlalchemy import Filter

from src.common.schemas import SQLFilterBase
from src.modules.visits.constants.enums import VisitStatusEnum
from src.modules.visits.models import VisitModel


class VisitFilter(SQLFilterBase):
    status: VisitStatusEnum | None = None

    class Constants(Filter.Constants):
        model = VisitModel
