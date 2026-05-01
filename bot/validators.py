"""
Input validation for trading bot CLI arguments.
Raises ValueError with clear messages on invalid input.
"""

VALID_SIDES = ("BUY", "SELL")
VALID_ORDER_TYPES = ("MARKET", "LIMIT", "STOP_MARKET")


def validate_symbol(symbol: str) -> str:
    """Validate and normalise the trading pair symbol."""
    if not symbol or not symbol.strip():
        raise ValueError("Symbol cannot be empty. Example: BTCUSDT")
    symbol = symbol.strip().upper()
    if len(symbol) < 3:
        raise ValueError(f"Symbol '{symbol}' looks invalid. Example: BTCUSDT")
    return symbol


def validate_side(side: str) -> str:
    """Validate order side."""
    if not side:
        raise ValueError("Side is required.")
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValueError(f"Side must be one of {VALID_SIDES}. Got: '{side}'")
    return side


def validate_order_type(order_type: str) -> str:
    """Validate order type."""
    if not order_type:
        raise ValueError("Order type is required.")
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(f"Order type must be one of {VALID_ORDER_TYPES}. Got: '{order_type}'")
    return order_type


def validate_quantity(quantity: str) -> float:
    """Validate and parse quantity."""
    try:
        qty = float(quantity)
    except (TypeError, ValueError):
        raise ValueError(f"Quantity must be a positive number. Got: '{quantity}'")
    if qty <= 0:
        raise ValueError(f"Quantity must be greater than zero. Got: {qty}")
    return qty


def validate_price(price: str) -> float:
    """Validate and parse price (required for LIMIT orders)."""
    try:
        p = float(price)
    except (TypeError, ValueError):
        raise ValueError(f"Price must be a positive number. Got: '{price}'")
    if p <= 0:
        raise ValueError(f"Price must be greater than zero. Got: {p}")
    return p


def validate_stop_price(stop_price: str) -> float:
    """Validate stop price for stop orders."""
    try:
        sp = float(stop_price)
    except (TypeError, ValueError):
        raise ValueError(f"Stop price must be a positive number. Got: '{stop_price}'")
    if sp <= 0:
        raise ValueError(f"Stop price must be greater than zero. Got: {sp}")
    return sp
