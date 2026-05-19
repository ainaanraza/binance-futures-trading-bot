"""
Order placement helper functions.
"""
from typing import Dict, Any
from .client import BinanceFuturesClient
from .exceptions import OrderPlacementError

def place_market_order(symbol: str, side: str, quantity: float) -> Dict[str, Any]:
    """
    Place a MARKET order.
    """
    client_instance = BinanceFuturesClient()
    
    try:
        response = client_instance.place_futures_order(
            symbol=symbol,
            side=side.upper(),
            type="MARKET",
            quantity=quantity
        )
        return _parse_order_response(response)
    except Exception as e:
        raise OrderPlacementError(f"Failed to place MARKET order: {str(e)}")


def place_limit_order(symbol: str, side: str, quantity: float, price: float) -> Dict[str, Any]:
    """
    Place a LIMIT order.
    """
    client_instance = BinanceFuturesClient()
    
    try:
        response = client_instance.place_futures_order(
            symbol=symbol,
            side=side.upper(),
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=price
        )
        return _parse_order_response(response)
    except Exception as e:
        raise OrderPlacementError(f"Failed to place LIMIT order: {str(e)}")


def place_stop_limit_order(symbol: str, side: str, quantity: float, price: float, stop_price: float) -> Dict[str, Any]:
    """
    Place a STOP (Stop-Limit) order.
    """
    client_instance = BinanceFuturesClient()
    
    try:
        response = client_instance.place_futures_order(
            symbol=symbol,
            side=side.upper(),
            type="STOP",
            timeInForce="GTC",
            quantity=quantity,
            price=price,
            stopPrice=stop_price
        )
        return _parse_order_response(response)
    except Exception as e:
        raise OrderPlacementError(f"Failed to place STOP order: {str(e)}")


def _parse_order_response(response: dict) -> Dict[str, Any]:
    """
    Parse the Binance API response and extract necessary fields.
    """
    return {
        "order_id": response.get("orderId"),
        "status": response.get("status"),
        "executed_qty": float(response.get("executedQty", 0)),
        "avg_price": float(response.get("avgPrice", 0)),
        "raw_response": response
    }
