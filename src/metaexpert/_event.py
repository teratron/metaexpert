# -*- coding: utf-8 -*-

import inspect
from pathlib import Path


class Event(set[dict]):
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

    def __init__(self):
        super().__init__()
        self.filename: str | None = None

    def _set_callback(self, name: str, callback: callable) -> None:
        """Set the callback for a specific event."""
        if name in self:
            self.__getattribute__(name)["callback"] = callback
        else:
            raise ValueError(f"Event {name} not found.")

    def _set_number(self, name: str, number: int) -> None:
        """Set the number of parameters for a specific event."""
        if name in self:
            self.__getattribute__(name)["number"] = number
        else:
            raise ValueError(f"Event {name} not found.")

    def fill(self) -> None:
        frame = inspect.stack()[len(inspect.stack()) - 1]
        module = inspect.getmodule(frame[0])
        # print(self.ON_INIT["name"])

        # Obtaining a file name
        self.filename = Path(frame[1]).stem
        # self.logger.debug("Processing file: %s", self.filename)
        a = (i['name'] for i in iter(self))
        print(a.__iter__())  # if i[0].startswith("ON_")
        if module:
            num: int = 0
            #     dec: set[str] = {event} if isinstance(event, str) else event
            #
            for attr in dir(module):
                # All objects of the module.
                obj: object | None = module.__dict__.get(attr)

                # Only module functions.
                # All the functions of the module with decorators or without shortcuts.
                if obj and callable(obj) and not isinstance(obj, type):
                    # List of hierarchy of objects, functions, decorators or closes.
                    qualif: list[str] = obj.__qualname__.split(".")

                    if len(qualif) > 1:
                        if qualif[0] == __class__.__name__ or qualif[0] == self.__class__.__name__:
                            if any(qualif[1] == item["name"] for item in self if isinstance(self, dict)):
                                num += 1
                                print("+++")
                                # asyncio.run(getattr(module, attr)())
                                getattr(module, attr)()
                                # self.logger.debug("Launch task for @%s:%s()", qualif[1], attr)
