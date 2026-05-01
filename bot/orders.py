"""
Order placement logic for Binance Futures Testnet.
Wraps the BinanceClient with order-specific methods.
"""

import logging
from bot.client import BinanceClient

logger = logging.getLogger(__name__)

ORDER_ENDPOINT = "/fapi/v1/order"


def place_market_order(client: BinanceClient, symbol: str, side: str, quantity: float) -> dict:
    """
    Place a MARKET order on Binance Futures Testnet.

    Args:
        client:   Authenticated BinanceClient instance.
        symbol:   Trading pair, e.g. 'BTCUSDT'.
        side:     'BUY' or 'SELL'.
        quantity: Contract quantity.

    Returns:
        Raw API response dict.
    """
    params = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": quantity,
    }
    logger.info("Placing MARKET order | %s %s qty=%s", side, symbol, quantity)
    return client.post(ORDER_ENDPOINT, params)


def place_limit_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    time_in_force: str = "GTC",
) -> dict:
    """
    Place a LIMIT order on Binance Futures Testnet.

    Args:
        client:        Authenticated BinanceClient instance.
        symbol:        Trading pair, e.g. 'BTCUSDT'.
        side:          'BUY' or 'SELL'.
        quantity:      Contract quantity.
        price:         Limit price.
        time_in_force: 'GTC' (default), 'IOC', or 'FOK'.

    Returns:
        Raw API response dict.
    """
    params = {
        "symbol": symbol,
        "side": side,
        "type": "LIMIT",
        "quantity": quantity,
        "price": price,
        "timeInForce": time_in_force,
    }
    logger.info(
        "Placing LIMIT order | %s %s qty=%s price=%s tif=%s",
        side, symbol, quantity, price, time_in_force,
    )
    return client.post(ORDER_ENDPOINT, params)


def place_stop_market_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    quantity: float,
    stop_price: float,
) -> dict:
    """
    Place a STOP_MARKET (stop-loss/take-profit trigger) order on Binance Futures Testnet.

    Args:
        client:     Authenticated BinanceClient instance.
        symbol:     Trading pair, e.g. 'BTCUSDT'.
        side:       'BUY' or 'SELL'.
        quantity:   Contract quantity.
        stop_price: Price that triggers the market order.

    Returns:
        Raw API response dict.
    """
    params = {
        "symbol": symbol,
        "side": side,
        "type": "STOP_MARKET",
        "quantity": quantity,
        "stopPrice": stop_price,
    }
    logger.info(
        "Placing STOP_MARKET order | %s %s qty=%s stopPrice=%s",
        side, symbol, quantity, stop_price,
    )
    return client.post(ORDER_ENDPOINT, params)
