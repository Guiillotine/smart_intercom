from typing import Annotated

from fastapi import Depends

from src.common.constants import CommonEnums
from src.common.constants.deps import get_common_enums
from src.modules.faces.services.constants.enums import FaceAnalyzerSrvEnums


def get_face_analyzer_service_enums(
    common_enums: Annotated[CommonEnums, Depends(get_common_enums)],
) -> FaceAnalyzerSrvEnums:
    """
    Dependency provider for FaceAnalyserSrvEnums instance.

    :return: Initialized FaceAnalyser service enums instance
    """
    return FaceAnalyzerSrvEnums(common_enums=common_enums)
