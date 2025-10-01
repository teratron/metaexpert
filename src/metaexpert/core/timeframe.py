from datetime import datetime, timedelta
from enum import Enum
from logging import Logger
from typing import Self

from metaexpert.config import APP_NAME, DEFAULT_TIMEFRAME
from metaexpert.logger import get_logger

logger: Logger = get_logger(APP_NAME)


class Timeframe(Enum):
    """Timeframe enumeration for supported timeframes."""

    M1 = {
        "name": "1m",
        "sec": 60,
        "min": 1,
        "hour": None,
        "delta": timedelta(minutes=1),
    }
    M3 = {
        "name": "3m",
        "sec": 180,
        "min": 3,
        "hour": None,
        "delta": timedelta(minutes=3),
    }
    M5 = {
        "name": "5m",
        "sec": 300,
        "min": 5,
        "hour": None,
        "delta": timedelta(minutes=5),
    }
    M15 = {
        "name": "15m",
        "sec": 900,
        "min": 15,
        "hour": None,
        "delta": timedelta(minutes=15),
    }
    M30 = {
        "name": "30m",
        "sec": 1800,
        "min": 30,
        "hour": None,
        "delta": timedelta(minutes=30),
    }
    H1 = {
        "name": "1h",
        "sec": 3600,
        "min": 60,
        "hour": 1,
        "delta": timedelta(hours=1),
    }
    H2 = {
        "name": "2h",
        "sec": 7200,
        "min": 120,  # 2 hours * 60 minutes
        "hour": 2,
        "delta": timedelta(hours=2),
    }
    H4 = {
        "name": "4h",
        "sec": 14400,
        "min": 240,  # 4 hours * 60 minutes
        "hour": 4,
        "delta": timedelta(hours=4),
    }
    H6 = {
        "name": "6h",
        "sec": 21600,
        "min": 360,  # 6 hours * 60 minutes
        "hour": 6,
        "delta": timedelta(hours=6),
    }
    H8 = {
        "name": "8h",
        "sec": 28800,
        "min": 480,  # 8 hours * 60 minutes
        "hour": 8,
        "delta": timedelta(hours=8),
    }
    H12 = {
        "name": "12h",
        "sec": 43200,
        "min": 720,  # 12 hours * 60 minutes
        "hour": 12,
        "delta": timedelta(hours=12),
    }
    D1 = {
        "name": "1d",
        "sec": 86400,
        "min": 1440,  # 1 day * 24 hours * 60 minutes
        "hour": 24,
        "delta": timedelta(days=1),
    }
    D3 = {
        "name": "3d",
        "sec": 259200,
        "min": 4320,  # 3 days * 24 hours * 60 minutes
        "hour": 72,
        "delta": timedelta(days=3),
    }
    W1 = {
        "name": "1w",
        "sec": 604800,
        "min": 10080,  # 7 days * 24 hours * 60 minutes
        "hour": 168,
        "delta": timedelta(weeks=1),
    }

    def get_name(self) -> str:
        """Get the string representation of the timeframe name."""
        name = self.value["name"]
        if isinstance(name, str):
            return name
        raise TypeError(f"Timeframe name must be a string, got {type(name).__name__}")

    def get_seconds(self) -> int:
        """Get the number of seconds in the timeframe."""
        sec = self.value["sec"]
        if isinstance(sec, int):
            return sec
        raise TypeError(f"Timeframe seconds must be an integer, got {type(sec).__name__}")

    def get_minutes(self) -> int:
        """Get the number of minutes in the timeframe."""
        minute = self.value["min"]
        if isinstance(minute, int):
            return minute
        raise TypeError(f"Timeframe minutes must be an integer, got {type(minute).__name__}")

    def get_hours(self) -> int | None:
        """Get the number of hours in the timeframe."""
        hour = self.value["hour"]
        if hour is None:
            return None
        if isinstance(hour, int):
            return hour
        raise TypeError(f"Timeframe hours must be an integer, got {type(hour).__name__}")

    def get_delta(self) -> timedelta:
        """Get the timedelta object representing the timeframe."""
        delta = self.value["delta"]
        if isinstance(delta, timedelta):
            return delta
        raise TypeError(f"Timeframe delta must be a timedelta, got {type(delta).__name__}")

    @classmethod
    def get_timeframe_from(cls, name: str) -> Self:
        """Get the period type from a string."""
        normalized_name: str = name.lower().strip()
        if isinstance(name, str):
            for item in cls:
                if item.get_name() == normalized_name:
                    return item
        return cls.get_timeframe_from(DEFAULT_TIMEFRAME)

    @staticmethod
    def _get_next_weekly_candle_time(now: datetime) -> datetime:
        """Calculates the start of the next weekly candle (Monday)."""
        # weekday() is 0 for Monday, 6 for Sunday
        days_to_add = 7 - now.weekday()
        next_monday = now + timedelta(days=days_to_add)
        return next_monday.replace(hour=0, minute=0, second=0, microsecond=0)

    def _get_next_regular_candle_time(self, now: datetime) -> datetime:
        """Calculates the start of the next candle for m, h, d timeframes."""
        timeframe_delta = self.get_delta()
        if not isinstance(timeframe_delta, timedelta):
            logger.error("Invalid timedelta value for timeframe: %s", self.get_name())
            raise ValueError(f"Invalid timedelta value for timeframe: {self.get_name()}")

        timeframe_seconds = timeframe_delta.total_seconds()
        if timeframe_seconds <= 0:
            logger.error("Timeframe duration must be positive: %s", self.get_name())
            raise ValueError(f"Timeframe duration must be positive: {self.get_name()}")

        now_timestamp = now.timestamp()
        # Floor division to find the start of the current candle interval
        current_candle_start_ts = (now_timestamp // timeframe_seconds) * timeframe_seconds
        # Add one interval to get the start of the next candle
        next_candle_start_ts = current_candle_start_ts + timeframe_seconds
        return datetime.fromtimestamp(next_candle_start_ts)

    def get_next_candle_time(self) -> datetime:
        """Calculate the timestamp of the next candle based on the timeframe.

        Returns:
            datetime: Timestamp of the next candle
        """
        now = datetime.now()
        name = self.get_name()
        if name[-1] == "w":
            return self._get_next_weekly_candle_time(now)
        return self._get_next_regular_candle_time(now)
