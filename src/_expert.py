"""Expert
"""
from _trade import Trade


class Expert(Trade):
    from _logger import getLogger

    __log = getLogger(__name__)

    magic: int = 0
    comment: str = None

    def __init__(
            self,
            symbol: str | set[str] | None = None,
            time_frame: str | set[str] | None = None,
            shift: int = 0,
            period: int = 0
    ) -> None:
	super().__init__(symbol, time_frame, shift, period)
        self.symbol = symbol
        self.time_frame = time_frame
        self.shift = shift
        self.period = period
