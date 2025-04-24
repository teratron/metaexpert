# -*- coding: utf-8 -*-

from enum import Enum

import metaexpert


class Period(Enum):
    M1 = {
        "name": "1m",
        "sec": 60,
        "min": 1
    }
    M3 = {
        "name": "3m",
        "sec": 180,
        "min": 3
    }
    M5 = {
        "name": "5m",
        "sec": 300,
        "min": 5
    }
    M15 = {
        "name": "15m",
        "sec": 900,
        "min": 15
    }
    M30 = {
        "name": "30m",
        "sec": 1800,
        "min": 30
    }
    H1 = {
        "name": "1h",
        "sec": 3600,
        "min": 60
    }
    H2 = {
        "name": "2h",
        "sec": 7200,
        "min": 120
    }
    H4 = {
        "name": "4h",
        "sec": 14400,
        "min": 240
    }
    H6 = {
        "name": "6h",
        "sec": 21600,
        "min": 360
    }
    H8 = {
        "name": "8h",
        "sec": 28800,
        "min": 480
    }
    H12 = {
        "name": "12h",
        "sec": 43200,
        "min": 720
    }
    D1 = {
        "name": "1d",
        "sec": 86400,
        "min": 1440
    }
    D3 = {
        "name": "3d",
        "sec": 259200,
        "min": 4320
    }
    W1 = {
        "name": "1w",
        "sec": 604800,
        "min": 10080
    }

    class Timeframe:
        """Timeframe class to represent different timeframes."""

        def __init__(self) -> None:
            """Initialize the Timeframe class."""
            pass

        @staticmethod
        def __get_period_from(name: str) -> Period | None:
            for period in Period:
                if period.value["name"] == name:
                    return period
            return None

if __name__ == "__main__":

    for item in Period:
        print(item.name, item.value["name"], item.value["sec"])

    print(Timeframe().__get_period_from("1m"))
