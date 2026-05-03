import logging
from typing import Annotated

from fastapi import Depends

from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes_enums
from src.common.logger.deps import get_face_logger
from src.modules.faces.interfaces import IFaceAnalyzerSrv
from src.modules.faces.services import FaceAnalyzerSrv
from src.modules.faces.services.constants.deps import get_face_analyzer_service_enums
from src.modules.faces.services.constants.enums import FaceAnalyzerSrvEnums


def get_face_analyzer_service(
    logger: Annotated[logging.Logger, Depends(get_face_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    enums: Annotated[FaceAnalyzerSrvEnums, Depends(get_face_analyzer_service_enums)],
) -> IFaceAnalyzerSrv:
    """
    Dependency provider for FaceAnalyzerSrv instance.

    :return: Initialized FaceAnalyzer service instance
    """
    return FaceAnalyzerSrv(
        logger=logger,
        enums=enums,
        errors=error_codes,
    )
