from typing import ClassVar, Callable

from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from src.common.constants.srv_req_enums import RequirementFieldNameEnum, \
    VisitRequirementsEnum
from src.modules.visits.models import VisitModel, VisitPersonModel
from src.modules.visits.schemas import Visit, VisitWithMessages, VisitFull


class VisitCustomOptions:
    @staticmethod
    def empty() -> list[ExecutableOption]:
        return []

    @staticmethod
    def with_messages() -> list[ExecutableOption]:
        return [selectinload(VisitModel.messages)]

    @staticmethod
    def full() -> list[ExecutableOption]:
        return [
            selectinload(VisitModel.messages),
            selectinload(VisitModel.visitors).selectinload(VisitPersonModel.person),
        ]


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
    GET_BY_SID: ClassVar[
        dict[VisitRequirementsEnum, dict[RequirementFieldNameEnum, Callable]]
    ] = {
        VisitRequirementsEnum.EMPTY: {
            RequirementFieldNameEnum.OPTIONS: VisitCustomOptions.empty,
            RequirementFieldNameEnum.RESPONSE_SCHEMA: Visit,
        },
        VisitRequirementsEnum.FULL: {
            RequirementFieldNameEnum.OPTIONS: VisitCustomOptions.full,
            RequirementFieldNameEnum.RESPONSE_SCHEMA: VisitFull,
        },
    }


class VisitRespSchemas:
    GET_ALL = Visit | VisitWithMessages
    GET_BY_SID = Visit | VisitFull


class VisitSrvConsts:
    def __init__(self):
        self.Requirements = VisitRequirements
        self.CustomOptions = VisitCustomOptions
