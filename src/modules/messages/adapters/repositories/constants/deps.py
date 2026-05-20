from src.modules.messages.adapters.repositories.constants import (
    MessageRepoConsts,
    MessageRepoEnums,
)


def get_message_repo_enums() -> MessageRepoEnums:
    return MessageRepoEnums()


def get_message_repo_consts() -> MessageRepoConsts:
    return MessageRepoConsts()
