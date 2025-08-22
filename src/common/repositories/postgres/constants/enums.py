from enum import StrEnum


class SchemaNamesEnum(StrEnum):
    USERS = "USERS"
    VISITS = "VISITS"


class PostgresEnums:
    def __init__(self):
        self.SchemaNames = SchemaNamesEnum
