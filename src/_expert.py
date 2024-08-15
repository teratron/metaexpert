"""Expert
"""
from typing import Any

from _trade import Trade
from _logger import getLogger

_logger = getLogger(__name__)


class Expert(Trade):
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
        """
        :param symbol: Инструмент с которым работает эксперт.
        :type symbol: str | set[str] | None
        :param time_frame: Таймфрейм, по которому осуществляется торговля эксперт.
        :type time_frame: str | set[str] | None
        :param shift: Сдвиг относительно текущего бара, бар на котором осуществляется торговля эксперта.
        :type shift: int
        :param period: Период (интервал) баров на котором осуществляется торговля и/или прорисовка эксперта.
        :type period: int
        """
        super().__init__(symbol, **props)
        self._symbol = symbol
        self._time_frame = time_frame
        self._shift = shift
        self._period = period
        self._magic = magic
        self._title = title
        self._prefix = prefix

    @property
    def magic(self) -> int:
        return self._magic

    @magic.setter
    def magic(self, value: int) -> None:
        self._magic = value

    @property
    def comment(self) -> str:
        return self.__comment

    @comment.setter
    def comment(self, value: str) -> None:
        self.__comment = value + f"Magic number: {self._magic}"
