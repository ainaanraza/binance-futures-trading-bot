"""
Binance Futures Testnet API Client wrapper.
"""
import os
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from .exceptions import APIConnectionError
from .logging_config import logger

# Load environment variables
load_dotenv()

class BinanceFuturesClient:
    """Singleton wrapper for the Binance Futures Testnet client."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BinanceFuturesClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            logger.error("Missing Binance API credentials in .env file.")
            raise APIConnectionError("BINANCE_API_KEY and BINANCE_API_SECRET must be set in .env")

        try:
            # Initialize python-binance client configured for Testnet
            self.client = Client(api_key, api_secret, testnet=True)
            logger.info("Successfully initialized Binance client for Testnet.")
        except Exception as e:
            logger.exception("Failed to initialize Binance Client.")
            raise APIConnectionError(f"Failed to connect to Binance: {str(e)}")

    def get_current_price(self, symbol: str) -> float:
        """
        Fetch the current market price for a given symbol.
        """
        try:
            logger.debug(f"Fetching current price for {symbol}")
            # Ensure it queries the futures market
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            logger.debug(f"Current price for {symbol} is {price}")
            return price
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"Binance API error fetching price for {symbol}: {e}")
            raise APIConnectionError(f"Error fetching price: {e.message}")
        except Exception as e:
            logger.exception(f"Unexpected error fetching price for {symbol}: {e}")
            raise APIConnectionError(f"Unexpected error: {str(e)}")

    def place_futures_order(self, **kwargs) -> dict:
        """
        Place an order on the Futures Testnet.
        """
        try:
            logger.info(f"Placing order with params: {kwargs}")
            response = self.client.futures_create_order(**kwargs)
            logger.info(f"Order placed successfully: {response.get('orderId')}")
            return response
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"Binance API error placing order: {e}")
            raise APIConnectionError(f"Error placing order: {e.message}")
        except Exception as e:
            logger.exception(f"Unexpected error placing order: {e}")
            raise APIConnectionError(f"Unexpected error: {str(e)}")
