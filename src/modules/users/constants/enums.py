from enum import IntEnum, StrEnum, auto

from src.common.constants import CommonEnums


class RoleEnum(IntEnum):
    USER = 10
    ADMIN = 20
    SUPERUSER = 30


class LogoutType(StrEnum):
    """
    Enumeration of user logout types.

    current - logout current device.
    everywhere - logout all user devices.
    """

    current = auto()
    everywhere = auto()


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
        self.LogoutType = LogoutType
