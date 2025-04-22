""" """

from config import APP_NAME
from logger import setup_logger, Logger
from metaexpert._process import Process
from metaexpert.arguments import Namespace, parse_arguments
from metaexpert.exchange import Exchange


class MetaExpert(Process):
    """Expert trading system"""

    name: str = APP_NAME

    def __init__(
            self,
            stock: Exchange | str | None = None,
            api_key: str | None = None,
            api_secret: str | None = None,
            *,
            base_url: str | None = None,
            trade_type: str | None = None,
            trade_contract: str | None = None,
            trade_mode: str | None = None
    ) -> None:
        self.stock: Exchange = stock
        self.api_key: str = api_key
        self.api_secret: str = api_secret
        self.base_url: str = base_url
        self.trade_type: str = trade_type
        self.trade_contract: str = trade_contract
        self.trade_mode: str = trade_mode

        # Parse command line arguments
        args: Namespace = parse_arguments()

        # Setup logger
        self.logger: Logger = setup_logger(self.name, args.log_level)
        self.logger.info("Starting expert trading system")
        self.logger.info("Type: %s, Contract: %s, Mode: %s", args.type, args.contract, args.mode)
        self.logger.info("Pair: %s, Timeframe: %s", args.pair, args.timeframe)
        
        super().__init__(self.name)

        match self.stock:
            case Exchange.binance:
                self.logger.debug("Binance exchange selected")
            case Exchange.bybit:
                self.logger.debug("Bybit exchange selected")
            case _:
                self.logger.warning("Unknown exchange selected")

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.name}"

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.name!r}>"

    # def run(self):
    #    pass

    # from metaexpert._market import Market
    # from metaexpert._trade import Trade
