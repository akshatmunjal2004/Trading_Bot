"""
Binance Futures Testnet API client wrapper.
Handles authentication, request signing, and HTTP communication.
"""

import hashlib
import hmac
import time
import logging
from urllib.parse import urlencode

import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://testnet.binancefuture.com"


class BinanceClient:
    """Low-level authenticated client for Binance Futures Testnet REST API."""

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _sign(self, params: dict) -> str:
        """Generate HMAC-SHA256 signature for the given parameters."""
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return signature

    def _get_timestamp(self) -> int:
        return int(time.time() * 1000)

    def post(self, endpoint: str, params: dict) -> dict:
        """Send an authenticated POST request to the Binance Futures API."""
        params["timestamp"] = self._get_timestamp()
        params["signature"] = self._sign(params)

        url = f"{BASE_URL}{endpoint}"
        logger.info("POST %s | params: %s", url, {k: v for k, v in params.items() if k != "signature"})

        try:
            response = self.session.post(url, params=params, timeout=10)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.error("Request timed out: %s", url)
            raise ConnectionError("Request timed out. Check your network connection.")
        except requests.exceptions.ConnectionError as e:
            logger.error("Network error: %s", e)
            raise ConnectionError(f"Network error: {e}")
        except requests.exceptions.HTTPError as e:
            error_data = {}
            try:
                error_data = response.json()
            except Exception:
                pass
            logger.error("HTTP %s error: %s | body: %s", response.status_code, url, error_data)
            code = error_data.get("code", "unknown")
            msg = error_data.get("msg", str(e))
            raise RuntimeError(f"Binance API error [{code}]: {msg}")

        data = response.json()
        logger.info("Response: %s", data)
        return data

    def get(self, endpoint: str, params: dict = None) -> dict:
        """Send an authenticated GET request to the Binance Futures API."""
        params = params or {}
        params["timestamp"] = self._get_timestamp()
        params["signature"] = self._sign(params)

        url = f"{BASE_URL}{endpoint}"
        logger.info("GET %s | params: %s", url, {k: v for k, v in params.items() if k != "signature"})

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.error("Request timed out: %s", url)
            raise ConnectionError("Request timed out.")
        except requests.exceptions.ConnectionError as e:
            logger.error("Network error: %s", e)
            raise ConnectionError(f"Network error: {e}")
        except requests.exceptions.HTTPError as e:
            error_data = {}
            try:
                error_data = response.json()
            except Exception:
                pass
            logger.error("HTTP error: %s | body: %s", url, error_data)
            code = error_data.get("code", "unknown")
            msg = error_data.get("msg", str(e))
            raise RuntimeError(f"Binance API error [{code}]: {msg}")

        data = response.json()
        logger.info("Response: %s", data)
        return data
