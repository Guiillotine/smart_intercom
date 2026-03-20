from enum import IntEnum


class PersonTypeEnum(IntEnum):
    """
    1: EMPLOYEE
    2: VISITOR
    """
    EMPLOYEE = 1
    VISITOR = 2


class PersonEnums:
    def __init__(self):
        self.PersonType = PersonTypeEnum
