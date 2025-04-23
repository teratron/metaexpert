# -*- coding: utf-8 -*-

from enum import Enum


class Event(Enum):
    """Event types for the trading system."""
    ON_INIT = {
        "name": "on_init",
        "description": "Initialization event",
        "number": 1,
        "callback": None
    }
    ON_DEINIT = {
        "name": "on_deinit",
        "description": "Deinitialization event",
        "number": 1,
        "callback": None
    }
    ON_TRADE = {
        "name": "on_trade",
        "description": "Trade event",
        "number": 1,
        "callback": None
    }
    ON_TRANSACTION = {
        "name": "on_transaction",
        "description": "Transaction event",
        "number": 1,
        "callback": None
    }
    ON_TICK = {
        "name": "on_tick",
        "description": "Tick event",
        "number": 3,
        "callback": {}
    }
    ON_BAR = {
        "name": "on_bar",
        "description": "Bar event",
        "number": 3,
        "callback": {}
    }
    ON_TIMER = {
        "name": "on_timer",
        "description": "Timer event",
        "number": 5,
        "callback": {}
    }
    ON_BOOK = {
        "name": "on_book",
        "description": "Book event",
        "number": 3,
        "callback": {}
    }

    # def __init__(self, value):
    #     self.name: str = value["name"]
    #     self.description: str = value["description"]
    #     self.number: int = value["number"]
    #     self.callback: set | None = value["callback"]
