import argparse
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm

from bot.validators import validate_inputs
from bot.client import BinanceFuturesClient
from bot.orders import place_market_order, place_limit_order, place_stop_limit_order
from bot.risk_management import RiskManagementEngine
from bot.journal import log_trade
from bot.logging_config import logger
from bot.exceptions import ValidationError, APIConnectionError, OrderPlacementError

console = Console()

def print_banner():
    banner = Text("🚀 Binance Futures Trading Bot (Testnet) 🚀", style="bold magenta", justify="center")
    console.print(Panel(banner, border_style="magenta", expand=False))

def print_success(message: str):
    console.print(f"[bold green]✔ SUCCESS:[/bold green] {message}")

def print_error(message: str):
    console.print(f"[bold red]✖ ERROR:[/bold red] {message}")

def parse_args():
    parser = argparse.ArgumentParser(description="Binance Futures CLI Trading Bot")
    parser.add_argument("--symbol", type=str, help="Trading pair symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, help="Order side (BUY or SELL)")
    parser.add_argument("--type", type=str, help="Order type (MARKET, LIMIT, or STOP)")
    parser.add_argument("--quantity", type=float, help="Quantity to trade")
    parser.add_argument("--price", type=float, help="Price for LIMIT or STOP orders")
    parser.add_argument("--stop-price", type=float, help="Stop price for STOP orders")
    return parser.parse_args()

def interactive_mode():
    """Interactive wizard for order placement."""
    console.print("[cyan]Entering Interactive Mode...[/cyan]\n")
    
    symbol = Prompt.ask("Enter Trading Symbol", default="BTCUSDT").upper()
    side = Prompt.ask("Enter Order Side", choices=["BUY", "SELL"], default="BUY").upper()
    order_type = Prompt.ask("Enter Order Type", choices=["MARKET", "LIMIT", "STOP"], default="MARKET").upper()
    
    quantity_str = Prompt.ask("Enter Quantity (e.g., 0.001)")
    try:
        quantity = float(quantity_str)
    except ValueError:
        print_error("Quantity must be a number.")
        sys.exit(1)
        
    price = None
    stop_price = None
    
    if order_type in ["LIMIT", "STOP"]:
        price_str = Prompt.ask("Enter Limit Price")
        try:
            price = float(price_str)
        except ValueError:
            print_error("Price must be a number.")
            sys.exit(1)
            
    if order_type == "STOP":
        stop_price_str = Prompt.ask("Enter Stop Price")
        try:
            stop_price = float(stop_price_str)
        except ValueError:
            print_error("Stop price must be a number.")
            sys.exit(1)
            
    # Confirm before proceeding
    console.print("\n[yellow]Order Summary:[/yellow]")
    console.print(f"Symbol: {symbol}\nSide: {side}\nType: {order_type}\nQty: {quantity}")
    if price: console.print(f"Price: {price}")
    if stop_price: console.print(f"Stop Price: {stop_price}")
    
    if not Confirm.ask("\nProceed with this order?"):
        console.print("[red]Order cancelled by user.[/red]")
        sys.exit(0)
        
    return symbol, side, order_type, quantity, price, stop_price

def main():
    print_banner()
    
    # Check if run interactively (no arguments provided)
    if len(sys.argv) == 1:
        symbol, side, order_type, quantity, price, stop_price = interactive_mode()
    else:
        args = parse_args()
        if not args.symbol or not args.side or not args.type or not args.quantity:
            print_error("Missing required arguments for CLI mode. Run without arguments for Interactive Mode.")
            sys.exit(1)
        symbol = args.symbol.upper()
        side = args.side.upper()
        order_type = args.type.upper()
        quantity = args.quantity
        price = args.price
        stop_price = args.stop_price

    # 1. Validate Inputs
    try:
        validate_inputs(symbol, side, order_type, quantity, price, stop_price)
    except ValidationError as e:
        print_error(str(e))
        logger.warning(f"Validation failed: {e}")
        sys.exit(1)

    # 2. Connect to Client & Get Price
    console.print("\n[cyan]Connecting to Binance Testnet...[/cyan]")
    try:
        client = BinanceFuturesClient()
        current_price = client.get_current_price(symbol)
        console.print(f"[green]Current market price for {symbol}:[/green] ${current_price:,.4f}\n")
    except APIConnectionError as e:
        print_error(str(e))
        sys.exit(1)

    # Determine Entry Price for Risk Calc
    entry_price = price if order_type in ["LIMIT", "STOP"] else current_price

    # 3. Risk Management Analysis
    risk_engine = RiskManagementEngine(side, entry_price, quantity)
    risk_engine.display_analysis()

    # 4. Place Order
    console.print(f"[yellow]Placing {order_type} {side} order for {quantity} {symbol}...[/yellow]")
    order_id = "N/A"
    status = "FAILED"
    try:
        if order_type == "MARKET":
            response = place_market_order(symbol, side, quantity)
        elif order_type == "LIMIT":
            response = place_limit_order(symbol, side, quantity, price)
        elif order_type == "STOP":
            response = place_stop_limit_order(symbol, side, quantity, price, stop_price)
        
        status = response.get("status", "UNKNOWN")
        order_id = str(response.get("order_id", "N/A"))
        avg_price = response.get("avg_price", 0)

        print_success(f"Order placed successfully! ID: {order_id} | Status: {status}")
        
        if avg_price > 0:
            console.print(f"[green]Executed at average price:[/green] ${avg_price:,.4f}")
            entry_price = avg_price

    except OrderPlacementError as e:
        print_error(str(e))
        logger.error(f"Order placement failed: {e}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        logger.exception("Unexpected error during order placement.")
        sys.exit(1)

    # 5. Log Trade
    console.print("[cyan]Saving trade to journal...[/cyan]")
    log_trade(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        entry_price=entry_price,
        stop_loss=risk_engine.stop_loss,
        take_profit=risk_engine.take_profit,
        status=status,
        order_id=order_id
    )
    print_success("Trade saved to journal.")
    console.print("\n[bold magenta]Done.[/bold magenta]")

if __name__ == "__main__":
    main()
