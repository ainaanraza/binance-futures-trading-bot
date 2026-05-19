# Binance Futures Testnet Trading Bot

A professional-grade, modular Python CLI trading bot for the Binance Futures Testnet (USDT-M). This project is designed with robust backend engineering practices, demonstrating a solid understanding of trading and risk management concepts.

## Features

- **Interactive UI Mode:** Simply run `python cli.py` without arguments to launch a highly polished, step-by-step interactive wizard with validation feedback!
- **Market, Limit & Stop Orders:** Full support for `MARKET`, `LIMIT`, and `STOP` (Stop-Limit) orders, handling both `BUY` and `SELL` sides seamlessly.
- **Risk Management Engine:** Automatically calculates Risk/Reward ratios, Stop Loss (1%), Take Profit (2%), and absolute potential loss/profit values.
- **Trade Journal:** Automatically logs all executed trades into a CSV journal (`data/trade_history.csv`) for post-trade analysis.
- **Professional CLI Dashboard:** Utilizes `rich` for beautifully formatted terminal outputs, status tables, and colored success/error messages.
- **Robust Error Handling:** Comprehensive input validation, network timeout handling, and graceful exits.
- **System Logging:** Rotating file logs to capture API requests, network events, and system errors in `logs/trading_bot.log`.

## Architecture

The codebase is highly modular:
- `client.py`: Singleton-like wrapper for `python-binance` configured for the Futures Testnet.
- `validators.py`: Input validation ensuring safe execution.
- `orders.py`: Order placement logic.
- `risk_management.py`: Core logic for calculating SL/TP and potential risk.
- `journal.py`: CSV writing module for trade history.
- `cli.py`: The `argparse` driven frontend.

## Setup Instructions

### 1. Prerequisites
- Python 3.11+
- A Binance account (for accessing the testnet)

### 2. Virtual Environment Setup
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Dependency Installation
```bash
pip install -r requirements.txt
```

### 4. Binance Futures Testnet Setup
1. Go to [Binance Futures Testnet](https://testnet.binancefuture.com).
2. Log in with your Binance account or create a Testnet account.
3. Generate API Keys in the Testnet dashboard.

### 5. .env Setup
Copy the example environment file and add your keys:
```bash
cp .env.example .env
```
Edit `.env`:
```env
BINANCE_API_KEY=your_actual_testnet_api_key
BINANCE_API_SECRET=your_actual_testnet_api_secret
```

## Run Examples

### 1. Interactive Mode (Highly Recommended)
Just run the script without any arguments to trigger the `rich` interactive prompt wizard!
```bash
python cli.py
```

### 2. Command-Line Mode

**Place a MARKET Order**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**Place a LIMIT Order**
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 74000
```

**Place a STOP (Stop-Limit) Order**
```bash
python cli.py --symbol BTCUSDT --side BUY --type STOP --quantity 0.001 --price 75000 --stop-price 74500
```

## Troubleshooting
- **APIConnectionError:** Check your `.env` API keys and ensure you are using keys generated for the *Testnet*, not the main Binance site.
- **ValidationError:** Ensure you provide a positive quantity, and a price if placing a `LIMIT` order.
- **Insufficient Balance:** Add mock funds in the Binance Futures Testnet dashboard.

## Assumptions & Future Improvements
- **Assumptions:** All trades calculate a fixed 1% Stop Loss and 2% Take Profit. Limit orders use the given price as the entry price for risk calculations, while Market orders fetch the current market price for estimation before execution.
- **Future Improvements:** 
  - Dynamic position sizing based on account balance.
  - Integration with WebSockets for real-time order tracking.
  - OCO (One Cancels the Other) order placement directly on the exchange.
