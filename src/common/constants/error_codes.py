from enum import Enum


class CommonErrorsEnum(Enum):
    # 400
    NOT_FOUND = (4, 404, "Entry not found")
    UNPROCESSABLE_ENTITY = (2, 422, "Unprocessable entity")
    # 500
    UNDEFINED = (0, 500, "Unknown error")


class AuthErrorsEnum(Enum):
    # 400
    BAD_REFRESH_TOKEN = (100, 401, "Invalid refresh token")
    BAD_ACCESS_TOKEN = (101, 401, "Invalid access token")
    INCORRECT_CREDENTIALS = (103, 401, "Incorrect login/password")


class DialogErrorsEnum(Enum):
    # 400
    BAD_REQUEST = ("bad_request", 400, "Bad request to LLM provider")
    INVALID_LLM_RESPONSE = ("invalid_llm_response", 400, "Invalid LLM response format")
    RATE_LIMIT_ERROR = ("rate_limit_error",  429, "Too many requests to LLM")
    TIMEOUT = ("llm_response_timeout_error", 408, "LLM response timeout has expired.")
    # 500
    OPENAI = ("openai_error", 500, "Error on openai side")


class IntercomErrorsEnum(Enum):
    # 400
    DIALOG_IS_OVER = ("dialog_is_over", 400, "Dialog is over")


class ErrorCodesEnums:
    def __init__(self):
        self.Common = CommonErrorsEnum
        self.Auth = AuthErrorsEnum
        self.Dialog = DialogErrorsEnum
        self.Intercom = IntercomErrorsEnum
