from enum import Enum


class PersonSortFieldEnum(str, Enum):
    first_name = "firstName"
    last_name = "lastName"
    created_at = "createdAt"


class PersonSchemaEnums:
    """
    Container for enums used in pydantic schemas.

    Provides centralized access to enumerations required for query construction.
    """

    def __init__(self):
        """Initialize repository enum container with core enumerations."""
        self.PersonSortField = PersonSortFieldEnum
