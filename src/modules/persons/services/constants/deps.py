from typing import Annotated

from fastapi import Depends

from src.common.constants import CommonEnums, SrvReqCommonEnums
from src.common.constants.deps import get_common_enums, get_srv_req_common_enums
from src.modules.persons.services.constants import PersonSrvEnums


def get_person_srv_enums(
    common_enums: Annotated[CommonEnums, Depends(get_common_enums)],
    srv_req_common_enums: Annotated[
        SrvReqCommonEnums, Depends(get_srv_req_common_enums)
    ],
) -> PersonSrvEnums:
    return PersonSrvEnums(
        common_enums=common_enums,
        srv_req_common_enums=srv_req_common_enums,
    )
