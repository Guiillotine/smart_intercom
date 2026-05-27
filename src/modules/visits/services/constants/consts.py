from typing import ClassVar, Callable

from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from src.common.constants.srv_req_enums import RequirementFieldNameEnum, \
    VisitRequirementsEnum
from src.modules.visits.models import VisitModel
from src.modules.visits.schemas import Visit, VisitWithMessages


class VisitCustomOptions:
    @staticmethod
    def empty() -> list[ExecutableOption]:
        return []

    @staticmethod
    def with_messages() -> list[ExecutableOption]:
        return [selectinload(VisitModel.messages)]


class VisitRequirements:
    GET_ALL: ClassVar[
        dict[VisitRequirementsEnum, dict[RequirementFieldNameEnum, Callable]]
    ] = {
        VisitRequirementsEnum.EMPTY: {
            RequirementFieldNameEnum.OPTIONS: VisitCustomOptions.empty,
            RequirementFieldNameEnum.RESPONSE_SCHEMA: Visit,
        },
        VisitRequirementsEnum.WITH_MESSAGES: {
            RequirementFieldNameEnum.OPTIONS: VisitCustomOptions.with_messages,
            RequirementFieldNameEnum.RESPONSE_SCHEMA: VisitWithMessages,
        },
    }


class VisitRespSchemas:
    GET_ALL = Visit | VisitWithMessages


class VisitSrvConsts:
    def __init__(self):
        self.Requirements = VisitRequirements
        self.CustomOptions = VisitCustomOptions
