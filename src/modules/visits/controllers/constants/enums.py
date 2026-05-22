from enum import StrEnum

from src.common.constants import CommonEnums


class VisitCtrlPathEnum(StrEnum):
    """Enumeration of controller route paths for visits endpoints.

    Defines all API route paths used by visits controllers.
    """
    get_visit = "/{sid}"
    get_all_visits = ""
    get_waiting_decision_visits = "/waiting_decision"
    make_door_open_decision = "/{sid}/decision"


class VisitCtrlEnums:
    """Container class for visits controller enumerations and constants.

    Provides centralized access to controller-related enums.
    """

    def __init__(
        self,
        common_enums: CommonEnums,
    ):
        """Initialize visits controller enums container."""

        self.Common = common_enums
        self.VisitCtrlPath = VisitCtrlPathEnum
