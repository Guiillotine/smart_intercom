from enum import auto, StrEnum


class AuthPayloadFieldsEnum(StrEnum):
    """
    Enum representing the standard fields used in authentication token payloads.
    """

    SUB = "sub"
    STATUS = "status"
    EXP = "exp"
    JTI = "jti"
    PAIR_ID = "pair_id"


class TokenPayloadFieldsEnum(StrEnum):
    EXP = "exp"
    JTI = "jti"
    PAIR_ID = "pair_id"
    DEVICE = "device"
    IAT = "iat"


class TokenType(StrEnum):
    """
    Enumeration of token types used in authentication.

    Defines string constants for token categories such as access and refresh,
    facilitating consistent token handling throughout the system.
    """

    ACCESS = auto()
    REFRESH = auto()


class TokenEnums:
    def __init__(self):
        self.AuthPayloadFields = AuthPayloadFieldsEnum
        self.TokenPayloadFields = TokenPayloadFieldsEnum
        self.TokenType = TokenType
