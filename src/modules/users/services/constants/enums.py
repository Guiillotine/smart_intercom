from src.common.constants import TokenEnums


class UserSrvEnums:
    def __init__(
        self,
    ):
        pass


class AuthSrvEnums:
    def __init__(
        self,
        token_enums: TokenEnums,
    ):
        self.TokenEnums = token_enums
