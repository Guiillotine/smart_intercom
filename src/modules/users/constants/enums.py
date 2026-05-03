from enum import IntEnum

from src.common.constants import CommonEnums


class RoleEnum(IntEnum):
    USER = 1
    ADMIN = 2
    SUPERUSER = 3


class UserEnums:
    """Container class for all user-related enumerations.

    Provides centralized access to user enums through a single instance.
    """

    def __init__(self, common_enums: CommonEnums):
        """
        Initialize the enum container with all user-related enumerations.
        """
        self.Role = RoleEnum
        self.Common = common_enums
