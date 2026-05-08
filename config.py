"""
config.py

Centralized configuration module for the
AI Stock Analysis System.

Purpose:
--------
This file manages:
- environment variables
- API keys
- model configuration
- logging configuration
- system constants
- runtime behavior

Benefits:
---------
- Single source of truth
- Cleaner imports
- Easier production deployment
- Easier environment switching
- Better maintainability
"""

# ============================================================
# STANDARD LIBRARIES
# ============================================================

import os
import warnings

# ============================================================
# THIRD-PARTY LIBRARIES
# ============================================================

import truststore
from dotenv import load_dotenv

# ============================================================
# ENVIRONMENT INITIALIZATION
# ============================================================

# Load environment variables from .env file
load_dotenv()

# Inject SSL trust store
# Helps avoid SSL certificate issues in notebooks/Windows
truststore.inject_into_ssl()

# Suppress warnings
warnings.filterwarnings("ignore")


# ============================================================
# APPLICATION INFO
# ============================================================

APP_NAME = "AI Stock Analysis System"

APP_VERSION = "1.0.0"

ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development"
)


# ============================================================
# LLM CONFIGURATION
# ============================================================

# OpenAI-compatible endpoint
BASE_URL = os.getenv("URL")

# API key
API_KEY = os.getenv("KEY")

# Model name
MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gpt-4o-mini"
)

# LLM temperature
TEMPERATURE = float(
    os.getenv("TEMPERATURE", 0)
)

# Maximum retries
MAX_RETRIES = int(
    os.getenv("MAX_RETRIES", 3)
)

# Request timeout (seconds)
REQUEST_TIMEOUT = int(
    os.getenv("REQUEST_TIMEOUT", 120)
)


# ============================================================
# STOCK ANALYSIS SETTINGS
# ============================================================

# Default historical period
DEFAULT_HISTORY_PERIOD = "6mo"

# RSI calculation window
RSI_PERIOD = 14

# Moving average windows
SMA_SHORT_WINDOW = 20

SMA_LONG_WINDOW = 50

# Long-term MA
SMA_200_WINDOW = 200

# Minimum historical rows required
MINIMUM_HISTORY_ROWS = 60


# ============================================================
# CREWAI SETTINGS
# ============================================================

# Verbose mode
CREW_VERBOSE = True

# Agent verbosity
AGENT_VERBOSE = True

# Task verbosity
TASK_VERBOSE = True

# Default maximum iterations
DEFAULT_AGENT_MAX_ITER = 5

# Allow delegation globally
ALLOW_DELEGATION = False


# ============================================================
# CACHE SETTINGS
# ============================================================

ENABLE_CACHE = True

CACHE_EXPIRY_SECONDS = 300


# ============================================================
# LOGGING SETTINGS
# ============================================================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)

LOG_DIRECTORY = "logs"

LOG_FILE_NAME = "stock_analysis.log"


# ============================================================
# RATE LIMITING
# ============================================================

ENABLE_RATE_LIMITING = False

MAX_REQUESTS_PER_MINUTE = 60


# ============================================================
# NEWS SETTINGS
# ============================================================

MAX_NEWS_HEADLINES = 10


# ============================================================
# RISK SCORING THRESHOLDS
# ============================================================

HIGH_DEBT_TO_EQUITY_THRESHOLD = 2.0

LOW_CURRENT_RATIO_THRESHOLD = 1.0

HIGH_PE_THRESHOLD = 50

HIGH_RSI_THRESHOLD = 70

LOW_RSI_THRESHOLD = 30


# ============================================================
# JSON OUTPUT SETTINGS
# ============================================================

ENABLE_PRETTY_JSON = True

JSON_INDENT = 2


# ============================================================
# FEATURE FLAGS
# ============================================================

ENABLE_MACRO_ANALYSIS = True

ENABLE_PORTFOLIO_ANALYSIS = True

ENABLE_NEWS_ANALYSIS = True

ENABLE_BALANCE_SHEET_ANALYSIS = True

ENABLE_ADVANCED_METRICS = True


# ============================================================
# DATA SOURCE SETTINGS
# ============================================================

PRIMARY_DATA_SOURCE = "Yahoo Finance"

SECONDARY_DATA_SOURCE = None


# ============================================================
# VALIDATION
# ============================================================

if not API_KEY:
    raise ValueError(
        "Missing API KEY in environment variables."
    )

if not BASE_URL:
    raise ValueError(
        "Missing BASE URL in environment variables."
    )


# ============================================================
# OPTIONAL FUTURE SETTINGS
# ============================================================

"""
Future Expansion Ideas
----------------------

You can later add:

- Redis configuration
- PostgreSQL configuration
- Vector database settings
- LangSmith tracing
- LangFuse observability
- Azure/OpenAI switching
- Real-time websocket feeds
- NSE/BSE APIs
- Async execution configs
- Portfolio tracking configs
- Backtesting configs
- Alerting configs
"""