"""
Logging configuration for the trading bot.
Sets up both a file handler (structured) and a console handler (human-readable).
"""

import logging
import logging.handlers
import os
from datetime import datetime

LOG_DIR = "logs"
LOG_LEVEL = logging.INFO


def setup_logging(log_dir: str = LOG_DIR) -> None:
    """
    Configure the root logger with:
    - A rotating file handler that writes JSON-like structured lines.
    - A console handler that prints clean, human-readable output.

    Args:
        log_dir: Directory where log files are stored (created if absent).
    """
    os.makedirs(log_dir, exist_ok=True)

    log_filename = os.path.join(log_dir, f"trading_bot_{datetime.now():%Y%m%d}.log")

    file_fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    console_fmt = logging.Formatter(
        fmt="%(levelname)-8s %(message)s",
    )

    file_handler = logging.handlers.RotatingFileHandler(
        log_filename,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(file_fmt)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(console_fmt)

    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)

    if not root_logger.handlers:
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
