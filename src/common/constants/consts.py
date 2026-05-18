from src.common.constants.enums import LanguageEnum


class LanguageConsts:
    DEFAULT_LANG: LanguageEnum = LanguageEnum.RU


class CommonConsts:
    def __init__(self):
        self.DefaultLanguage = LanguageConsts().DEFAULT_LANG
