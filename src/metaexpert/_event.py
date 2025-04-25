# -*- coding: utf-8 -*-

from enum import Enum
from typing import Self


class Event(Enum):
    """Event types for the trading system."""
    ON_INIT = {
        "name": "on_init",
        "number": 1,
        "callback": []
    }
    ON_DEINIT = {
        "name": "on_deinit",
        "number": 1,
        "callback": []
    }
    ON_TRADE = {
        "name": "on_trade",
        "number": 1,
        "callback": []
    }
    ON_TRANSACTION = {
        "name": "on_transaction",
        "number": 1,
        "callback": []
    }
    ON_TICK = {
        "name": "on_tick",
        "number": 3,
        "callback": []
    }
    ON_BAR = {
        "name": "on_bar",
        "number": 3,
        "callback": []
    }
    ON_TIMER = {
        "name": "on_timer",
        "number": 5,
        "callback": []
    }
    ON_BOOK = {
        "name": "on_book",
        "number": 3,
        "callback": []
    }

    @classmethod
    def get_event_from(cls, name: str) -> Self | None:
        for item in cls:
            if item.value["name"] == name:
                return item
        return None
