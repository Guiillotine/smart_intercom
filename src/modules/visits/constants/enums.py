from enum import StrEnum, auto, IntEnum


class VisitStatusEnum(StrEnum):
    IN_PROCESS = auto()
    ASKED_WANT_TO_ENTER = auto()
    WAITING_DECISION = auto()
    OVER = auto()


class VisitFinishReasonEnum(IntEnum):
    """Why visit was finished"""
    EMPLOYEE_DECISION = 1
    CANCELLED_BY_VISITOR = 2
    TIMEOUT = 3


class VisitHandoffReasonEnum(IntEnum):
    """Why employee was called"""
    READY_FOR_EMPLOYEE_DECISION = 1
    EMPLOYEE_RECOGNIZED = 2
    VISITOR_REQUESTED_EMPLOYEE = 3
    BOT_ERROR = 4


class VisitSortFieldsEnum(StrEnum):
    START_DATETIME = "startDatetime"
    FINISH_DATETIME = "finishDatetime"


class VisitEnums:
    def __init__(self):
        self.Status = VisitStatusEnum
        self.SortFields = VisitSortFieldsEnum
        self.FinishReason = VisitFinishReasonEnum
        self.HandoffReason = VisitHandoffReasonEnum
