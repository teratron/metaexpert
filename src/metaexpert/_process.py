# -*- coding: utf-8 -*-

import inspect
from enum import Enum
from types import ModuleType
from typing import Self, TypedDict, Callable


# from logger import get_logger

class ProcessDict(TypedDict):
    name: str
    number: int
    callback: list[Callable]


class Process(Enum):
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
    def __get_process_from(cls, name: str) -> Self | None:
        for item in cls:
            if item.value["name"] == name.lower():
                return item

        return None

    @classmethod
    def init(cls) -> ModuleType | None:
        """Initialize the process.

        This method is called to set up the process and register callbacks.
        It inspects the current module to find functions decorated with
        specific event decorators and registers them as callbacks for the
        corresponding events.
        """
        # logger = get_logger(__name__)
        frame = inspect.stack()[len(inspect.stack()) - 1]
        module: ModuleType = inspect.getmodule(frame[0])

        if module:
            for attr in dir(module):
                # All objects of the module.
                obj: object | None = module.__dict__.get(attr)

                # Only module functions.
                # All the functions of the module with decorators or without shortcuts.
                if obj and callable(obj) and not isinstance(obj, type):
                    # List of hierarchy of objects, functions, decorators or closes.
                    qualif: list[str] = obj.__qualname__.split(".")

                    if len(qualif) > 1:
                        event = cls.__get_process_from(qualif[1])

                        if event:
                            if len(event.value["callback"]) < event.value["number"]:
                                event.value["callback"].append(getattr(module, attr))
                            #     logger.debug(
                            #         "Registering callback for %s:%s()",
                            #         event.value["name"], attr
                            #     )
                            # else:
                            #     logger.warning(
                            #         "Too many callbacks for %s: %d",
                            #         qualif[1], event.value["number"] + 1
                            #     )
            return module

        return None

    def run(self) -> None:
        """Run the process.

        This method executes the registered callbacks for the event.
        """
        # logger = get_logger(__name__)
        for callback in self.value["callback"]:
            callback()
            # logger.debug("Launch task for %s()", self.value["name"])
