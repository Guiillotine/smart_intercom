from datetime import datetime

from fastapi_filter.contrib.sqlalchemy import Filter

from src.common.schemas import SQLFilterBase
from src.modules.persons.constants.enums import PersonTypeEnum
from src.modules.persons.models import PersonModel


class PersonFilter(SQLFilterBase):
    full_name: str | None = None
    person_type: PersonTypeEnum | None = None


    class Constants(Filter.Constants):
        model = PersonModel
