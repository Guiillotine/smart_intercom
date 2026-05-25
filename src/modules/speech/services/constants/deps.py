from typing import Annotated

from fastapi import Depends

from src.common.constants.consts import CommonConsts
from src.common.constants.deps import get_common_consts
from src.modules.speech.services.constants import ASRServiceEnums, ASRServiceConsts, \
    TTSServiceEnums, TTSServiceConsts


def get_asr_service_enums() -> ASRServiceEnums:
    return ASRServiceEnums()


def get_tts_service_enums() -> TTSServiceEnums:
    return TTSServiceEnums()


def get_asr_service_consts(
    common_consts: Annotated[CommonConsts, Depends(get_common_consts)],
) -> ASRServiceConsts:
    return ASRServiceConsts(common_consts=common_consts)


def get_tts_service_consts() -> TTSServiceConsts:
    return TTSServiceConsts()
