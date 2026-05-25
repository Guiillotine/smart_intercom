from src.common.constants import TokenEnums
from src.modules.users.constants import UserEnums


class UserUCEnums:
    pass


class AuthUCEnums:
    def __init__(
        self,
        token_enums: TokenEnums,
        user_common_enums: UserEnums,
    ):
        self.User = user_common_enums
        self.Token = token_enums
