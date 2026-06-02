from src.common.constants import SrvReqCommonEnums
from src.modules.visits.constants import VisitEnums


class VisitUCEnums:
    def __init__(
        self,
        visit_common_enums: VisitEnums,
        srv_req_common_enums: SrvReqCommonEnums,
    ):
        self.Visit = visit_common_enums
        self.SrvReqCommon = srv_req_common_enums
