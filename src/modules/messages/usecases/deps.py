from typing import Annotated

from fastapi import Depends

from src.modules.messages.interfaces import IMessageSrv, IMessageUC
from src.modules.messages.services.deps import get_message_service
from src.modules.messages.usecases.constants import MessageUCConsts, MessageUCEnums
from src.modules.messages.usecases.constants.deps import (
    get_message_uc_consts,
    get_message_uc_enums,
)
from src.modules.messages.usecases.message import MessageUC


async def get_message_usecase(
    enums: Annotated[MessageUCEnums, Depends(get_message_uc_enums)],
    consts: Annotated[MessageUCConsts, Depends(get_message_uc_consts)],
    message_service: Annotated[IMessageSrv, Depends(get_message_service)],
) -> IMessageUC:
    return MessageUC(enums=enums, consts=consts, message_service=message_service)
