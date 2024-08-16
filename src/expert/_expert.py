"""Expert
"""
import asyncio
from functools import wraps
from typing import Any, Callable, Coroutine

from expert._trade import Trade
from _logger import getLogger

_logger = getLogger(__name__)


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
        self.__task_on_trade = asyncio.create_task(self.on_trade)
        self.__task_on_tick = asyncio.create_task(self.on_tick)
        self.__task_on_minute = asyncio.create_task(self.on_minute)
        self.__task_on_bar = asyncio.create_task(self.on_bar(time_frame))

    async def __aenter__(self) -> None:
        await self.__task_on_trade
        await self.__task_on_tick
        await self.__task_on_minute
        await self.__task_on_bar

    def on_init(self, func) -> None:
        pass

    def on_deinit(self, func) -> None:
        pass

    async def on_trade(self, func) -> None:
        pass

    async def on_tick(self, func: Callable[[], None]) -> Callable[[], Coroutine[Any, Any, None]]:
        async def inner() -> None:
            while True:
                func()
                print(self)

        return inner

    async def on_minute(self, func) -> None:
        pass

    # Call: TypeAlias = Callable[[list[Any], dict[str, Any]], None]
    def on_bar(self, time_frame="1h") -> Callable:
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
