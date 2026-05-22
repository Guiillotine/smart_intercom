from typing import Annotated

from fastapi import Depends

from src.common.constants import CommonEnums
from src.common.constants.deps import get_common_enums
from src.modules.dialogues.constants import DialogueEnums, DialogueConsts


def get_dialogue_enums(
    common_enums: Annotated[CommonEnums, Depends(get_common_enums)],
) -> DialogueEnums:
    return DialogueEnums(
        common_enums=common_enums,
    )


def get_dialogue_consts() -> DialogueConsts:
    return DialogueConsts()
