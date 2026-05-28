from enum import StrEnum, auto


class RequirementFieldNameEnum(StrEnum):
    OPTIONS = auto()
    RESPONSE_SCHEMA = auto()


class VisitRequirementsEnum(StrEnum):
    EMPTY = auto()
    FULL = auto()
    WITH_MESSAGES = auto()


class SrvReqCommonEnums:
    """
    Container for output service requirements used enumerations.
    """

    def __init__(self):
        self.VisitRequirements = VisitRequirementsEnum
        self.RequirementFieldName = RequirementFieldNameEnum
