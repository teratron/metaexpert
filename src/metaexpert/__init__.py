"""MetaExpert: A Python-based Expert Trading System.

This module provides a framework for creating and managing expert trading systems
using the MetaExpert library. It includes features for event handling, logging,
and integration with various stock exchanges.
"""
from datetime import datetime
from importlib import import_module
from pathlib import Path
from types import ModuleType

from metaexpert._argument import Namespace, parse_arguments
from metaexpert._contract_type import Contract
from metaexpert._market_type import Instrument
from metaexpert._mode import Mode
from metaexpert._process import Process
from metaexpert._service import Service
from metaexpert.config import APP_NAME, MODE_BACKTEST
from metaexpert.exchanges import Exchange
from metaexpert.logger import setup_logger, Logger

logger: Logger = setup_logger(APP_NAME)


class MetaExpert(Service):
    """Expert trading system"""

    _module: ModuleType | None = None
    _filename: str | None = None

    def __init__(
            self,

            # Required Parameters
            exchange: str | None = None,
            *,

            # API Credentials (required for live mode)
            api_key: str | None = None,
            api_secret: str | None = None,
            api_passphrase: str | None = None,

            # Connection Settings
            subaccount: str | None = None,
            base_url: str | None = None,
            testnet: bool = True,
            proxy: dict[str, str] | None = None,

            # Market & Trading Mode
            market_type: str | None = "futures",
            contract_type: str | None = "inverse",
            margin_mode: str | None = "isolated",
            position_mode: str | None = "hedge",

            # Logging Configuration
            log_level: str = "INFO",
            log_file: str = "expert.log",
            trade_log_file: str = "trades.log",
            error_log_file: str = "errors.log",
            log_to_console: bool = True,

            # Advanced System Settings
            rate_limit: int = 1200,
            enable_metrics: bool = True,
            persist_state: bool = True,
            state_file: str = "state.json",
    ) -> None:
        """Initialize the expert trading system.

        Args:
            exchange (str | None): Stock exchange to use (e.g., Binance, Bybit).
            api_key (str | None): API key for authentication.
            api_secret (str | None): API secret for authentication.
            base_url (str | None): Base URL for the exchange API.
            market_type (str | None): Type of financial instruments (e.g., spot, futures).
            contract_type (str | None): Type of contract (e.g., coin_m, usdt_m).
        """

        self.args: Namespace = parse_arguments()
        self.mode: Mode = self.args.mode

        # Initialize stock exchange
        self.client: Exchange = Exchange.init(
            exchange or self.args.exchange,
            api_key or self.args.api_key,
            api_secret or self.args.api_secret,
            base_url or self.args.base_url,
            market_type or self.args.market_type,
            contract_type or self.args.contract_type
        )
        self._running: bool = False

        super().__init__()

        # Setup logger
        # self.logger: Logger = setup_logger(self.name, args.log_level)
        logger.info("Starting expert on %s", self.args.exchange)
        logger.info("Market type: %s, Contract type: %s, Mode: %s", self.args.market_type, self.args.contract_type, self.args.mode)
        logger.info("Pair: %s, Timeframe: %s", self.args.pair, self.args.timeframe)

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.strategy_name}"

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.strategy_name!r}>"

    def run(
            self,
            mode: str = "paper",
            backtest_start: str | datetime = "2024-01-01",
            backtest_end: str | datetime = "2025-08-31",
            initial_capital: float = 10000,
    ) -> None:
        """Run the expert trading system."""
        self.mode: Mode = Mode.get_mode_from(mode or self.args.mode)
        self._running: bool = True

        logger.info("Starting trading bot in %s mode", self.mode)

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
            # while self._running:
            #     # Sleep until next candle
            #     if self.mode != MODE_BACKTEST:
            #         pass
            #     else:
            #         # In backtest mode, we process all data at once
            #         self._running = False

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
