from enum import Enum


class CommonErrorsEnum(Enum):
    UNDEFINED = (0, 500, "Unknown error")
    UNPROCESSABLE_ENTITY = (2, 422, "Unprocessable entity")
    NOT_FOUND = (4, 404, "Entry not found")


class AuthErrorsEnum(Enum):
    BAD_REFRESH_TOKEN = (100, 401, "Invalid refresh token")
    BAD_ACCESS_TOKEN = (101, 401, "Invalid access token")
    INCORRECT_CREDENTIALS = (103, 401, "Incorrect login/password")


class ErrorCodesEnums:
    def __init__(self):
        self.Common = CommonErrorsEnum
        self.Auth = AuthErrorsEnum
