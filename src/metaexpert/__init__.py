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
from pathlib import Path
from types import ModuleType

from metaexpert.cli.argument_parser import Namespace, parse_arguments
from metaexpert.config import APP_NAME, MODE_BACKTEST
from metaexpert.core._trade_mode import TradeMode
from metaexpert.core.events import Service
from metaexpert.core.process import Process
from metaexpert.exchanges import Exchange
from metaexpert.logger import Logger, configure_logging, setup_logger

# Set up the main logger for the MetaExpert system
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
        structured_logging: bool = False,
        async_logging: bool = False,
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

        # Parse command line arguments
        self.args: Namespace = parse_arguments()
        self.trade_mode: TradeMode | None = None
        self.backtest_start: str | datetime | None = None
        self.backtest_end: str | datetime | None = None
        self.initial_capital: float | None = None
        self._running: bool = False

        # Initialize stock exchange
        self.client: Exchange = Exchange.create(
            exchange_name=exchange or self.args.exchange,
            api_key=api_key or self.args.api_key,
            api_secret=api_secret or self.args.api_secret,
            base_url=base_url or self.args.base_url,
            market_type=market_type or self.args.market_type,
            contract_type=contract_type or self.args.contract_type,
        )

        # Setup enhanced logger with new features
        self._setup_enhanced_logging(
            log_level=log_level,
            log_file=log_file,
            trade_log_file=trade_log_file,
            error_log_file=error_log_file,
            log_to_console=log_to_console,
            structured_logging=structured_logging,
            async_logging=async_logging,
        )

        # Log initialization
        logger.info("Starting expert on %s", self.args.exchange)
        logger.info(
            "Market type: %s, Contract type: %s, Mode: %s",
            self.args.market_type,
            self.args.contract_type,
            self.args.trade_mode,
        )
        logger.info("Pair: %s, Timeframe: %s", self.args.pair, self.args.timeframe)

    def _setup_enhanced_logging(
        self,
        log_level: str,
        log_file: str,
        trade_log_file: str,
        error_log_file: str,
        log_to_console: bool,
        structured_logging: bool,
        async_logging: bool,
    ) -> None:
        """Set up enhanced logging with the new features.

        Args:
            log_level: Logging level
            log_file: Main log file
            trade_log_file: Trade execution log file
            error_log_file: Error-specific log file
            log_to_console: Whether to print logs to console
            structured_logging: Whether to use structured JSON logging
            async_logging: Whether to use asynchronous logging
        """
        try:
            # Configure centralized logging system
            config = {
                "default_level": log_level,
                "handlers": {
                    "console": {
                        "level": log_level,
                        "format": "[%(asctime)s] %(levelname)s: %(name)s: %(message)s",
                        "structured": structured_logging,
                    },
                    "file": {
                        "level": log_level,
                        "format": "[%(asctime)s] %(levelname)s: %(name)s: %(message)s",
                        "structured": structured_logging,
                        "filename": log_file,
                        "max_size": 10485760,  # 10MB
                        "backup_count": 5,
                    },
                    "trade_file": {
                        "level": "INFO",
                        "format": "[%(asctime)s] %(levelname)s: %(name)s: %(message)s",
                        "structured": structured_logging,
                        "filename": trade_log_file,
                        "max_size": 10485760,  # 10MB
                        "backup_count": 5,
                    },
                    "error_file": {
                        "level": "ERROR",
                        "format": "[%(asctime)s] %(levelname)s: %(name)s: %(message)s",
                        "structured": structured_logging,
                        "filename": error_log_file,
                        "max_size": 10485760,  # 10MB
                        "backup_count": 5,
                    },
                },
                "structured_logging": structured_logging,
                "async_logging": async_logging,
            }

            # Apply configuration
            result = configure_logging(config)
            if result["status"] == "error":
                logger.warning(
                    "Failed to configure enhanced logging: %s", result["message"]
                )

            # Note: We don't reassign the global logger here to avoid the syntax error
            # The enhanced features are configured through the centralized configuration system

        except Exception as e:
            logger.error("Failed to set up enhanced logging: %s", str(e))

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.strategy_name}"

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.strategy_name!r}>"

    def run(
        self,
        trade_mode: str = "paper",
        backtest_start: str | datetime = datetime.now()
        .replace(year=datetime.now().year - 1)
        .strftime("%Y-%m-%d"),
        backtest_end: str | datetime = datetime.now().strftime("%Y-%m-%d"),
        initial_capital: float = 10000,
    ) -> None:
        """Run the expert trading system."""
        self.trade_mode = TradeMode.get_mode_from(
            trade_mode or self.args.trade_mode
        )
        self.backtest_start = backtest_start
        self.backtest_end = backtest_end
        self.initial_capital = initial_capital
        self._running = True

        logger.info("Starting trading bot in %s mode", self.trade_mode)

        try:
            # Initialize event handling
            self._module = Process.init()

            if self._module and self._module.__file__:
                self._filename = Path(self._module.__file__).stem

            # Initialize the expert
            Process.ON_INIT.run()
            logger.info("Expert initialized successfully")

            # Register the expert with the process
            ws_url = self.client.get_websocket_url(self.symbol, self.timeframe)
            Process.processing(ws_url)

            # Main event loop
            while self._running:
                # Sleep until next candle
                if self.trade_mode != MODE_BACKTEST:
                    pass
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
    # balance = import_module("metaexpert.exchanges.binance").get_balance
