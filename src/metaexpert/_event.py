# -*- coding: utf-8 -*-

import inspect
from pathlib import Path

from logger import Logger, get_logger


class Event(list[dict]):
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

    def __init__(self, name: str):
        """Initialize the event system.
        Args:
            name (str): Name of the event system.
        """
        super().__init__()
        self.logger: Logger = get_logger(name)
        self.module: object | None = None
        self.filename: str | None = None
        self.__list: list[str] = self.__get_list()
        print(self.__list)

    def __get_list(self) -> list[str]:
        """Get the list of event names."""
        return list(self.__getattribute__(item)["name"] for item in self.__dir__() if item.startswith("ON_"))

    def __get_number(self, name: str) -> int:
        """Get the number of parameters for a specific event."""
        if name not in self.__list:
            self.logger.warning("Event %s not found", name)
            return 0

        return self.__getattribute__(name.upper())["number"]

    def __set_callback(self, name: str, callback: callable) -> None:
        """Set the callback for a specific event."""
        if name not in self.__list:
            self.logger.warning("Event %s not found", name)
            return

        self.__getattribute__(name.upper())["callback"].append(callback)

    def __len_callback(self, name: str) -> int:
        """Get the number of callbacks for a specific event."""
        if name not in self.__list:
            self.logger.warning("Event %s not found", name)
            return 0

        return len(self.__getattribute__(name.upper())["callback"])

    def init_event(self) -> None:
        """Fill the event list with the callbacks."""
        frame = inspect.stack()[len(inspect.stack()) - 1]
        module = inspect.getmodule(frame[0])

        if module:
            self.module = module
            self.filename = Path(frame[1]).stem

            for attr in dir(module):
                # All objects of the module.
                obj: object | None = module.__dict__.get(attr)

                # Only module functions.
                # All the functions of the module with decorators or without shortcuts.
                if obj and callable(obj) and not isinstance(obj, type):
                    # List of hierarchy of objects, functions, decorators or closes.
                    qualif: list[str] = obj.__qualname__.split(".")

                    if len(qualif) > 1 and qualif[1] in self.__list:
                        if self.__len_callback(qualif[1]) < self.__get_number(qualif[1]):
                            self.__set_callback(qualif[1], getattr(module, attr))
                        else:
                            self.logger.warning(
                                "Too many callbacks for %s: %d",
                                qualif[1], self.__len_callback(qualif[1]) + 1
                            )

    def run_event(self, name: str) -> None:
        """Run the event."""
        if name in self.__list:
            for callback in self.__getattribute__(name.upper())["callback"]:
                callback()
                self.logger.debug("Launch task for %s()", name)
        else:
            self.logger.warning("Event %s not found", name)
