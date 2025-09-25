"""Trade
"""
from dataclasses import dataclass
from typing import Any

from metaexpert.logger import get_logger

_logger = get_logger(__name__)


@dataclass
class Trade:
    """Trade
    """

    def __init__(self, symbol: str | None, **props: dict[str, Any]) -> None:
        self.symbol: str = symbol if symbol else ""
        self._lots: float = props.__getattribute__("lots")
        self._stop_loss: float = props.get("stop_loss_pct", 0)
        self._take_profit: float = props.get("take_profit_pct", 0)
        self._trailing_stop: float = props.get("trailing_stop_pct", 0)
        self._positions: int = props.get("positions", 0)
        self._slippage: int = props.get("slippage", 0)

    def trade(
            self,
            *,
            lots: float = 0,
            stop_loss: float = 0,
            take_profit: float = 0,
            trailing_stop: float = 0,
            positions: int = 0,
            slippage: int = 0
    ) -> None:
        self._lots = lots
        self._stop_loss = stop_loss
        self._take_profit = take_profit
        self._trailing_stop = trailing_stop
        self._positions = positions
        self._slippage = slippage

    # POSITION
    def open_position(self, side: str) -> bool:
        return False

    def close_position(self, side: str) -> bool:
        return False

    def close_all_positions(self, side: str) -> bool:
        return False

    def modify_position(self) -> bool:
        return False

    def modify_all_positions(self) -> bool:
        return False

    # ORDER
    def open_order(self, side: str) -> bool:
        return False

    def close_order(self, side: str) -> bool:
        return False

    def close_all_orders(self, side: str) -> bool:
        return False

#    datetime          m_long_timer;
#    datetime          m_short_timer;
#    int               m_long_position;
#    int               m_short_position;
#
#    bool              CheckParameters(void);
#    bool              CheckLots(void);
#    void              CheckingAbilityOpenTransactions(void);
#    double            MarginCheck(const ENUM_ORDER_TYPE type, const double price) const;
#    double            FreeMarginCheck(const ENUM_ORDER_TYPE type, const double price) const;
