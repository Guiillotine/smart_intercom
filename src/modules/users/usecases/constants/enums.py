from src.common.constants import TokenEnums


class UserUCEnums:
    pass


class AuthUCEnums:
    def __init__(
        self,
        token_enums: TokenEnums,
    ):
        self.Token = token_enums
