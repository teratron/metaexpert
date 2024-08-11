"""Expert
"""


class Expert:
    from _logger import getLogger

    __log = getLogger(__name__)

    magic: int = 0
    comment: str = None

    def __init__(self, symbol: str = None,  time_frame: str = None,  shift: int = 0, period: int = 0) -> None:
        self.symbol = symbol
        self.time_frame = time_frame
        self.shift = shift
        self.period = period



