from typing import Annotated

from fastapi import Depends

from src.common.constants import CommonEnums, SrvReqCommonEnums
from src.common.constants.deps import get_common_enums, get_srv_req_common_enums
from src.modules.visits.services.constants import VisitSrvConsts, VisitSrvEnums


def get_visit_srv_enums(
    common_enums: Annotated[CommonEnums, Depends(get_common_enums)],
    srv_req_common_enums: Annotated[
        SrvReqCommonEnums, Depends(get_srv_req_common_enums)
    ],
) -> VisitSrvEnums:
    return VisitSrvEnums(
        common_enums=common_enums,
        srv_req_common_enums=srv_req_common_enums,
    )


def get_visit_srv_consts() -> VisitSrvConsts:
    return VisitSrvConsts()
