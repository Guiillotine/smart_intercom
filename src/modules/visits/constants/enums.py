from enum import StrEnum, auto


class VisitStatusEnum(StrEnum):
    ACTIVE = auto()
    WAITING_DECISION = auto()
    OVER = auto()


class VisitEnums:
    def __init__(self):
        self.VisitStatus = VisitStatusEnum
