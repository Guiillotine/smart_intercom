from src.modules.users.constants import UserEnums


class PostgresInitEnums:
    def __init__(
        self,
        user_common_enums: UserEnums,
    ):
        self.User = user_common_enums
