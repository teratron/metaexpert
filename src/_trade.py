"""Trade
"""
from dataclasses import dataclass
from typing import Any

from _logger import getLogger

_logger = getLogger(__name__)


@dataclass
class Trade:
    _lots: float = 0
    _stop_loss: float = 0
    _take_profit: float = 0
    _trailing_stop: float = 0
    _positions: int = 0
    _slippage: int = 0

    def __init__(self, symbol: str | None, **props: dict[str, Any]) -> None:
        self.symbol = symbol
        self._lots = props.get("lots", 0)
        self._stop_loss = props.get("stop_loss", 0)
        self._take_profit = props.get("take_profit", 0)
        self._trailing_stop = props.get("trailing_stop", 0)
        self._positions = props.get("positions", 0)
        self._slippage = props.get("slippage", 0)

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

    # @property
    # def lots(self) -> float:
    #     return self._lots
    #
    # @lots.setter
    # def lots(self, value: float) -> None:
    #     self._lots = value
    #
    # @property
    # def stop_loss(self) -> float:
    #     return self._stop_loss
    #
    # @stop_loss.setter
    # def stop_loss(self, value: float) -> None:
    #     self._stop_loss = value
    #
    # @property
    # def take_profit(self) -> float:
    #     return self._take_profit
    #
    # @take_profit.setter
    # def take_profit(self, value: float) -> None:
    #     self._take_profit = value
    #
    # @property
    # def trailing_stop(self) -> float:
    #     return self._trailing_stop
    #
    # @trailing_stop.setter
    # def trailing_stop(self, value: float) -> None:
    #     self._trailing_stop = value
    #
    # @property
    # def positions(self) -> int:
    #     return self._positions
    #
    # @positions.setter
    # def positions(self, value: int) -> None:
    #     self._positions = value
    #
    # @property
    # def slippage(self) -> int:
    #     return self._slippage
    #
    # @slippage.setter
    # def slippage(self, value: int) -> None:
    #     self._slippage = value

# struct sTrade
#   {
# protected:
#    string            m_symbol;
#    ENUM_TIMEFRAMES   m_time_frame;
#    int               m_magic;
#    string            m_comment;
#    double            m_lots;
#    double            m_stop_loss;
#    double            m_take_profit;
#    double            m_trailing_stop;
#    int               m_positions;
#    uint              m_slippage;
#    //---
#    datetime          m_long_timer;
#    datetime          m_short_timer;
#    int               m_long_position;
#    int               m_short_position;
#
# public:
#    //--- конструктор с параметром по умолчанию
#                      sTrade(void);
#    //--- конструктор с параметрами
#                      sTrade(const string symbol, const ENUM_TIMEFRAMES time_frame, const int magic, const string comment, const double lots, const uint stop_loss, const uint take_profit, const uint trailing_stop, const uint position);
#    //--- конструктор копирования
#                      sTrade(const sTrade &trade);
#    //--- деструктор
#                     ~sTrade(void);
#    //---
#    int               Init(const string symbol, const ENUM_TIMEFRAMES time_frame, const int magic, const string comment, const double lots, const uint stop_loss, const uint take_profit, const uint trailing_stop, const uint position);
#    //---
#    bool              Processing(const int signal_long, const int signal_short);
#    bool              Processing(const int signal);
#    bool              Processing(void);
#    //---
#    bool              OpenPosition(const ENUM_POSITION_TYPE type);
#    bool              LongOpened(void) {return(OpenPosition(POSITION_TYPE_BUY));}
#    bool              ShortOpened(void) {return(OpenPosition(POSITION_TYPE_SELL));}
#    //---
#    int               ClosePositions(const ENUM_POSITION_TYPE type);
#    int               LongClosed(void) {return(ClosePositions(POSITION_TYPE_BUY));}
#    int               ShortClosed(void) {return(ClosePositions(POSITION_TYPE_SELL));}
#    //---
#    int               ClosePositionsBy(const ENUM_POSITION_TYPE type);
#    int               LongClosedBy(void) {return(ClosePositionsBy(POSITION_TYPE_BUY));}
#    int               ShortClosedBy(void) {return(ClosePositionsBy(POSITION_TYPE_SELL));}
#    //---
#    bool              ModifyPosition(const ENUM_POSITION_TYPE type);
#    bool              LongModified(void) {return(ModifyPosition(POSITION_TYPE_BUY));}
#    bool              ShortModified(void) {return(ModifyPosition(POSITION_TYPE_SELL));}
#
# protected:
#    bool              CheckParameters(void);
#    bool              CheckLots(void);
#    void              CheckingAbilityOpenTransactions(void);
#    double            MarginCheck(const ENUM_ORDER_TYPE type, const double price) const;
#    double            FreeMarginCheck(const ENUM_ORDER_TYPE type, const double price) const;
#   };