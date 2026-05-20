from enum import StrEnum

from src.common.constants import CommonEnums


class UserCtrlPathEnum(StrEnum):
    """Enumeration of controller route paths for user endpoints.

    Defines all API route paths used by user controllers.
    """
    me = "/me"
    get_user = ""


class AuthCtrlPathEnum(StrEnum):
    """Enumeration of controller route paths for auth-related endpoints.

    Defines all API route paths used by auth controllers.
    """
    login = "/login"
    logout = "/logout"
    refresh_token = "/refresh_token"
    register = "/register"


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
        self.AuthCtrlPath = AuthCtrlPathEnum
        self.UserCtrlPath = UserCtrlPathEnum
