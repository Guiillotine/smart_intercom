from enum import StrEnum

from src.common.constants import CommonEnums


class EmployeeCtrlPathEnum(StrEnum):
    """Enumeration of controller route paths for employee endpoints.

    Defines all API route paths used by employee controllers.
    """
    pass


class EmployeeCtrlEnums:
    """Container class for employee controller enumerations and constants.

    Provides centralized access to controller-related enums.
    """

    def __init__(
        self,
        common_enums: CommonEnums,
    ):
        """Initialize employee controller enums container."""

        self.Common = common_enums
        self.EmployeeCtrlPath = EmployeeCtrlPathEnum
