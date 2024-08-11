"""Trade
"""
from _expert import Expert


class Trade:
    from _logger import getLogger

    __log = getLogger(__name__)

    def __init__(self,
                 symbol: str = None,
                 time_frame: str = None,
                 lots: int = 0,
                 stop_loss: float = 0,
                 take_profit: float = 0,
                 trailing_stop: float = 0,
                 positions: int = 0,
                 slippage: float = 0) -> None:
        # super().__init__(symbol, time_frame, shift, period)
        self.lots = lots
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.trailing_stop = trailing_stop
        self.positions = positions
        self.slippage = slippage
