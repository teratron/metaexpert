import asyncio
import inspect
from enum import Enum
from threading import Thread
from types import ModuleType
from typing import Self

from metaexpert.config import APP_NAME
from metaexpert.logger import Logger, get_logger

logger: Logger = get_logger(APP_NAME)


class Process(Enum):
    """Event types for the trading system."""

    ON_INIT = {
        "name": "on_init",
        "number": 1,
        "callback": [],
        "is_async": False,
        # "status": None,  # InitStatus.INIT_SUCCEEDED
        "is_done": False,
    }
    ON_DEINIT = {
        "name": "on_deinit",
        "number": 1,
        "callback": [],
        "is_async": False
    }
    ON_TICK = {
        "name": "on_tick",
        "number": 1,
        "callback": [],
        "is_async": True
    }
    ON_BAR = {
        "name": "on_bar",
        "number": 5,
        "callback": [],
        "is_async": True
    }
    ON_TIMER = {
        "name": "on_timer",
        "number": 5,
        "callback": [],
        "is_async": True
    }
    ON_TRADE = {
        "name": "on_trade",
        "number": 1,
        "callback": [],
        "is_async": True
    }
    ON_TRANSACTION = {
        "name": "on_transaction",
        "number": 1,
        "callback": [],
        "is_async": True
    }
    ON_BOOK = {
        "name": "on_book",
        "number": 1,
        "callback": [],
        "is_async": True
    }

    # def __iter__(self) -> Generator:
    #     for item in self.value.items():
    #         yield item
    #
    # def __dir__(self) -> list[str]:
    #     """Return a list of attributes for the process."""
    #     return list(self.value.keys())

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
        module: ModuleType | None = inspect.getmodule(frame[0])
        if module is None:
            return None

        for attr in dir(module):
            # All objects of the module.
            obj: object | None = module.__dict__.get(attr)

            # All the functions of the module with decorators or without shortcuts.
            if obj and callable(obj) and not isinstance(obj, type):
                # List of hierarchy of objects, functions, decorators or closes.
                qualif: list[str] = getattr(obj, "__qualname__", "").split(".")
                if len(qualif) > 1:
                    event = cls.__get_process_from(qualif[1])
                    if event:
                        callback = event.value.get("callback")
                        if isinstance(callback, list):
                            number = event.value.get("number")
                            if isinstance(number, int):
                                if len(callback) < number:
                                    callback.append(getattr(module, attr))
                                    logger.debug(
                                        "Registering callback for '%s:%s()'",
                                        event.value.get("name"), attr
                                    )
                                else:
                                    logger.warning(
                                        "Too many callbacks for '%s': %d",
                                        qualif[1], number + 1
                                    )

        return module

    def run(self) -> None:
        """Run the process.

        This method executes the registered callbacks for the event.
        If the process is marked as asynchronous, it runs the callbacks using asyncio.
        """
        if self.value.get("is_async"):
            asyncio.run(self.__async_run())
        else:
            self.__run()

    def __run(self) -> None:
        """Run the process.

        This method executes the registered callbacks for the event.
        """
        callback = self.value.get("callback")
        if not isinstance(callback, list):
            logger.error("Callbacks for '%s' are not a list", self.value.get("name"))
            return

        for func in callback:
            func()
            logger.debug("Launch task for '%s'", self.value.get("name"))

        if hasattr(self.value, "is_done") and not self.value.get("is_done"):
            self.value["is_done"] = True
            logger.debug("Process '%s' is done", self.value.get("name"))

    async def __async_run(self) -> None:
        """Run the process asynchronously.

        This method executes the registered callbacks for the event asynchronously.
        """
        callback = self.value.get("callback")
        if not isinstance(callback, list):
            logger.error("Callbacks for '%s' are not a list", self.value.get("name"))
            return

        logger.debug("Launch task for '%s(s)'", self.value.get("name"))
        await asyncio.gather(
            *(asyncio.create_task(func()) for func in callback)
        )

    # @classmethod
    # def __gather_tasks(cls) -> tuple[Task, ...]:
    #     """Gather all tasks for the process.
    #
    #     This method collects all tasks associated with the event and returns them as a single task.
    #     """
    #     tasks: list[Task] = []
    #     for item in cls:
    #         for func in item.value.get("callback"):
    #             if cls.value.get("is_async"):
    #                 tasks.append(asyncio.create_task(func()))
    #
    #     return tuple(tasks)
    # return tuple(*(task for task in self.value.get("task")))  # if hasattr(self.value, "task")

    # @classmethod
    # async def processing(cls) -> bool:
    #     # if not cls.ON_INIT.value.get("is_done"):
    #     #     return False
    #
    #     task: list = []  # map(asyncio.create_task, )
    #     for item in cls:
    #         if item.value.get("is_async"):
    #             callback = item.value.get("callback")
    #             if not isinstance(callback, list):
    #                 logger.error("Callbacks for '%s' are not a list", item.value.get("name"))
    #                 continue
    #
    #             for func in callback:
    #                 if func and callable(func):
    #                     # print(f"Creating task for {func.__name__}")
    #                     if inspect.iscoroutinefunction(func):
    #                         # If the function is a coroutine, create an asyncio task
    #                         task.append(asyncio.create_task(func()))
    #                     else:
    #                         # If the function is a regular function, run it in a thread
    #                         task.append(asyncio.to_thread(func))
    #                 # tasks.append(asyncio.create_task(func()))
    #
    #     # await asyncio.gather(*(tuple(task)))
    #     Thread(target=asyncio.gather, args=(*(tuple(task)),), daemon=True).start()
    #
    #     # Run all tasks concurrently
    #     # Thread(
    #     #     target=WebSocketClient,
    #     #     args=("wss://stream.bybit.com/v5/public/spot", ["tickers.ADAUSDT", "orderbook.50.ADAUSDT"]),
    #     #     daemon=True
    #     # ).start()
    #
    #     return True

    @classmethod
    async def processing(cls) -> bool:
        tasks: list = []
        for item in cls:
            if item.value.get("is_async"):
                callback = item.value.get("callback")
                if not isinstance(callback, list):
                    logger.error("Callbacks for '%s' are not a list", item.value.get("name"))
                    continue

                for func in callback:
                    if func and callable(func):
                        if inspect.iscoroutinefunction(func):
                            tasks.append(asyncio.create_task(func()))
                        else:
                            tasks.append(asyncio.to_thread(func))

        Thread(target=cls.run_async_tasks, args=(tasks,), daemon=True).start()
        return True

    @staticmethod
    def run_async_tasks(tasks) -> None:
        # Создаем новый цикл событий для потока
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Запускаем задачи
            loop.run_until_complete(asyncio.gather(*tasks))
        finally:
            # Закрываем цикл событий
            loop.close()

# Создаем и запускаем поток
# thread = Thread(target=run_async_tasks, args=(tasks,), daemon=True)
# thread.start()
