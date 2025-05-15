import asyncio
import inspect
from enum import Enum
from types import ModuleType
from typing import Self, TypedDict, Callable

from metaexpert.config import APP_NAME
from metaexpert.logger import Logger, get_logger

logger: Logger = get_logger(APP_NAME)


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
    ON_BOOK = {
        "name": "on_book",
        "number": 3,
        "callback": []
    }
    ON_TICK = {
        "name": "on_tick",
        "number": 1,
        "callback": []
    }
    ON_BAR = {
        "name": "on_bar",
        "number": 5,
        "callback": []
    }
    ON_TIMER = {
        "name": "on_timer",
        "number": 5,
        "callback": []
    }

    @classmethod
    def __get_process_from(cls, name: str) -> Self | None:
        for item in cls:
            if item.value.get("name") == name.lower():
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
                            if len(event.value.get("callback")) < event.value.get("number"):
                                event.value.get("callback").append(getattr(module, attr))
                                logger.debug(
                                    "Registering callback for %s:%s()",
                                    event.value.get("name"), attr
                                )
                            else:
                                logger.warning(
                                    "Too many callbacks for %s: %d",
                                    qualif[1], event.value.get("number") + 1
                                )
            return module

        return None

    def run(self) -> None:
        """Run the process.

        This method executes the registered callbacks for the event.
        """
        for callback in self.value.get("callback"):
            callback()
            logger.debug("Launch task for %s()", self.value.get("name"))

    async def async_run(self) -> None:
        """Run the process asynchronously.

        This method executes the registered callbacks for the event asynchronously.
        """
        # match self:
        #     case Process.ON_TRADE:
        #         # logger.info("Trading...")
        #         pass
        #     case Process.ON_TRANSACTION:
        #         # logger.info("Transaction...")
        #         pass
        #     case Process.ON_BOOK:
        #         # logger.info("Book...")
        #         pass
        #     case Process.ON_TICK:
        #         # logger.info("Tick...")
        #         pass
        #     case Process.ON_BAR:
        #         # logger.info("Bar...")
        #         pass
        #     case Process.ON_TIMER:
        #         await asyncio.gather(
        #             *(
        #                 asyncio.create_task(Timer(interval=0, callback=callback).start())
        #                 for callback in self.value.get("callback")
        #             )
        #         )
        # logger.info("Timer...")

        await asyncio.gather(
            *(asyncio.create_task(callback()) for callback in self.value.get("callback"))
        )
        logger.debug("Launch task for %s()", self.value.get("name"))
