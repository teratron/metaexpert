# -*- coding: utf-8 -*-

from enum import Enum


class Timeframe(Enum):
    M1 = {
        "name": "1m",
        "sec": 60
    }
    M3 = {
        "name": "3m",
        "sec": 180
    }
    M5 = {
        "name": "5m",
        "sec": 300
    }
    M15 = {
        "name": "15m",
        "sec": 900
    }
    M30 = {
        "name": "30m",
        "sec": 1800
    }
    H1 = {
        "name": "1h",
        "sec": 3600
    }
    H2 = {
        "name": "2h",
        "sec": 7200
    }
    H4 = {
        "name": "4h",
        "sec": 14400
    }
    H6 = {
        "name": "6h",
        "sec": 21600
    }
    H8 = {
        "name": "8h",
        "sec": 28800
    }
    H12 = {
        "name": "12h",
        "sec": 43200
    }
    D1 = {
        "name": "1d",
        "sec": 86400
    }
    D3 = {
        "name": "3d",
        "sec": 259200
    }
    W1 = {
        "name": "1w",
        "sec": 604800
    }

    # def __init__(self) -> None:
    #     super().__init__()
    #     self.__list: list[str] = self.__get_list()
    #
    # def __get_list(self) -> list[str]:
    #     """Get the list of timeframe names."""
    #     return list(
    #         item for item in self.__dir__()
    #         if item.startswith("M") or item.startswith("H") or item.startswith("D") or item.startswith("W")
    #     )

# if __name__ == "__main__":
#     #tf = Timeframe()
#     for item in Timeframe:
#         print(item)
