"""MetaExpert: A Python-based Expert Trading System.

This module provides a framework for creating and managing expert trading systems
using the MetaExpert library. It includes features for event handling, logging,
and integration with various stock exchanges.
"""

from config import APP_NAME, MODE_BACKTEST
from logger import setup_logger, Logger
from metaexpert._process import Event
from metaexpert._service import Service
from metaexpert.argument import Namespace, parse_arguments
from metaexpert.exchange import Stock, Exchange

# from metaexpert._market import Market
# from metaexpert._trade import Trade

class MetaExpert(Service):
    """Expert trading system"""

    name: str = APP_NAME

    def __init__(
            self,
            stock: Stock | str | None = None,
            api_key: str | None = None,
            api_secret: str | None = None,
            *,
            base_url: str | None = None,
            trade_type: str | None = None,
            trade_contract: str | None = None,
            trade_mode: str | None = None
    ) -> None:
        """Initialize the expert trading system.

        Args:
            stock (Stock | str | None): Stock exchange to use (e.g., Binance, Bybit).
            api_key (str | None): API key for authentication.
            api_secret (str | None): API secret for authentication.
            base_url (str | None): Base URL for the exchange API.
            trade_type (str | None): Type of trading (e.g., spot, futures).
            trade_contract (str | None): Type of contract (e.g., coin_m, usdt_m).
            trade_mode (str | None): Mode of operation (e.g., live, paper, backtest).
        """

        # Parse command line arguments
        args: Namespace = parse_arguments()

        self.stock: Stock = stock
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
        self.logger.info("Starting expert on %s", self.stock.value["name"])
        self.logger.info("Type: %s, Contract: %s, Mode: %s", args.type, args.contract, args.mode)
        self.logger.info("Pair: %s, Timeframe: %s", args.pair, args.timeframe)

        # Initialize stock exchange
        #self.init_exchange()

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.name}"

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.name!r}>"

    def run(self) -> None:
        """Run the expert trading system."""
        self.logger.info("Starting trading bot in %s mode", self.trade_mode)
        self.running = True
        # print(self.symbol)
        # print(self.timeframe)
        # print(self.filename)

        try:
            # Initialize event handling
            # self.event.init()
            self.init_process()

            # Initialize the expert
            # self.event.run("on_init")
            self.run_process(Event.ON_INIT)
            self.logger.info("Expert initialized successfully")

            while self.running:
                # Fetch latest market data
                # data = self.fetch_historical_data()

                # Sleep until next candle
                if self.trade_mode != MODE_BACKTEST:
                    pass
                    # self.logger.info("Waiting for next candle...")
                    # Calculate sleep time based on timeframe
                    # sleep_time = self._get_sleep_time()
                    # time.sleep(sleep_time)
                else:
                    # In backtest mode, we process all data at once
                    self.running = False

        except KeyboardInterrupt:
            # Handle keyboard interrupt
            self.logger.info("Expert stopped by user")
        except (ConnectionError, TimeoutError) as e:
            # Handle network-related errors
            self.logger.error("Network error occurred: %s", e)
        except ValueError as e:
            # Handle data validation errors
            self.logger.error("Data validation error: %s", e)
        except RuntimeError as e:
            # Handle runtime-specific errors
            self.logger.error("Runtime error: %s", e)
        finally:
            self.running = False
            # self.event.run("on_deinit")
            self.run_process(Event.ON_DEINIT)
            self.logger.info("Expert shutdown complete")
