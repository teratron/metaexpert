# -*- coding: utf-8 -*-

from enum import Enum


class Exchange(Enum):
    """Exchange enumeration for supported exchanges."""
    BINANCE = {
        "name": "Binance",
        "description": "Binance exchange",
    }
    BYBIT = {
        "name": "Bybit",
        "description": "Bybit exchange",
    }
