"""
Trade journal system.
"""
import os
import csv
from datetime import datetime
from typing import Dict, Any
import pandas as pd
from .logging_config import logger

DATA_DIR = "data"
JOURNAL_FILE = "trade_history.csv"
JOURNAL_PATH = os.path.join(DATA_DIR, JOURNAL_FILE)

COLUMNS = [
    "timestamp",
    "symbol",
    "side",
    "order_type",
    "quantity",
    "entry_price",
    "stop_loss",
    "take_profit",
    "status",
    "order_id"
]

def _ensure_journal_exists():
    """Ensure the data directory and CSV file exist."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    if not os.path.exists(JOURNAL_PATH):
        try:
            df = pd.DataFrame(columns=COLUMNS)
            df.to_csv(JOURNAL_PATH, index=False)
            logger.info(f"Created new trade journal at {JOURNAL_PATH}")
        except Exception as e:
            logger.error(f"Failed to create trade journal: {e}")

def log_trade(
    symbol: str, 
    side: str, 
    order_type: str, 
    quantity: float, 
    entry_price: float, 
    stop_loss: float, 
    take_profit: float, 
    status: str, 
    order_id: str
) -> None:
    """
    Log a trade into the CSV journal.
    """
    _ensure_journal_exists()

    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "symbol": symbol,
        "side": side,
        "order_type": order_type,
        "quantity": quantity,
        "entry_price": entry_price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "status": status,
        "order_id": order_id
    }

    try:
        with open(JOURNAL_PATH, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=COLUMNS)
            writer.writerow(record)
        logger.info(f"Successfully logged trade {order_id} to journal.")
    except Exception as e:
        logger.error(f"Error logging trade to journal: {e}")
