# Trading Bot — Binance Futures Testnet

A clean, beginner-friendly Python CLI tool for placing orders on the Binance Futures Testnet (USDT-M).

Supports **MARKET**, **LIMIT**, and **STOP_MARKET** orders with structured logging, input validation, and clear error messages.

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance API client (signing, HTTP)
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # CLI input validation
│   └── logging_config.py  # File + console logging setup
├── logs/                  # Auto-created; daily rotating log files
├── cli.py                 # CLI entry point (argparse)
├── .env.example           # Credential template
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone / unzip the project

```bash
cd trading_bot
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get Binance Futures Testnet credentials

1. Go to [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
2. Sign in with your GitHub account.
3. Navigate to **API Key** in the top menu.
4. Click **Generate** — your key and secret are shown once, save them immediately.

### 5. Configure credentials

```bash
cp .env.example .env
# Edit .env and fill in your key and secret
```

`.env`:
```
BINANCE_API_KEY=your_key_here
BINANCE_API_SECRET=your_secret_here
```

> **Never commit your `.env` file.** Add it to `.gitignore`.

---

## How to Run

### MARKET order

```bash
# Buy 0.001 BTC at market price
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# Sell 0.01 ETH at market price
python cli.py --symbol ETHUSDT --side SELL --type MARKET --quantity 0.01
```

### LIMIT order

```bash
# Sell 0.01 ETH when price reaches 3200 USDT
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3200

# Buy 0.001 BTC at 40000 USDT (GTC — resting order)
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 40000

# Immediate-or-Cancel limit order
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 42000 --tif IOC
```

### STOP_MARKET order *(bonus order type)*

```bash
# Trigger a market sell if BTC drops to 60000
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 60000
```

### Sample output

```
──────────────────────────────────────────────────
  Order Request Summary
──────────────────────────────────────────────────
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.001

──────────────────────────────────────────────────
  Order Response
──────────────────────────────────────────────────
  Order ID   : 3851293741
  Status     : FILLED
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Orig Qty   : 0.001
  Exec Qty   : 0.001
  Avg Price  : 42850.30
  Time       : 1736936622104

──────────────────────────────────────────────────
  Result
──────────────────────────────────────────────────
  Order placed successfully!
```

---

## Logging

Logs are written to `logs/trading_bot_YYYYMMDD.log` (rotating, max 5 MB, 3 backups).

Each line records:
- Timestamp
- Log level
- Module name
- Full API request params (signature redacted)
- Full API response

Sample log entries are included in `logs/` for reference.

---

## Assumptions

- **Testnet only** — the base URL is hardcoded to `https://testnet.binancefuture.com`. Change `BASE_URL` in `bot/client.py` to go live (at your own risk).
- **USDT-M contracts** only. Coin-M (delivery) contracts use a different endpoint.
- Quantities are passed as-is to the API. If the exchange rejects a quantity precision error, reduce decimal places (e.g. `0.001` instead of `0.0013`).
- `python-binance` is intentionally **not** used — direct REST calls make the authentication and signing logic fully transparent and educational.

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `requests` | HTTP client for Binance REST API |
| `python-dotenv` | Load `.env` credentials |

---

## Error Handling

| Scenario | Behaviour |
|----------|-----------|
| Missing/invalid CLI args | Argparse error with usage hint |
| Bad symbol / quantity / price | Validation error with clear message |
| Network timeout | `ConnectionError` with suggestion |
| Binance API error (e.g. -2019) | Prints Binance error code and message |
| Missing credentials | Explains `.env` setup |
