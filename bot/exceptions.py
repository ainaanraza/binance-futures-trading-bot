"""
Custom exceptions for the trading bot.
"""

class ValidationError(Exception):
    """Raised when user input fails validation."""
    pass


class APIConnectionError(Exception):
    """Raised when there is an issue connecting to the Binance API."""
    pass


class OrderPlacementError(Exception):
    """Raised when an order fails to be placed on the exchange."""
    pass
