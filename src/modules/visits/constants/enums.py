from enum import StrEnum, auto


class VisitStatusEnum(StrEnum):
    ACTIVE = auto()
    WAITING_DECISION = auto()
    OVER = auto()


class VisitFinishReasonEnum(StrEnum):
    EMPLOYEE_DECISION = auto()
    CANCELLED_BY_VISITOR = auto()
    BOT_ERROR = auto()
    TIMEOUT = auto() # TODO


class VisitEnums:
    def __init__(self):
        self.VisitStatus = VisitStatusEnum
        self.VisitFinishReason = VisitFinishReasonEnum
