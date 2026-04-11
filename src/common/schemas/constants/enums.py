from enum import Enum


class SortDirectionEnum(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class SchemaEnums:
    """
    Container for enums used in pydantic schemas.

    Provides centralized access to enumerations required for query construction.
    """

    def __init__(self):
        self.SortDirection = SortDirectionEnum
