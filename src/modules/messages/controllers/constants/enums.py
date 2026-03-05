from enum import StrEnum

from src.common.constants import CommonEnums


class MessageCtrlPathEnum(StrEnum):
    """Enumeration of controller route paths for messages endpoints.

    Defines all API route paths used by messages controllers.
    """
    pass


class MessageCtrlEnums:
    """Container class for messages controller enumerations and constants.

    Provides centralized access to controller-related enums.
    """

    def __init__(
        self,
        common_enums: CommonEnums,
    ):
        """Initialize messages controller enums container."""

        self.Common = common_enums
        self.MessageCtrlPath = MessageCtrlPathEnum
