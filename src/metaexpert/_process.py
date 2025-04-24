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
    def __init__(self, name: str):
        """Initialize the event system.

        Args:
            name (str): Name of the event.
        """
        super().__init__()
        self.logger: Logger = get_logger(name)
        self.module: object | None = None
        self.filename: str | None = None
        self.__list: list[str] = self.__get_list()
        # print(self[0])

    @staticmethod
    def __get_event_from(name: str) -> Event | None:
        """Get the event from its name.

        Args:
            name (str): Name of the event.

        Returns:
            Event | None: Event object if found, else None.
        """
        for event in Event:
            if event.value["name"] == name:
                return event

        return None

    @staticmethod
    def __get_list() -> list[str]:
        """Get the list of event names.

        Returns:
            list[str]: List of event names.
        """
        #return list(self.__getattribute__(item)["name"] for item in self.__dir__() if item.startswith("ON_"))
        return list(item.value["name"] for item in Event)

    def __get_number(self, name: str) -> int:
        """Get the number of parameters for a specific event.

        Args:
            name (str): Name of the event.
        """
        if name not in self.__list:
            self.logger.warning("Event %s not found", name)
            return 0

        return self.__getattribute__(name.upper())["number"]

    def __set_callback(self, name: str, callback: callable) -> None:
        """Set the callback for a specific event.

        Args:
            name (str): Name of the event.
            callback (callable): Callback function to be executed.
        """
        if name not in self.__list:
            self.logger.warning("Event %s not found", name)
            return

        self.__getattribute__(name.upper())["callback"].append(callback)

    def __len_callback(self, name: str) -> int:
        """Get the number of callbacks for a specific event.

        Args:
            name (str): Name of the event.
        """
        if name not in self.__list:
            self.logger.warning("Event %s not found", name)
            return 0

        return len(self.__getattribute__(name.upper())["callback"])

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

                    if len(qualif) > 1 and qualif[1] in self.__list:
                        if self.__len_callback(qualif[1]) < self.__get_number(qualif[1]):
                            self.__set_callback(qualif[1], getattr(module, attr))
                        else:
                            self.logger.warning(
                                "Too many callbacks for %s: %d",
                                qualif[1], self.__len_callback(qualif[1]) + 1
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


