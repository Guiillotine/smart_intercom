from enum import StrEnum

from src.common.constants import CommonEnums


class UserCtrlPathEnum(StrEnum):
    """Enumeration of controller route paths for users endpoints.

    Defines all API route paths used by users controllers.
    """
    pass


class UserCtrlEnums:
    """Container class for users controller enumerations and constants.

    Provides centralized access to controller-related enums.
    """

    def __init__(
        self,
        common_enums: CommonEnums,
    ):
        """Initialize users controller enums container."""

        self.Common = common_enums
        self.UserCtrlPath = UserCtrlPathEnum
