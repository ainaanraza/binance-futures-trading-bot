"""
Lightweight Risk Management Engine.
"""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

class RiskManagementEngine:
    def __init__(self, side: str, entry_price: float, quantity: float):
        self.side = side.upper()
        self.entry_price = entry_price
        self.quantity = quantity
        self.stop_loss_pct = 0.01  # 1%
        self.take_profit_pct = 0.02 # 2%

        self.stop_loss = self._calculate_stop_loss()
        self.take_profit = self._calculate_take_profit()
        self.risk_reward_ratio = "1:2"
        self.potential_loss = self._calculate_potential_loss()
        self.potential_profit = self._calculate_potential_profit()

    def _calculate_stop_loss(self) -> float:
        if self.side == "BUY":
            return self.entry_price * (1 - self.stop_loss_pct)
        else:
            return self.entry_price * (1 + self.stop_loss_pct)

    def _calculate_take_profit(self) -> float:
        if self.side == "BUY":
            return self.entry_price * (1 + self.take_profit_pct)
        else:
            return self.entry_price * (1 - self.take_profit_pct)

    def _calculate_potential_loss(self) -> float:
        # absolute difference between entry and stop loss, multiplied by quantity
        return abs(self.entry_price - self.stop_loss) * self.quantity

    def _calculate_potential_profit(self) -> float:
        return abs(self.entry_price - self.take_profit) * self.quantity

    def display_analysis(self) -> None:
        """
        Display a professional trade analysis summary using rich.
        """
        table = Table(show_header=False, box=None)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="yellow")
        
        table.add_row("Entry Price", f"${self.entry_price:,.4f}")
        table.add_row("Stop Loss", f"${self.stop_loss:,.4f}")
        table.add_row("Take Profit", f"${self.take_profit:,.4f}")
        table.add_row("Risk/Reward Ratio", self.risk_reward_ratio)
        table.add_row("Potential Loss", f"${self.potential_loss:,.2f}", style="red")
        table.add_row("Potential Profit", f"${self.potential_profit:,.2f}", style="green")

        panel = Panel(
            table,
            title="[bold blue]Trade Analysis[/bold blue]",
            border_style="blue",
            expand=False
        )
        console.print(panel)
        console.print()
