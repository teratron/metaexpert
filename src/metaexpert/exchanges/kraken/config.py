# Configuration for the Kraken exchange.
from pydantic import Field
from pydantic_settings import BaseSettings


class KrakenConfig(BaseSettings):
    """
    Kraken API configuration.
    """

    kraken_api_key: str = Field(..., env="KRAKEN_API_KEY")
    kraken_api_secret: str = Field(..., env="KRAKEN_API_SECRET")