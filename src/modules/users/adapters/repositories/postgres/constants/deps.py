from src.modules.users.adapters.repositories.postgres.constants import (
    UserRepoConsts,
    UserRepoEnums,
)


def get_user_repo_enums() -> UserRepoEnums:
    return UserRepoEnums()


def get_user_repo_consts() -> UserRepoConsts:
    return UserRepoConsts()
