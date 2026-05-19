from enum import Enum


class CommonErrorsEnum(Enum):
    # 400
    NOT_FOUND = ("not_found", 404, "Entry not found")
    # --- 422 Unprocessable Entity ---
    UNPROCESSABLE_ENTITY = ("unprocessable_entity", 422, "Unprocessable entity")
    NUMBER_OUT_OF_BOUNDS = (
        "number_out_of_bounds",
        422,
        "Numeric field is out of bounds",
    )
    # 500
    UNDEFINED = ("undefined", 500, "Unknown error")


class AuthErrorsEnum(Enum):
    # 400
    INVALID_REFRESH_TOKEN = ("invalid_refresh_token", 401, "Invalid refresh token")
    INVALID_ACCESS_TOKEN = ("invalid_access_token", 401, "Invalid access token")
    INCORRECT_CREDENTIALS = ("incorrect_credentials", 401, "Incorrect login/password")


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


class PersonErrorsEnum(Enum):
    # 404
    PERSON_NOT_FOUND = ("person_not_found", 404, "Person not found")


class ErrorCodesEnums:
    def __init__(self):
        self.Auth = AuthErrorsEnum
        self.Common = CommonErrorsEnum
        self.Dialog = DialogErrorsEnum
        self.Person = PersonErrorsEnum
        self.Intercom = IntercomErrorsEnum
