# utils/logger.py
import os
import sys
import logging
import datetime


def setup_logger(name=None, log_dir="logs"):
    """Configure and return a logger."""
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(
        log_dir, f"backtest_{datetime.datetime.now():%Y%m%d_%H%M%S}.log"
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, mode="w", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    logger = logging.getLogger(name)
    logger.info(f"Logger initialized. Logs will be saved to: {log_file}")
    return logger
