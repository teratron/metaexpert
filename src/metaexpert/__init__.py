""" """

from logger import get_logger, Logger
from metaexpert._process import Process
from metaexpert.exchange import Exchange


class MetaExpert(Process):
    """Expert trading system"""

    name: str = "MetaExpert"

    def __init__(
            self,
            *,
            stock: Exchange | None = None,
            api_key: str | None = None,
            api_secret: str | None = None,
            base_url: str | None = None,
            trade_type: str | None = None,
            trade_contract: str | None = None,
            trade_mode: str | None = None
    ) -> None:
        self.stock: Exchange = stock
        self.api_key: str = api_key
        self.api_secret: str = api_secret
        self.base_url: str = base_url
        self.logger: Logger = get_logger(__name__)
        self.trade_type: str = trade_type
        self.trade_contract: str = trade_contract
        self.trade_mode: str = trade_mode
        super().__init__(self.name)

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.name}"

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.name!r}>"

    # def run(self):
    #    pass

    # from metaexpert._market import Market
    # from metaexpert._trade import Trade
