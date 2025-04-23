# -*- coding: utf-8 -*-

import inspect
from pathlib import Path

from logger import Logger, get_logger


class Event(list[dict]):
    """Event types for the trading system."""
    on_init = {
        "number": 1,
        "callback": []
    }
    on_deinit = {
        "number": 1,
        "callback": []
    }
    on_trade = {
        "number": 1,
        "callback": []
    }
    on_transaction = {
        "number": 1,
        "callback": []
    }
    on_tick = {
        "number": 3,
        "callback": []
    }
    on_bar = {
        "number": 3,
        "callback": []
    }
    on_timer = {
        "number": 5,
        "callback": []
    }
    on_book = {
        "number": 3,
        "callback": []
    }

    def __init__(self, name: str):
        super().__init__()
        self.logger: Logger = get_logger(name)
        self.module: object | None = None
        self.filename: str | None = None
        self.__enum: list[str] = self.__get_list()

    def __get_list(self) -> list[str]:
        """Get the list of event names."""
        return list(item for item in self.__dir__() if item.startswith("on_"))

    def __get_number(self, name: str) -> int:
        """Get the number of parameters for a specific event."""
        return self.__getattribute__(name)["number"]

    def __set_callback(self, name: str, callback: callable) -> None:
        """Set the callback for a specific event."""
        self.__getattribute__(name)["callback"].append(callback)

    def __len_callback(self, name: str) -> int:
        """Get the number of callbacks for a specific event."""
        return len(self.__getattribute__(name)["callback"])

    def init(self) -> None:
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

                    if len(qualif) > 1 and qualif[1] in self.__enum:
                        if self.__len_callback(qualif[1]) < self.__get_number(qualif[1]):
                            self.__set_callback(qualif[1], getattr(module, attr))
                        else:
                            self.logger.warning(
                                "Too many callbacks for %s: %d",
                                qualif[1], self.__len_callback(qualif[1]) + 1
                            )

    def run(self, name: str) -> None:
        """Run the event."""
        if name in self.__enum:
            for callback in self.__getattribute__(name)["callback"]:
                callback()
                self.logger.debug("Launch task for %s()", name)
        else:
            self.logger.warning("Event %s not found", name)
