from enum import Enum


class CommonErrorsEnum(Enum):
    UNDEFINED = (0, 500, "Unknown error")
    NOT_FOUND = (1, 404, "Entry not found")
    NOT_ALLOWED = (2, 405, "Access Denied")


class AuthErrorsEnum(Enum):
    BAD_REFRESH_TOKEN = (100, 401, "Invalid refresh token")
    BAD_ACCESS_TOKEN = (101, 401, "Invalid access token")
    INCORRECT_CREDENTIALS = (103, 401, "Incorrect login/password")


class ErrorCodesEnums:
    def __init__(self):
        self.CommonErrors = CommonErrorsEnum
        self.AuthErrors = AuthErrorsEnum
