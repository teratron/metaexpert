# -*- coding: utf-8 -*-

import inspect
from enum import Enum
from pathlib import Path

from logger import Logger, get_logger


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


class Process:
    def __init__(self, name: str) -> None:
        """Initialize the event system.

        Args:
            name (str): Name of the library.
        """
        self.logger: Logger = get_logger(name)
        self.module: object | None = None
        self.filename: str | None = None

    @staticmethod
    def __get_event_from(name: str) -> Event | None:
        for event in Event:
            if event.value["name"] == name:
                return event
        return None

    @staticmethod
    def __get_number(event: Event) -> int:
        return event.value["number"]

    @staticmethod
    def __add_callback(event: Event, callback: callable) -> None:
        event.value["callback"].append(callback)

    @staticmethod
    def __len_callback(event: Event) -> int:
        return len(event.value["callback"])

    def init_process(self) -> None:
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

                    if len(qualif) > 1: # and qualif[1] in self.__list:
                        event = self.__get_event_from(qualif[1])

                        if event:
                            if self.__len_callback(event) < self.__get_number(event):
                                self.__add_callback(event, getattr(module, attr))
                            else:
                                self.logger.warning(
                                    "Too many callbacks for %s: %d",
                                    qualif[1], self.__len_callback(event) + 1
                                )

    def run_process(self, event: Event) -> None:
        """Run the process.

        Args:
            event (Event): Event to be executed.
        """
        if event in  Event:
            for callback in event.value["callback"]:
                callback()
                self.logger.debug("Launch task for %s()", event.value["name"])
        else:
            self.logger.warning("Process %s not found", event.value["name"])


