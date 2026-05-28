from enum import StrEnum, auto, IntEnum


class VisitStatusEnum(IntEnum):
    """Visit state"""
    IN_PROCESS = 1
    ASKED_WANT_TO_ENTER = 2
    WAITING_DECISION = 3
    OVER = 4


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
