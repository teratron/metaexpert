import asyncio
import inspect
from enum import Enum
from types import ModuleType
from typing import Self

from metaexpert.config import APP_NAME
from metaexpert.logger import Logger, get_logger

# from threading import Thread

logger: Logger = get_logger(APP_NAME)


class Process(Enum):
    """Event types for the trading system."""

    ON_INIT = {
        "name": "on_init",
        "number": 1,
        "callback": [],
        # "status": None,  # InitStatus.INIT_SUCCEEDED
        "is_done": False,
    }
    ON_DEINIT = {
        "name": "on_deinit",
        "number": 1,
        "callback": [],
    }
    ON_TICK = {
        "name": "on_tick",
        "number": 1,
        "callback": [],
        "task": []
    }
    ON_BAR = {
        "name": "on_bar",
        "number": 5,
        "callback": [],
        "task": []
    }
    ON_TIMER = {
        "name": "on_timer",
        "number": 5,
        "callback": [],
        "task": []
    }
    ON_TRADE = {
        "name": "on_trade",
        "number": 1,
        "callback": [],
    }
    ON_TRANSACTION = {
        "name": "on_transaction",
        "number": 1,
        "callback": [],
    }
    ON_BOOK = {
        "name": "on_book",
        "number": 1,
        "callback": [],
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

        if not module:
            return None

        for attr in dir(module):
            # All objects of the module.
            obj: object | None = module.__dict__.get(attr)

            # All the functions of the module with decorators or without shortcuts.
            if obj and callable(obj) and not isinstance(obj, type):
                # List of hierarchy of objects, functions, decorators or closes.
                qualif: list[str] = obj.__qualname__.split(".")

                if len(qualif) > 1:
                    event = cls.__get_process_from(qualif[1])

                    if event:
                        if len(event.value.get("callback")) < event.value.get("number"):
                            func = getattr(module, attr)
                            event.value.get("callback").append(func)
                            logger.debug(
                                "Registering callback for '%s:%s()'",
                                event.value.get("name"), attr
                            )

                            if hasattr(event.value, "task"):
                                event.value.get("task").append(asyncio.create_task(func()))
                                logger.debug(
                                    "Creating task for '%s:%s()'",
                                    event.value.get("name"), attr
                                )
                        else:
                            logger.warning(
                                "Too many callbacks for '%s': %d",
                                qualif[1], event.value.get("number") + 1
                            )

        return module

    def run(self) -> None:
        """Run the process.

        This method executes the registered callbacks for the event.
        """
        for func in self.value.get("callback"):
            func()
            logger.debug("Launch task for '%s'", self.value.get("name"))

        if hasattr(self.value, "is_done") and not self.value.get("is_done"):
            self.value["is_done"] = True
            logger.debug("Process '%s' is done", self.value.get("name"))

    async def async_run(self) -> None:
        """Run the process asynchronously.

        This method executes the registered callbacks for the event asynchronously.
        """
        logger.debug("Launch task for '%s(s)'", self.value.get("name"))
        await asyncio.gather(
            *(asyncio.create_task(func()) for func in self.value.get("callback"))
        )

    def __gather_tasks(self) -> tuple[asyncio.Task]:
        """Gather all tasks for the process.

        This method collects all tasks associated with the event and returns them as a single task.
        """
        return tuple(*(task for task in self.value.get("task")))  # if hasattr(self.value, "task")

    @classmethod
    def processing(cls) -> bool:
        if not cls.ON_INIT.value.get("is_done"):
            return False

        # Thread(
        #     target=WebSocketClient,
        #     args=("wss://stream.bybit.com/v5/public/spot", ["tickers.ADAUSDT", "orderbook.50.ADAUSDT"]),
        #     daemon=True
        # ).start()

        return True
