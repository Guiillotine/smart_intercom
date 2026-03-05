from enum import StrEnum

from src.common.constants import CommonEnums


class IntercomCtrlPathEnum(StrEnum):
    """Enumeration of controller route paths for intercoms endpoints.

    Defines all API route paths used by intercoms controllers.
    """
    pass


class IntercomCtrlEnums:
    """Container class for intercoms controller enumerations and constants.

    Provides centralized access to controller-related enums.
    """

    def __init__(
        self,
        common_enums: CommonEnums,
    ):
        """Initialize intercoms controller enums container."""

        self.Common = common_enums
        self.IntercomCtrlPath = IntercomCtrlPathEnum
