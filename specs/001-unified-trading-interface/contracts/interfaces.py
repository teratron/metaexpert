# Python Interfaces for the Unified Trading System
#
# This file defines the abstract contracts that all components, especially
# exchange-specific implementations, must adhere to. It uses Pydantic models
# (defined in `src/metaexpert/core/models.py`) for data transfer.

from abc import ABC, abstractmethod
from typing import List, Optional

# Assume models are in src.metaexpert.core.models
# from src.metaexpert.core.models import Order, Trade, Position, MarketData, Portfolio

# This is a placeholder for the actual models for context
class BaseModel:
    pass
class Order(BaseModel): pass
class Trade(BaseModel): pass
class Position(BaseModel): pass
class MarketData(BaseModel): pass
class Portfolio(BaseModel): pass


class IExchange(ABC):
    """An abstract interface representing the unified contract for an exchange connection."""

    @abstractmethod
    async def connect(self) -> None:
        """Establishes and authenticates the connection to the exchange."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Closes the connection to the exchange."""
        pass

    @abstractmethod
    async def fetch_portfolio(self) -> Portfolio:
        """Fetches the user's entire portfolio, including balances and open positions."""
        pass

    @abstractmethod
    async def fetch_open_orders(self, symbol: Optional[str] = None) -> List[Order]:
        """Fetches all open orders for a specific symbol or all symbols."""
        pass

    @abstractmethod
    async def create_order(self, order: Order) -> Order:
        """Places a new order on the exchange."""
        pass

    @abstractmethod
    async def cancel_order(self, order_id: str) -> bool:
        """Cancels an existing order by its ID."""
        pass

    @abstractmethod
    async def fetch_historical_data(self, symbol: str, timeframe: str, since: int, limit: int) -> List[MarketData]:
        """Fetches historical market data (OHLCV)."""
        pass


class ITradingStrategy(ABC):
    """An abstract interface for a trading strategy."""

    @abstractmethod
    def on_tick(self, tick: MarketData):
        """Called on every new market tick."""
        pass

    @abstractmethod
    def on_bar(self, bar: MarketData):
        """Called on every new complete candle/bar."""
        pass

    @abstractmethod
    def on_order_update(self, order: Order):
        """Called when an order's status changes."""
        pass

    @abstractmethod
    def on_trade(self, trade: Trade):
        """Called when a trade is executed."""
        pass
