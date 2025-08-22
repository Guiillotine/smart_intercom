from datetime import datetime

from pytz import UTC


class CustomDatetime:
    @staticmethod
    def get_datetime() -> datetime:
        return datetime.now().replace(microsecond=0)

    @staticmethod
    def get_utc_datetime() -> datetime:
        return datetime.now(UTC).replace(microsecond=0)
