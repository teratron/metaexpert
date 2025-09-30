"""MetaExpert: A Python-based Expert Trading System.

This module provides a framework for creating and managing expert trading systems
using the MetaExpert library. It includes features for event handling, logging,
and integration with various stock exchanges.

The system supports multiple trading modes and configurations:
- Market types: spot, futures, options
- Contract types: linear (USD-M) or inverse (COIN-M) for futures
- Margin modes: isolated or cross margin
- Position modes: hedge (two-way) or oneway (one-way)
- Position sizing: fixed base, fixed quote, percent equity, or risk-based

Enums:
- SizeType: Position sizing methods
- ContractType: Contract types for futures trading
- MarginMode: Margin modes for futures trading
- PositionMode: Position modes for futures trading
"""

from datetime import datetime
from logging import Logger
from pathlib import Path
from types import ModuleType

#from metaexpert.cli.argument_parser import Namespace, parse_arguments
from metaexpert.config import (
    BACKTEST_END_DATE,
    BACKTEST_START_DATE,
    ENABLE_METRICS,
    INITIAL_CAPITAL,
    LIB_NAME,
    LOG_ASYNC_LOGGING_ENABLED,
    LOG_CONSOLE_LOGGING_ENABLED,
    LOG_ERROR_FILE,
    LOG_FILE,
    LOG_LEVEL,
    LOG_STRUCTURED_LOGGING_ENABLED,
    LOG_TRADE_FILE,
    PERSIST_STATE,
    RATE_LIMIT,
    STATE_FILE,
    TRADE_MODE_PAPER,
)
from metaexpert.core import MetaProcess, Process, Service, TradeMode
from metaexpert.exchanges import MetaExchange
from metaexpert.logger import MetaLogger


class MetaExpert(Service):
    """Expert trading system"""

    _module: ModuleType | None = None
    _filename: str | None = None

    def __init__(
        self,
        #
        # --- Required Parameters ---
        exchange: str,
        *,
        # --- API Credentials (required for live mode) ---
        api_key: str | None = None,
        api_secret: str | None = None,
        api_passphrase: str | None = None,
        #
        # --- Connection Settings ---
        subaccount: str | None = None,
        base_url: str | None = None,
        testnet: bool = True,
        proxy: dict[str, str] | None = None,
        #
        # --- Market & Trading Mode ---
        market_type: str = "futures",
        contract_type: str = "inverse",
        margin_mode: str = "isolated",
        position_mode: str = "hedge",
        #
        # --- Logging Configuration ---
        log_level: str = LOG_LEVEL,
        log_file: str = LOG_FILE,
        trade_log_file: str = LOG_TRADE_FILE,
        error_log_file: str = LOG_ERROR_FILE,
        log_to_console: bool = LOG_CONSOLE_LOGGING_ENABLED,
        structured_logging: bool = LOG_STRUCTURED_LOGGING_ENABLED,
        async_logging: bool = LOG_ASYNC_LOGGING_ENABLED,
        #
        # --- Advanced System Settings ---
        rate_limit: int = RATE_LIMIT,
        enable_metrics: bool = ENABLE_METRICS,
        persist_state: bool = PERSIST_STATE,
        state_file: str = STATE_FILE,
    ) -> None:
        """Initialize the expert trading system.

        Args:
            exchange (str): Stock exchange to use (e.g., Binance, Bybit).
            api_key (str | None): API key for authentication.
            api_secret (str | None): API secret for authentication.
            api_passphrase (str | None): API passphrase (required for some exchanges).
            subaccount (str | None): Subaccount name (for exchanges that support it).
            base_url (str | None): Base URL for the exchange API.
            testnet (bool): Whether to use testnet.
            proxy (dict[str, str] | None): Proxy settings.
            market_type (str | None): Type of financial instruments (e.g., spot, futures, options).
            contract_type (str | None): Type of contract for futures (e.g., linear, inverse).
            margin_mode (str | None): Margin mode for futures (e.g., isolated, cross).
            position_mode (str | None): Position mode for futures (e.g., hedge, oneway).
            log_level (str): Logging level.
            log_file (str): Main log file.
            trade_log_file (str): Trade execution log file.
            error_log_file (str): Error-specific log file.
            log_to_console (bool): Whether to print logs to console.
            structured_logging (bool): Whether to use structured JSON logging.
            async_logging (bool): Whether to use asynchronous logging.
            rate_limit (int): Max requests per minute.
            enable_metrics (bool): Enable performance metrics.
            persist_state (bool): Persist state between runs.
            state_file (str): State persistence file.
        """

        # Configure logging using the enhanced expert integration
        self.logger: Logger = MetaLogger(
            name=LIB_NAME,
            log_level=log_level,
            log_file=log_file,
            trade_log_file=trade_log_file,
            error_log_file=error_log_file,
            log_to_console=log_to_console,
            structured_logging=structured_logging,
            async_logging=async_logging,
        )

        # Parse command line arguments
        #self.args: Namespace = parse_arguments()

        # Initialize stock exchange
        self.client: MetaExchange = MetaExchange.create(
            exchange=exchange,
            api_key=api_key,
            api_secret=api_secret,
            api_passphrase=api_passphrase,
            subaccount=subaccount,
            base_url=base_url,
            testnet=testnet,
            proxy=proxy,
            market_type=market_type,
            contract_type=contract_type,
            margin_mode=margin_mode,
            position_mode=position_mode,
        )

        #  Initialize process
        self.system: MetaProcess = MetaProcess(
            client=self.client,
            rate_limit=rate_limit,
            enable_metrics=enable_metrics,
            persist_state=persist_state,
            state_file=state_file,
        )

        self.trade_mode: TradeMode | None = None
        self.backtest_start: str | datetime | None = None
        self.backtest_end: str | datetime | None = None
        self.initial_capital: float | None = None
        self._running: bool = False

        # Log initialization
        self.logger.info("Starting expert on %s", exchange)
        self.logger.info(
            "Market type: %s, Contract type: %s, Margin mode: %s, Position mode: %s",
            market_type,
            contract_type,
            margin_mode,
            position_mode,
        )

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.strategy_name}"

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.strategy_name!r}>"

    def run(
        self,
        trade_mode: str = TRADE_MODE_PAPER,
        backtest_start: str | datetime = BACKTEST_START_DATE,
        backtest_end: str | datetime = BACKTEST_END_DATE,
        initial_capital: float = INITIAL_CAPITAL,
    ) -> None:
        """Run the expert trading system."""
        self.trade_mode = TradeMode.get_trade_mode_from(trade_mode)
        self.backtest_start = backtest_start
        self.backtest_end = backtest_end
        self.initial_capital = initial_capital
        self._running = True

        self.logger.info(
            "Starting trading bot in %s mode",
            self.trade_mode.get_name(),
        )

        try:
            # Initialize event handling
            self._module = Process.init()
            if self._module and self._module.__file__:
                self._filename = Path(self._module.__file__).stem

            # Initialize the expert
            Process.ON_INIT.run()
            self.logger.info("Expert initialized successfully")

            # Register the expert with the process
            if self.symbol is None:
                raise ValueError("Cannot get websocket URL without a symbol.")
            if self.timeframe is None:
                raise ValueError("Cannot get websocket URL without a timeframe.")
            ws_url = self.client.get_websocket_url(
                self.symbol, self.timeframe.get_name()
            )
            Process.processing(ws_url)

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
            self._running = False
            Process.ON_DEINIT.run()
            self.logger.info("Expert shutdown complete")

    # from metaexpert.exchanges.binance import balance
    # balance = import_module("metaexpert.exchanges.binance").get_balance
