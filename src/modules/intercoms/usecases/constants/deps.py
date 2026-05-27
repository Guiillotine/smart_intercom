from typing import Annotated

from fastapi import Depends

from src.common.constants import CommonEnums, SrvReqCommonEnums
from src.common.constants.consts import CommonConsts
from src.common.constants.deps import get_common_enums, get_common_consts, \
    get_srv_req_common_enums
from src.modules.dialogues.constants import DialogueEnums
from src.modules.dialogues.constants.deps import get_dialogue_enums
from src.modules.intercoms.usecases.constants import IntercomUCConsts, IntercomUCEnums
from src.modules.messages.constants import MessageEnums
from src.modules.messages.constants.deps import get_message_enums
from src.modules.visits.constants import VisitEnums
from src.modules.visits.constants.deps import get_visit_enums


def get_intercom_usecase_enums(
    common_enums: Annotated[CommonEnums, Depends(get_common_enums)],
    visit_common_enums: Annotated[VisitEnums, Depends(get_visit_enums)],
    message_common_enums: Annotated[MessageEnums, Depends(get_message_enums)],
    dialogue_common_enums: Annotated[DialogueEnums, Depends(get_dialogue_enums)],
    srv_req_common_enums: Annotated[
        SrvReqCommonEnums, Depends(get_srv_req_common_enums)
    ],
) -> IntercomUCEnums:
    return IntercomUCEnums(
        common_enums=common_enums,
        visit_common_enums=visit_common_enums,
        message_common_enums=message_common_enums,
        srv_req_common_enums=srv_req_common_enums,
        dialogue_common_enums=dialogue_common_enums,
    )


def get_intercom_usecase_consts(
    common_consts: Annotated[CommonConsts, Depends(get_common_consts)],
) -> IntercomUCConsts:
    return IntercomUCConsts(common_consts=common_consts)
