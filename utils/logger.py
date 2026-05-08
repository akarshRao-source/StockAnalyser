"""
logger.py

Centralized logging configuration for the stock analysis system.

Benefits:
---------
- Consistent log formatting
- Easier debugging
- File logging support
- Production-ready logging structure
"""

import logging
import os
from logging.handlers import RotatingFileHandler


# ============================================================
# LOG DIRECTORY
# ============================================================

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)


# ============================================================
# LOG FORMAT
# ============================================================

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ============================================================
# LOGGER CREATION
# ============================================================

def get_logger(name: str) -> logging.Logger:
    """
    Create and configure logger.

    Parameters:
    -----------
    name : str
        Usually __name__

    Returns:
    --------
    logging.Logger
    """

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        LOG_FORMAT,
        datefmt=DATE_FORMAT
    )

    # ========================================================
    # Console Handler
    # ========================================================

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # ========================================================
    # Rotating File Handler
    # ========================================================

    file_handler = RotatingFileHandler(
        filename=os.path.join(LOG_DIR, "stock_analysis.log"),
        maxBytes=5 * 1024 * 1024,   # 5 MB
        backupCount=5
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.propagate = False

    return logger