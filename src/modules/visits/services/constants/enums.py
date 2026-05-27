from src.common.constants import CommonEnums, SrvReqCommonEnums


class VisitSrvEnums:
    def __init__(
        self,
        common_enums: CommonEnums,
        srv_req_common_enums: SrvReqCommonEnums,
    ):
        self.Common = common_enums
        self.SrvReqCommon = srv_req_common_enums
