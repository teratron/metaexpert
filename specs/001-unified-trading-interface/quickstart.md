# Quickstart: Implementing a New Exchange

This guide shows the basic steps for a developer to add support for a new exchange to MetaExpert by implementing the `IExchange` interface.

## Prerequisites

- A development environment with the MetaExpert project checked out.
- Familiarity with the target exchange's API documentation.

## Step 1: Create the Exchange Module

Create a new directory for your exchange under `src/metaexpert/exchanges/`, for example, `src/metaexpert/exchanges/my_new_exchange/`.

## Step 2: Implement the `IExchange` Interface

Inside your new module, create a class that inherits from `IExchange` and implements all its abstract methods.

```python
# src/metaexpert/exchanges/my_new_exchange/connector.py

from typing import List, Optional

from src.metaexpert.core.interfaces import IExchange
from src.metaexpert.core.models import Order, Portfolio, MarketData

class MyNewExchangeConnector(IExchange):
    """A connector for MyNewExchange."""

    async def connect(self) -> None:
        print("Connecting to MyNewExchange...")
        # Add logic to connect and authenticate with the exchange API
        pass

    async def disconnect(self) -> None:
        print("Disconnecting from MyNewExchange...")
        # Add logic to close the connection
        pass

    async def fetch_portfolio(self) -> Portfolio:
        # 1. Call the exchange's API to get account balances and positions.
        # 2. Normalize the raw API response into the unified `Portfolio` Pydantic model.
        # 3. Return the `Portfolio` object.
        pass

    async def create_order(self, order: Order) -> Order:
        # 1. Convert the unified `Order` model into the format expected by the exchange's API.
        # 2. Place the order.
        # 3. Normalize the response back into a unified `Order` model and return it.
        pass

    # ... implement all other abstract methods ...

```

## Step 3: Register the Exchange

Update the factory or registration mechanism in the library to make `MyNewExchangeConnector` available to the system.

## Step 4: Write Contract Tests

Add integration tests in the `tests/contract/` directory to verify that your new implementation correctly and fully adheres to the `IExchange` contract.
