from enum import Enum


class CommonErrorsEnum(Enum):
    # 400
    NOT_FOUND = ("not_found", 404, "Entry not found")
    INCORRECT_SORT_FIELD = ("incorrect_sort_field", 400, "Incorrect sort field")
    # 403
    FORBIDDEN = ("forbidden", 403, "Forbidden")
    # 409
    NOT_UNIQUE = ("not_unique", 409, "Non-unique field(s) during creation")
    # 422
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
    INCORRECT_CREDENTIALS = (
        "incorrect_credentials",
        400,
        "Incorrect login or password",
    )
    INCORRECT_USER_ROLE = ("incorrect_user_role", 400, "Incorrect user role")
    # 401
    INVALID_REFRESH_TOKEN = ("invalid_refresh_token", 401, "Invalid refresh token")
    INVALID_ACCESS_TOKEN = ("invalid_access_token", 401, "Invalid access token")

class VisitErrorsEnum(Enum):
    # 400
    VISIT_NOT_IN_PROCESS = ("visit_not_in_process", 400, "Visit is not in process")
    # 404
    VISIT_NOT_FOUND = ("visit_not_found", 404, "Visit not found")


class DialogueErrorsEnum(Enum):
    # 400
    BAD_REQUEST = ("bad_request", 400, "Bad request to LLM provider")
    INVALID_LLM_RESPONSE = ("invalid_llm_response", 400, "Invalid LLM response format")
    RATE_LIMIT_ERROR = ("rate_limit_error",  429, "Too many requests to LLM")
    TIMEOUT = ("llm_response_timeout_error", 408, "LLM response timeout has expired.")
    # 500
    OPENAI = ("openai_error", 500, "Error on openai side")


class IntercomErrorsEnum(Enum):
    # 400
    DIALOGUE_IS_OVER = ("dialogue_is_over", 400, "Dialogue is over")


class PersonErrorsEnum(Enum):
    # 404
    PERSON_NOT_FOUND = ("person_not_found", 404, "Person not found")


class UserErrorsEnum(Enum):
    # 400
    INCORRECT_PHOTO = ("incorrect_person_photo", 400, "Person photo is incorrect")
    # 404
    USER_NOT_FOUND = ("user_not_found", 404, "User not found")


class TokenErrorsEnum(Enum):
    # 401
    INVALID_TOKEN = ("invalid_token", 400, "Invalid token")
    INVALID_ACCESS_TOKEN = ("invalid_access_token", 400, "Invalid access token")
    INVALID_REFRESH_TOKEN = ("invalid_refresh_token", 400, "Invalid refresh token")
    # 404
    TOKEN_NOT_FOUND = ("token_not_found", 404, "Token not found")


class ErrorCodesEnums:
    def __init__(self):
        self.Auth = AuthErrorsEnum
        self.User = UserErrorsEnum
        self.Token = TokenErrorsEnum
        self.Visit = VisitErrorsEnum
        self.Common = CommonErrorsEnum
        self.Person = PersonErrorsEnum
        self.Dialogue = DialogueErrorsEnum
        self.Intercom = IntercomErrorsEnum
