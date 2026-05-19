"""
Input validation for CLI arguments.
"""
from typing import Optional
from .exceptions import ValidationError

def validate_inputs(symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None, stop_price: Optional[float] = None) -> None:
    """
    Validate all inputs before proceeding with order placement.
    Raises ValidationError if any check fails.
    """
    # 1. Validate Symbol format (basic check)
    if not symbol or not symbol.isalnum() or len(symbol) < 3:
        raise ValidationError(f"Invalid symbol format: '{symbol}'. Must be alphanumeric.")

    # 2. Validate Side
    valid_sides = ["BUY", "SELL"]
    if side.upper() not in valid_sides:
        raise ValidationError(f"Invalid side: '{side}'. Must be one of {valid_sides}.")

    # 3. Validate Order Type
    valid_types = ["MARKET", "LIMIT", "STOP"]
    if order_type.upper() not in valid_types:
        raise ValidationError(f"Invalid order type: '{order_type}'. Must be one of {valid_types}.")

    # 4. Validate Quantity
    if quantity <= 0:
        raise ValidationError(f"Invalid quantity: {quantity}. Must be greater than 0.")

    # 5. Validate Price/StopPrice for LIMIT and STOP orders
    if order_type.upper() == "LIMIT":
        if price is None or price <= 0:
            raise ValidationError(f"A valid positive price is required for LIMIT orders. Got: {price}")
    elif order_type.upper() == "STOP":
        if price is None or price <= 0:
            raise ValidationError(f"A valid positive price is required for STOP orders. Got: {price}")
        if stop_price is None or stop_price <= 0:
            raise ValidationError(f"A valid positive stop_price is required for STOP orders. Got: {stop_price}")
    elif order_type.upper() == "MARKET":
        pass
