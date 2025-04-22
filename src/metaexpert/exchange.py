# -*- coding: utf-8 -*-

# from typing import NamedTuple
from enum import Enum


# class Exchange(NamedTuple):
#     Binance: str  #binance
#     Bybit: str  #bybit


class Exchange(Enum):
    binance = {
        "name": "Binance",
    }
    bybit = {
        "name": "Bybit",
    }

    # def __init__(self, value):
    #     self.name = value["name"]

# def binance(self: {query}) -> Exchange:
#     return Exchange.Binance
