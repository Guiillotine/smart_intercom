from typing import Annotated

from fastapi import Depends

from src.common.constants import SrvReqCommonEnums
from src.common.constants.deps import get_srv_req_common_enums
from src.modules.visits.usecases.constants import VisitUCConsts, VisitUCEnums


def get_visit_uc_enums(
    srv_req_common_enums: Annotated[
        SrvReqCommonEnums, Depends(get_srv_req_common_enums)
    ]
) -> VisitUCEnums:
    return VisitUCEnums(srv_req_common_enums=srv_req_common_enums)


def get_visit_uc_consts() -> VisitUCConsts:
    return VisitUCConsts()
