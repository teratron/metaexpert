# -*- coding: utf-8 -*-

from enum import Enum
from typing import Self, TypedDict


class TimeframeDict(TypedDict):
    name: str
    sec: int
    min: int
    hour: int | None


class Timeframe(Enum):
    """Timeframe enumeration for supported timeframes."""
    M1 = {
        "name": "1m",
        "sec": 60,
        "min": 1,
        "hour": None
    }
    M3 = {
        "name": "3m",
        "sec": 180,
        "min": 3,
        "hour": None
    }
    M5 = {
        "name": "5m",
        "sec": 300,
        "min": 5,
        "hour": None
    }
    M15 = {
        "name": "15m",
        "sec": 900,
        "min": 15,
        "hour": None
    }
    M30 = {
        "name": "30m",
        "sec": 1800,
        "min": 30,
        "hour": None
    }
    H1 = {
        "name": "1h",
        "sec": 3600,
        "min": 60,
        "hour": 1
    }
    H2 = {
        "name": "2h",
        "sec": 7200,
        "min": 120,
        "hour": 2
    }
    H4 = {
        "name": "4h",
        "sec": 14400,
        "min": 240,
        "hour": 4
    }
    H6 = {
        "name": "6h",
        "sec": 21600,
        "min": 360,
        "hour": 6
    }
    H8 = {
        "name": "8h",
        "sec": 28800,
        "min": 480,
        "hour": 8
    }
    H12 = {
        "name": "12h",
        "sec": 43200,
        "min": 720,
        "hour": 12
    }
    D1 = {
        "name": "1d",
        "sec": 86400,
        "min": 1440,
        "hour": 24
    }
    D3 = {
        "name": "3d",
        "sec": 259200,
        "min": 4320,
        "hour": 72
    }
    W1 = {
        "name": "1w",
        "sec": 604800,
        "min": 10080,
        "hour": 168
    }

    @classmethod
    def get_period_from(cls, name: str) -> Self | None:
        for item in cls:
            if item.value["name"] == name.lower():
                return item

        return None


if __name__ == "__main__":
    for i in Timeframe:
        print(i.name, i.value["name"], i.value["sec"])
#
#     print(Timeframe()._get_period_from("1m"))
