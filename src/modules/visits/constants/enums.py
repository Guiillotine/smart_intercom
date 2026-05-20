from enum import StrEnum, auto


class VisitStatusEnum(StrEnum):
    IN_PROCESS = auto()
    ASKED_WANT_TO_ENTER = auto()
    WAITING_DECISION = auto()
    OVER = auto()


class VisitFinishReasonEnum(StrEnum):
    EMPLOYEE_DECISION = auto()
    CANCELLED_BY_VISITOR = auto()
    BOT_ERROR = auto()
    TIMEOUT = auto()


class VisitSortFieldsEnum(StrEnum):
    START_DATETIME = "startDatetime"
    FINISH_DATETIME = "finishDatetime"


class VisitEnums:
    def __init__(self):
        self.VisitStatus = VisitStatusEnum
        self.VisitSortFields = VisitSortFieldsEnum
        self.VisitFinishReason = VisitFinishReasonEnum
