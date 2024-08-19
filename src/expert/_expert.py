"""Expert
"""
import asyncio
import inspect
import os
import sys
from functools import wraps
from pprint import pprint
from typing import Any, Callable, Coroutine, TypeVar, TypeAlias

from expert._trade import Trade
from _logger import getLogger

# import typing as t

_logger = getLogger(__name__)


class Expert(Trade):
    """
    :param symbol: Инструмент с которым работает эксперт.
    :type symbol: `str` or `None`
    :param time_frame: Таймфрейм, по которому осуществляется торговля эксперт.
    :type time_frame: `str` or `set[str]` or `None`
    :param shift: Сдвиг относительно текущего бара, бар на котором осуществляется торговля эксперта.
    :type shift: `int`
    :param period: Период (интервал) баров на котором осуществляется торговля и/или прорисовка эксперта.
    :type period: `int`
    """
    __comment: str = None

    def __init__(
            self,
            symbol: str | None = None,
            time_frame: str | set[str] | None = None,
            *,
            shift: int = 0,
            period: int = 1,
            magic: int = 0,
            title: str = "",
            prefix: str = "_",
            **props: dict[str, Any]
    ) -> None:
        super().__init__(symbol, **props)
        self._symbol = symbol
        self._time_frame = time_frame
        self._shift = shift
        self._period = period
        self._magic = magic
        self._title = title
        self._prefix = prefix

        # Создание асинхронных задач
        # self.__task_on_trade = asyncio.create_task(self.on_trade)
        # self.__task_on_tick = asyncio.create_task(self.on_tick)
        # self.__task_on_timer = asyncio.create_task(self.on_timer)
        # self.__task_on_bar = asyncio.create_task(self.on_bar(time_frame))

    # @setup_method
    # def route(self, rule: str) -> Callable:
    #     def inner(func: Callable) -> Callable:
    #         print(rule)
    #         func()
    #         return func
    #
    #     return inner

    #def run(self, import_name: str) -> None:
    def run(self) -> None:
        frame = inspect.stack()[1]
        mod = inspect.getmodule(frame[0])
        # pprint(mod)

        #for attr in dir(mod):
        for attr in mod.__dict__:
            #a: list = mod.__dict__.get(attr)
            pprint(attr)
            # match attr:
            #     case "init":
            #         print(attr)
            #     case "deinit":
            #         print(attr)
            #     case "trade":
            #         print(attr)
            #     case "tick":
            #         print(attr)
            #     case "bar":
            #         print(attr)
            #     case "timer":
            #         print(attr)

        #print("")
        #pprint(mod.__dict__["init"])
        #print("")
        a: list = mod.__dict__.get("init").__qualname__.split(".")
        #pprint(a[a.index("on_init")])
        # mod.init()
        # mod.deinit()
        # mod.trade()
        # mod.tick()

        # asyncio.run()
        # self.on_init()
        # if import_name == "__main__":
        #     file_name: str | None = getattr(sys.modules["__main__"], "__file__", None)
        #     print(file_name)
        #     name: str = os.path.splitext(os.path.basename(file_name))[0]
        #     print(name)
        #     mod = __import__(name)
        #     print(mod)
        #     mod.init()
        #     mod.deinit()
        #     mod.trade()

    def on_init(self, func: Callable) -> Callable:
        def inner() -> Callable:
            #func()
            return func()

        return inner

    def on_deinit(self, func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    def on_trade(self, func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    def on_tick(self, func: Callable[[], None]) -> Callable[[], Coroutine[Any, Any, None]]:
        @wraps(func)
        def inner() -> None:
            #task = asyncio.create_task(func)
            #await task

            i = 10
            while i > 0:
                func()
                print(self, " ", i)
                i -= 1
            #return func()

        return inner

    #Call: TypeAlias = Callable[[list[Any], dict[str, Any]], None]

    def on_bar(self, time_frame: str = "1h") -> Callable:
        def outer(func: Callable[[tuple[Any, ...], dict[str, Any]], None]) -> (
                Callable[[tuple[Any, ...], dict[str, Any]], Coroutine[Any, Any, None]]
        ):
            @wraps(func)
            async def inner(*args, **kwargs) -> None:
                await func(*args, **kwargs)
                print(self, time_frame)

            return inner

        return outer

    def on_timer(self, interval: int = 1000) -> Callable:
        def outer(func: Callable) -> Callable:
            @wraps(func)
            async def inner() -> None:
                await func()
                print(self, interval)

            return inner

        return outer

    # @property
    # def magic(self) -> int:
    #     return self._magic
    #
    # @magic.setter
    # def magic(self, value: int) -> None:
    #     self._magic = value
    #
    # @property
    # def comment(self) -> str:
    #     return self.__comment
    #
    # @comment.setter
    # def comment(self, value: str) -> None:
    #     self.__comment = value + f"Magic number: {self._magic}"
