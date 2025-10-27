"""MetaExpert: A Python-based Expert Trading System."""

from datetime import datetime
from pathlib import Path
from types import ModuleType
from typing import Literal, cast

# from metaexpert.cli.argument_parser import Namespace, parse_arguments
from metaexpert.config import (
    BACKTEST_END_DATE,
    BACKTEST_START_DATE,
    DEFAULT_CONTRACT_TYPE,
    DEFAULT_MARGIN_MODE,
    DEFAULT_MARKET_TYPE,
    DEFAULT_POSITION_MODE,
    DEFAULT_TRADE_MODE,
    INITIAL_CAPITAL,
    LOG_ASYNC_LOGGING,
    LOG_CONSOLE_LOGGING,
    LOG_ERROR_FILE,
    LOG_FILE,
    LOG_LEVEL,
    LOG_STRUCTURED_LOGGING,
    LOG_TRADE_FILE,
    LOG_LEVEL_TYPE,
)
from metaexpert.core import Events, EventType, TradeMode
from metaexpert.exchanges import MetaExchange
from metaexpert.logger import BoundLogger, get_logger, setup_logging

from .logger.config import LoggerConfig


class MetaExpert(Events):
    """Expert trading system"""

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
        market_type: str = DEFAULT_MARKET_TYPE,
        contract_type: str = DEFAULT_CONTRACT_TYPE,
        margin_mode: str = DEFAULT_MARGIN_MODE,
        position_mode: str = DEFAULT_POSITION_MODE,
        #
        # --- Logging Configuration ---
        log_level: LOG_LEVEL_TYPE = LOG_LEVEL,
        log_file: str = LOG_FILE,
        trade_log_file: str = LOG_TRADE_FILE,
        error_log_file: str = LOG_ERROR_FILE,
        log_to_console: bool = LOG_CONSOLE_LOGGING,
        structured_logging: bool = LOG_STRUCTURED_LOGGING,
        async_logging: bool = LOG_ASYNC_LOGGING,
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
        """
        # Configure logging using the enhanced expert integration
        # Note: This setups global logging state. Only one MetaExpert instance should manage logging.
        # Create a config based on the provided parameters
        # Note: LoggerConfig does not support structured_logging and async_logging directly.
        # We will ignore these for now, or map them if possible (e.g. structured_logging -> json_logs).
        # For this fix, we will pass only supported parameters.
        # The specific file paths and settings are handled by the global config.
        # This is a simplification and might require more complex logic to truly customize per instance.
        # A better approach might be to have a dedicated logger for each expert, but that's a larger change.
        # Let's adapt the call to setup_logging with supported params.
        # LoggerConfig does not take structured_logging and async_logging.
        # We'll map structured_logging to json_logs if True, otherwise False.
        # async_logging is likely not supported directly in setup.py.
        # We will pass supported params and ignore unsupported ones.
        config = LoggerConfig(
            log_level=log_level,
            log_file=log_file,
            trade_log_file=trade_log_file,
            error_log_file=error_log_file,
            log_to_console=log_to_console,
            # structured_logging=structured_logging, # Not supported in LoggerConfig
            # async_logging=async_logging, # Not supported in LoggerConfig
            json_logs=structured_logging,  # Map structured_logging to json_logs
            # Other params like log_dir, max_bytes etc. use defaults from LoggerConfig
        )
        # Setup logging with the new config. This affects global state.
        setup_logging(config)
        # Get the logger instance
        self.logger: BoundLogger = get_logger(self.__class__.__name__)

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

        self.trade_mode: TradeMode | None = None
        self.backtest_start: str | datetime | None = None
        self.backtest_end: str | datetime | None = None
        self.initial_capital: float | None = None
        self._module: ModuleType | None = None
        self._filename: str | None = None
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
        trade_mode: str = DEFAULT_TRADE_MODE,
        backtest_start: str | datetime = BACKTEST_START_DATE,
        backtest_end: str | datetime = BACKTEST_END_DATE,
        initial_capital: float = INITIAL_CAPITAL,
    ) -> None:
        """Run the expert trading system.

        Args:

           trade_mode (str): Trading mode ('paper', 'live', 'backtest').
           backtest_start (str | datetime): Start date for backtesting.
           backtest_end (str | datetime): End date for backtesting.
           initial_capital (float): Initial capital for paper trading or backtesting.
        """
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
            self._module = EventType.init()
            if self._module and self._module.__file__:
                self._filename = Path(self._module.__file__).stem

            # Initialize the expert
            EventType.ON_INIT.run()
            self.logger.info("Expert initialized successfully")

            # Register the expert with the process
            if self.symbol is None:
                raise ValueError("Cannot get websocket URL without a symbol.")
            if self.timeframe is None:
                raise ValueError("Cannot get websocket URL without a timeframe.")

            ws_url = self.client.get_websocket_url(
                self.symbol, self.timeframe.get_name()
            )
            self.logger.info("Websocket URL: {ws_url}", ws_url=ws_url)
            EventType.processing(ws_url)

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
            EventType.ON_DEINIT.run()
            self.logger.info("Expert shutdown complete")

    # from metaexpert.exchanges.binance import balance
    # balance = import_module("metaexpert.exchanges.binance").get_balance
