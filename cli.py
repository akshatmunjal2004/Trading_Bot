"""
CLI entry point for the Binance Futures Testnet trading bot.

Usage examples:
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
  python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3200
  python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 60000
"""

import argparse
import os
import sys

from dotenv import load_dotenv

from bot.client import BinanceClient
from bot.logging_config import setup_logging
from bot.orders import place_limit_order, place_market_order, place_stop_market_order
from bot.validators import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_stop_price,
    validate_symbol,
)

load_dotenv()


# ─── Output helpers ──────────────────────────────────────────────────────────

def print_section(title: str) -> None:
    print(f"\n{'─' * 50}")
    print(f"  {title}")
    print(f"{'─' * 50}")


def print_request_summary(symbol, side, order_type, quantity, price=None, stop_price=None) -> None:
    print_section("Order Request Summary")
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Type       : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price is not None:
        print(f"  Price      : {price}")
    if stop_price is not None:
        print(f"  Stop Price : {stop_price}")


def print_order_response(response: dict) -> None:
    print_section("Order Response")
    print(f"  Order ID   : {response.get('orderId', 'N/A')}")
    print(f"  Status     : {response.get('status', 'N/A')}")
    print(f"  Symbol     : {response.get('symbol', 'N/A')}")
    print(f"  Side       : {response.get('side', 'N/A')}")
    print(f"  Type       : {response.get('type', 'N/A')}")
    print(f"  Orig Qty   : {response.get('origQty', 'N/A')}")
    print(f"  Exec Qty   : {response.get('executedQty', 'N/A')}")
    avg_price = response.get("avgPrice") or response.get("price") or "N/A"
    print(f"  Avg Price  : {avg_price}")
    print(f"  Time       : {response.get('updateTime', 'N/A')}")


# ─── Argument parsing ────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Place orders on Binance Futures Testnet (USDT-M)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--symbol",     required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side",       required=True, help="BUY or SELL")
    parser.add_argument("--type",       required=True, dest="order_type", help="MARKET, LIMIT, or STOP_MARKET")
    parser.add_argument("--quantity",   required=True, help="Contract quantity")
    parser.add_argument("--price",      default=None,  help="Limit price (required for LIMIT orders)")
    parser.add_argument("--stop-price", default=None,  dest="stop_price",
                        help="Stop trigger price (required for STOP_MARKET orders)")
    parser.add_argument("--tif",        default="GTC", help="Time-in-force for LIMIT orders: GTC/IOC/FOK (default GTC)")
    return parser


# ─── Main ────────────────────────────────────────────────────────────────────

def main() -> None:
    setup_logging()
    parser = build_parser()
    args = parser.parse_args()

    # --- Validate inputs -----------------------------------------------------
    try:
        symbol     = validate_symbol(args.symbol)
        side       = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity   = validate_quantity(args.quantity)

        price = None
        if order_type == "LIMIT":
            if args.price is None:
                parser.error("--price is required for LIMIT orders.")
            price = validate_price(args.price)

        stop_price = None
        if order_type == "STOP_MARKET":
            if args.stop_price is None:
                parser.error("--stop-price is required for STOP_MARKET orders.")
            stop_price = validate_stop_price(args.stop_price)

    except ValueError as e:
        print(f"\n[Validation Error] {e}", file=sys.stderr)
        sys.exit(1)

    # --- Load credentials ----------------------------------------------------
    api_key    = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()

    if not api_key or not api_secret:
        print(
            "\n[Config Error] BINANCE_API_KEY and BINANCE_API_SECRET must be set.\n"
            "Copy .env.example to .env and fill in your testnet credentials.",
            file=sys.stderr,
        )
        sys.exit(1)

    # --- Print request summary -----------------------------------------------
    print_request_summary(symbol, side, order_type, quantity, price, stop_price)

    # --- Place order ---------------------------------------------------------
    client = BinanceClient(api_key=api_key, api_secret=api_secret)

    try:
        if order_type == "MARKET":
            response = place_market_order(client, symbol, side, quantity)

        elif order_type == "LIMIT":
            response = place_limit_order(client, symbol, side, quantity, price, time_in_force=args.tif)

        elif order_type == "STOP_MARKET":
            response = place_stop_market_order(client, symbol, side, quantity, stop_price)

    except (ConnectionError, RuntimeError) as e:
        print(f"\n[Order Failed] {e}", file=sys.stderr)
        sys.exit(1)

    # --- Print response ------------------------------------------------------
    print_order_response(response)
    print_section("Result")
    print("  Order placed successfully!")
    print()


if __name__ == "__main__":
    main()
