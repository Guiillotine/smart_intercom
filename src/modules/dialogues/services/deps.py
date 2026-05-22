import logging
from typing import Annotated

from fastapi import Depends
from openai import OpenAI

from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes_enums
from src.common.logger.deps import get_dialogue_logger
from src.config.settings import Settings
from src.config.settings.deps import get_settings
from src.modules.dialogues.adapters.openai.deps import get_openai_client
from src.modules.dialogues.constants import DialogueConsts, DialogueEnums
from src.modules.dialogues.constants.deps import get_dialogue_enums, get_dialogue_consts
from src.modules.dialogues.interfaces import IDialogueSrv
from src.modules.dialogues.services.dialogue import DialogueSrv


def get_dialogue_service(
    logger: Annotated[logging.Logger, Depends(get_dialogue_logger)],
    enums: Annotated[DialogueEnums, Depends(get_dialogue_enums)],
    consts: Annotated[DialogueConsts, Depends(get_dialogue_consts)],
    errors: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    settings: Annotated[Settings, Depends(get_settings)],
    client: Annotated[OpenAI, Depends(get_openai_client)],
) -> IDialogueSrv:
    return DialogueSrv(
        logger=logger,
        enums=enums,
        consts=consts,
        errors=errors,
        settings=settings,
        client=client,
    )
