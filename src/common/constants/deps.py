from src.common.constants import CommonEnums, ErrorCodesEnums, TokenEnums, \
    SrvReqCommonEnums
from src.common.constants.consts import CommonConsts


def get_common_enums():
    """Dependency provider for common enums."""
    return CommonEnums()


def get_token_enums():
    """Dependency provider for token enums."""
    return TokenEnums()


def get_error_codes_enums():
    """Dependency provider for error code enums."""
    return ErrorCodesEnums()


def get_common_consts():
    """Dependency provider for common consts."""
    return CommonConsts()


def get_srv_req_common_enums() -> SrvReqCommonEnums:
    """Dependency provider for output service requirement enums."""
    return SrvReqCommonEnums()
