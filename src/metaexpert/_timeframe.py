# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from enum import Enum
from typing import Self, TypedDict


class TimeframeDict(TypedDict):
    name: str
    sec: int
    min: int
    hour: int | None
    delta: timedelta | None


class Timeframe(Enum):
    """Timeframe enumeration for supported timeframes."""

    M1 = {
        "name": "1m",
        "sec": 60,
        "min": 1,
        "hour": None,
        "delta": timedelta(minutes=1)
    }
    M3 = {
        "name": "3m",
        "sec": 180,
        "min": 3,
        "hour": None,
        "delta": timedelta(minutes=3)
    }
    M5 = {
        "name": "5m",
        "sec": 300,
        "min": 5,
        "hour": None,
        "delta": timedelta(minutes=5)
    }
    M15 = {
        "name": "15m",
        "sec": 900,
        "min": 15,
        "hour": None,
        "delta": timedelta(minutes=15)
    }
    M30 = {
        "name": "30m",
        "sec": 1800,
        "min": 30,
        "hour": None,
        "delta": timedelta(minutes=30)
    }
    H1 = {
        "name": "1h",
        "sec": 3600,
        "min": 60,
        "hour": 1,
        "delta": timedelta(hours=1)
    }
    H2 = {
        "name": "2h",
        "sec": 7200,
        "min": 120,
        "hour": 2,
        "delta": timedelta(hours=2)
    }
    H4 = {
        "name": "4h",
        "sec": 14400,
        "min": 240,
        "hour": 4,
        "delta": timedelta(hours=4)
    }
    H6 = {
        "name": "6h",
        "sec": 21600,
        "min": 360,
        "hour": 6,
        "delta": timedelta(hours=6)
    }
    H8 = {
        "name": "8h",
        "sec": 28800,
        "min": 480,
        "hour": 8,
        "delta": timedelta(hours=8)
    }
    H12 = {
        "name": "12h",
        "sec": 43200,
        "min": 720,
        "hour": 12,
        "delta": timedelta(hours=12)
    }
    D1 = {
        "name": "1d",
        "sec": 86400,
        "min": 1440,
        "hour": 24,
        "delta": timedelta(days=1)
    }
    D3 = {
        "name": "3d",
        "sec": 259200,
        "min": 4320,
        "hour": 72,
        "delta": timedelta(days=3)
    }
    W1 = {
        "name": "1w",
        "sec": 604800,
        "min": 10080,
        "hour": 168,
        "delta": timedelta(weeks=1)
    }

    @classmethod
    def get_period_from(cls, name: str | Self) -> Self | None:
        """Get the period type from a string."""
        if isinstance(name, Timeframe):
            return name

        for item in cls:
            if item.value.get("name") == name.lower():
                return item

        return None

    @classmethod
    def get_next_candle_time(cls) -> datetime:
        """Calculate the timestamp of the next candle based on the timeframe.

        Returns:
            datetime: Timestamp of the next candle
        """
        now = datetime.now()
        next_time = now

        match cls.value.get("name")[-1]:
            case "m":
                # For minute timeframes
                minutes = cls.value.get("min")
                next_minute = ((now.minute // minutes) + 1) * minutes
                next_time = now.replace(minute=next_minute % 60, second=0, microsecond=0)

                if next_minute >= 60:
                    next_time += timedelta(hours=next_minute // 60)
            case "h":
                # For hour timeframes
                hours = cls.value.get("hour")
                next_hour = ((now.hour // hours) + 1) * hours
                next_time = now.replace(hour=next_hour % 24, minute=0, second=0, microsecond=0)

                if next_hour >= 24:
                    next_time += timedelta(days=next_hour // 24)
            case "d":
                # For day timeframes
                next_time = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
            case "w":
                pass
            case _:
                raise ValueError(f"Unsupported timeframe: {cls.value.get("name")}")

        return next_time

# if __name__ == "__main__":
#     for i in Timeframe:
#         print(i.name, i.value.get("name"), i.value.get("sec"))
#
#     print(Timeframe()._get_period_from("1m"))
