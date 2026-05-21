from typing import Annotated

from fastapi.params import Depends

from src.common.constants import CommonEnums
from src.common.constants.deps import get_common_enums
from src.common.schemas.constants import SchemaEnums
from src.common.schemas.constants.deps import get_schema_enums
from src.modules.messages.services.constants import MessageSrvConsts, MessageSrvEnums


def get_message_srv_enums(
    common_enums: Annotated[CommonEnums, Depends(get_common_enums)],
    schema_enums: Annotated[SchemaEnums, Depends(get_schema_enums)],
) -> MessageSrvEnums:
    return MessageSrvEnums(
        common_enums=common_enums,
        schema_enums=schema_enums,
    )


def get_message_srv_consts() -> MessageSrvConsts:
    return MessageSrvConsts()
