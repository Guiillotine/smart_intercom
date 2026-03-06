from enum import StrEnum


class SchemaNamesEnum(StrEnum):
    USERS = "USERS"
    VISITS = "VISITS"
    PERSONS = "PERSONS"
    MESSAGES = "MESSAGES"


class PostgresEnums:
    def __init__(self):
        self.SchemaNames = SchemaNamesEnum
