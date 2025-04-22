""" """

from config import APP_NAME, MODE_LIVE, MODE_BACKTEST
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
        # Parse command line arguments
        args: Namespace = parse_arguments()

        self.stock: Exchange = stock
        self.api_key: str = api_key
        self.api_secret: str = api_secret
        self.base_url: str = base_url
        self.trade_type: str = trade_type
        self.trade_contract: str = trade_contract
        self.trade_mode: str = trade_mode
        self.running: bool = False

        super().__init__(self.name)

        # Setup logger
        self.logger: Logger = setup_logger(self.name, args.log_level)
        self.logger.info("Starting expert in %s mode", self.symbol)
        self.logger.info("Type: %s, Contract: %s, Mode: %s", args.type, args.contract, args.mode)
        self.logger.info("Pair: %s, Timeframe: %s", args.pair, args.timeframe)

        self._init_exchange()

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.name}"

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.name!r}>"

    def _init_exchange(self):
        match self.stock:
            case Exchange.binance:
                self.logger.debug("Binance exchange selected")
            case Exchange.bybit:
                self.logger.debug("Bybit exchange selected")
            case _:
                self.logger.warning("Unknown exchange selected")

        if self.trade_mode == MODE_LIVE and (not self.api_key or not self.api_secret):
            self.logger.error("API key and secret are required for live trading")
            raise ValueError("API key and secret are required for live trading")

        # Initialize client with or without authentication based on mode
        if self.trade_mode == MODE_BACKTEST or (not self.api_key or not self.api_secret):
            # self.client = Spot()
            self.logger.info("Initialized Binance client in public mode")
        else:
            # self.client = Spot(api_key=self.api_key, api_secret=self.api_secret, base_url=self.base_url)
            self.logger.info("Initialized Binance client with API key authentication")

    def run(self) -> None:
        try:
            # Initialize and run the trading bot
            self._run("on_init", 1)
            self.logger.info("Expert initialized successfully")

            # self._run(self.__events)
            # while True:
            #     pass
        except KeyboardInterrupt:
            self.logger.info("Expert stopped by user")
        except (ConnectionError, TimeoutError) as e:
            self.logger.exception("An error occurred: %s", e)
        finally:
            self._run("on_deinit")
            self.logger.info("Expert shutdown complete")

    # from metaexpert._market import Market
    # from metaexpert._trade import Trade
