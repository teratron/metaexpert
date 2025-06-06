"""MetaExpert: A Python-based Expert Trading System.

This module provides a framework for creating and managing expert trading systems
using the MetaExpert library. It includes features for event handling, logging,
and integration with various stock exchanges.
"""
from importlib import import_module
from pathlib import Path
from types import ModuleType

from metaexpert._argument import Namespace, parse_arguments
from metaexpert._contract import Contract
from metaexpert._instrument import Instrument
from metaexpert._mode import Mode
from metaexpert._process import Process
from metaexpert._service import Service
from metaexpert.config import APP_NAME, MODE_BACKTEST
from metaexpert.exchanges import Exchange
from metaexpert.logger import setup_logger, Logger

# from metaexpert._market import Market
# from metaexpert._trade import Trade

logger: Logger = setup_logger(APP_NAME)


class MetaExpert(Service):
    """Expert trading system"""

    _module: ModuleType | None = None
    _filename: str | None = None

    def __init__(
            self,
            stock: str | None = None,
            api_key: str | None = None,
            api_secret: str | None = None,
            *,
            base_url: str | None = None,
            instrument: str | None = None,
            contract: str | None = None,
            mode: str | None = None
    ) -> None:
        """Initialize the expert trading system.

        Args:
            stock (str | None): Stock exchange to use (e.g., Binance, Bybit).
            api_key (str | None): API key for authentication.
            api_secret (str | None): API secret for authentication.
            base_url (str | None): Base URL for the exchange API.
            instrument (str | None): Type of financial instruments (e.g., spot, futures).
            contract (str | None): Type of contract (e.g., coin_m, usdt_m).
            mode (str | None): Mode of operation (e.g., live, paper, backtest).
        """

        # Parse command line arguments
        args: Namespace = parse_arguments()

        # Initialize stock exchange
        self.client: Exchange = Exchange.init(
            stock or args.stock,
            api_key or args.api_key,
            api_secret or args.api_secret,
            base_url or args.base_url,
            instrument or args.type,
            contract or args.contract
        )
        self.mode: Mode | None = Mode.get_mode_from(mode or args.mode)
        self._running: bool = False

        super().__init__()

        # Setup logger
        # self.logger: Logger = setup_logger(self.name, args.log_level)
        logger.info("Starting expert on %s", args.stock)
        logger.info("Type: %s, Contract: %s, Mode: %s", args.type, args.contract, args.mode)
        logger.info("Pair: %s, Timeframe: %s", args.pair, args.timeframe)

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.name}"

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.name!r}>"

    def run(self) -> None:
        """Run the expert trading system."""
        logger.info("Starting trading bot in %s mode", self.mode)
        self._running = True

        try:
            # Initialize event handling
            self._module = Process.init()

            if self._module and self._module.__file__:
                self._filename: str = Path(self._module.__file__).stem

            # Initialize the expert
            Process.ON_INIT.run()
            logger.info("Expert initialized successfully")

            # Register the expert with the process
            Process.processing()

            # Запускаем основной цикл обработки событий
            while self._running:
                # Fetch latest market data
                # data = self.fetch_historical_data()

                # Sleep until next candle
                if self.mode != MODE_BACKTEST:
                    pass
                    # self.logger.info("Waiting for next candle...")
                    # Calculate sleep time based on timeframe
                    # sleep_time = self._get_sleep_time()
                    # time.sleep(sleep_time)
                else:
                    # In backtest mode, we process all data at once
                    self._running = False

        except KeyboardInterrupt:
            # Handle keyboard interrupt
            logger.info("Expert stopped by user")
        except (ConnectionError, TimeoutError) as e:
            # Handle network-related errors
            logger.error("Network error occurred: %s", e)
        except ValueError as e:
            # Handle data validation errors
            logger.error("Data validation error: %s", e)
        except RuntimeError as e:
            # Handle runtime-specific errors
            logger.error("Runtime error: %s", e)
        finally:
            self._running = False
            Process.ON_DEINIT.run()
            logger.info("Expert shutdown complete")

    # from metaexpert.exchanges.binance import balance
    balance = import_module("metaexpert.exchanges.binance").balance
