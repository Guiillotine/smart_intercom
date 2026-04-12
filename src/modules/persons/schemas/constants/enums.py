from enum import Enum


class PersonSortFieldEnum(str, Enum):
    full_name = "fullName"
    created_at = "createdAt"


class PersonSchemaEnums:
    """
    Container for enums used in pydantic schemas.

    Provides centralized access to enumerations required for query construction.
    """

    def __init__(self):
        """Initialize repository enum container with core enumerations."""
        self.PersonSortField = PersonSortFieldEnum
