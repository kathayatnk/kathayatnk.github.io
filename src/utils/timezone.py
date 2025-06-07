
import zoneinfo

from datetime import datetime
from datetime import timezone as datetime_timezone

from src.core.settings import settings


class TimeZone:
    def __init__(self, tz: str = settings.DATETIME_TIMEZONE) -> None:
        self.tz_info = zoneinfo.ZoneInfo(tz)

    def now(self) -> datetime:
        return datetime.now(self.tz_info)

    def f_datetime(self, dt: datetime) -> datetime:
        return dt.astimezone(self.tz_info)

    def f_str(self, date_str: str, format_str: str = settings.DATETIME_FORMAT) -> datetime:
        return datetime.strptime(date_str, format_str).replace(tzinfo=self.tz_info)

    @staticmethod
    def t_str(dt: datetime, format_str: str = settings.DATETIME_FORMAT) -> str:
        return dt.strftime(format_str)

    @staticmethod
    def f_utc(dt: datetime) -> datetime:
        return dt.astimezone(datetime_timezone.utc)


timezone: TimeZone = TimeZone()
