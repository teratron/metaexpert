"""Expert
"""
import asyncio
from functools import wraps, update_wrapper
from typing import Any, Callable, Coroutine, TypeVar, cast

from expert._trade import Trade
from _logger import getLogger
import typing as t

_logger = getLogger(__name__)
F = TypeVar("F", bound=Callable[..., Any])


def setup_method(func: F) -> F:
    def wrapper_func(self: Expert, *args: Any, **kwargs: Any) -> Any:
        return func(self, *args, **kwargs)

    return cast(F, update_wrapper(wrapper_func, func))


class Expert(Trade):
    """
    :param symbol: Инструмент с которым работает эксперт.
    :type symbol: str or set[str] or None
    :param time_frame: Таймфрейм, по которому осуществляется торговля эксперт.
    :type time_frame: str or set[str] or None
    :param shift: Сдвиг относительно текущего бара, бар на котором осуществляется торговля эксперта.
    :type shift: int
    :param period: Период (интервал) баров на котором осуществляется торговля и/или прорисовка эксперта.
    :type period: int
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

    @setup_method
    def route(self, rule: str) -> Callable:
        def inner(func: Callable) -> Callable:
            print(rule)
            func()
            return func

        return inner

    @setup_method
    def on_init(self, func) -> None:
        pass

    @setup_method
    def on_deinit(self, func) -> None:
        pass

    @setup_method
    def on_trade(self, func) -> None:
        pass

    @setup_method
    def on_tick(self, func: Callable[[], None]) -> Callable[[], Coroutine[Any, Any, None]]:
        @wraps(func)
        async def inner() -> None:
            task = asyncio.create_task(func)
            await task

            i = 10
            while i > 0:
                func()
                print(self, " ", i)
                i -= 1

        return inner

    @setup_method
    def on_timer(self, interval: int = 1000) -> Callable:
        def outer(func: Callable) -> Callable:
            @wraps(func)
            async def inner() -> Coroutine:
                await func()
                print(self, interval)
                return await func()

            return inner

        return outer

    # Call: TypeAlias = Callable[[list[Any], dict[str, Any]], None]
    def on_bar(self, time_frame: str = "1h") -> Callable:
        async def outer(func: Callable[[tuple[Any, ...], dict[str, Any]], None]) -> (
                Callable[[tuple[Any, ...], dict[str, Any]], Coroutine[Any, Any, None]]
        ):
            @wraps(func)
            async def inner(*args, **kwargs) -> None:
                func(*args, **kwargs)
                print(self, time_frame)

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
