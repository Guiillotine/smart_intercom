from enum import StrEnum, auto


class SchemaNamesEnum(StrEnum):
    USERS = auto()
    VISITS = auto()
    PERSONS = auto()
    MESSAGES = auto()


class PostgresEnums:
    def __init__(self):
        self.SchemaNames = SchemaNamesEnum
