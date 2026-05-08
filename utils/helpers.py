"""
helpers.py

Common reusable helper utilities for the stock analysis system.

This file contains:
- ticker normalization
- safe division helpers
- percentage conversion helpers
- numeric validation helpers
- dataframe sanitization helpers

These utilities are intentionally generic so they can
be reused across tools, agents, and future services.
"""

from typing import Optional, Any

import numpy as np
import pandas as pd


# ============================================================
# TICKER HELPERS
# ============================================================

def normalize_ticker(
    ticker: Optional[str] = None,
    stock_symbol: Optional[str] = None,
    symbol: Optional[str] = None,
) -> Optional[str]:
    """
    Normalize ticker symbols into Yahoo Finance format.

    Examples:
    ---------
    TCS -> TCS.NS
    NSE:TCS -> TCS.NS
    BSE:500325 -> 500325.BO
    INFY.NS -> INFY.NS

    Parameters:
    -----------
    ticker : Optional[str]
    stock_symbol : Optional[str]
    symbol : Optional[str]

    Returns:
    --------
    Optional[str]
        Normalized Yahoo Finance ticker.
    """

    raw = ticker or stock_symbol or symbol

    if not raw:
        return None

    raw = str(raw).strip().upper()

    # Already normalized
    if raw.endswith(".NS") or raw.endswith(".BO"):
        return raw

    # NSE prefixed
    if raw.startswith("NSE:"):
        return raw.replace("NSE:", "") + ".NS"

    # BSE prefixed
    if raw.startswith("BSE:"):
        return raw.replace("BSE:", "") + ".BO"

    # Default to NSE
    return raw + ".NS"


# ============================================================
# SAFE NUMERIC HELPERS
# ============================================================

def is_valid_number(value: Any) -> bool:
    """
    Check whether value is a valid numeric value.

    Rejects:
    - None
    - NaN
    - Infinite values

    Returns:
    --------
    bool
    """

    if value is None:
        return False

    if isinstance(value, (float, np.floating)):
        if np.isnan(value) or np.isinf(value):
            return False

    return True


def safe_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    """
    Safely convert a value into float.

    Parameters:
    -----------
    value : Any
    default : Optional[float]

    Returns:
    --------
    Optional[float]
    """

    try:
        if not is_valid_number(value):
            return default

        return float(value)

    except Exception:
        return default


def safe_int(value: Any, default: Optional[int] = None) -> Optional[int]:
    """
    Safely convert a value into integer.

    Parameters:
    -----------
    value : Any
    default : Optional[int]

    Returns:
    --------
    Optional[int]
    """

    try:
        if not is_valid_number(value):
            return default

        return int(value)

    except Exception:
        return default


def safe_divide(
    numerator: Any,
    denominator: Any,
    multiplier: float = 1.0,
    precision: int = 2,
) -> Optional[float]:
    """
    Safely divide two numbers.

    Prevents:
    - division by zero
    - NaN propagation
    - invalid numeric conversions

    Parameters:
    -----------
    numerator : Any
    denominator : Any
    multiplier : float
        Useful for percentage calculations.
    precision : int

    Returns:
    --------
    Optional[float]
    """

    try:
        numerator = safe_float(numerator)
        denominator = safe_float(denominator)

        if numerator is None or denominator in [None, 0]:
            return None

        result = (numerator / denominator) * multiplier

        return round(result, precision)

    except Exception:
        return None


# ============================================================
# PERCENTAGE HELPERS
# ============================================================

def to_percentage(
    value: Any,
    precision: int = 2
) -> Optional[float]:
    """
    Convert decimal value into percentage.

    Example:
    --------
    0.25 -> 25.0

    Parameters:
    -----------
    value : Any
    precision : int

    Returns:
    --------
    Optional[float]
    """

    try:
        value = safe_float(value)

        if value is None:
            return None

        return round(value * 100, precision)

    except Exception:
        return None


def percentage_change(
    current_value: Any,
    previous_value: Any,
    precision: int = 2
) -> Optional[float]:
    """
    Calculate percentage change.

    Formula:
    --------
    ((current - previous) / previous) * 100

    Parameters:
    -----------
    current_value : Any
    previous_value : Any

    Returns:
    --------
    Optional[float]
    """

    try:
        current_value = safe_float(current_value)
        previous_value = safe_float(previous_value)

        if current_value is None or previous_value in [None, 0]:
            return None

        result = (
            (current_value - previous_value)
            / previous_value
        ) * 100

        return round(result, precision)

    except Exception:
        return None


# ============================================================
# DATAFRAME HELPERS
# ============================================================

def sanitize_dataframe(df):
    """
    Safely sanitize dataframe for JSON serialization.

    Handles:
    - None
    - invalid objects
    - NaN
    - infinite values
    """

    import pandas as pd
    import numpy as np

    # --------------------------------------------------------
    # Validate dataframe
    # --------------------------------------------------------

    if df is None:
        return pd.DataFrame()

    if not isinstance(df, pd.DataFrame):
        return pd.DataFrame()

    if df.empty:
        return pd.DataFrame()

    # --------------------------------------------------------
    # Replace invalid values
    # --------------------------------------------------------

    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    return df.fillna(0)

def dataframe_to_serializable_dict(df):
    """
    Convert dataframe into JSON-safe dictionary.

    Handles:
    - Timestamp keys
    - NaN
    - infinite values

    Returns:
    --------
    dict
    """

    import pandas as pd
    import numpy as np

    if df is None:
        return {}

    if not isinstance(df, pd.DataFrame):
        return {}

    if df.empty:
        return {}

    # --------------------------------------------------------
    # Clean dataframe
    # --------------------------------------------------------

    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    df = df.fillna(0)

    # --------------------------------------------------------
    # Convert Timestamp columns to string
    # --------------------------------------------------------

    df.columns = [
        str(col)
        for col in df.columns
    ]

    # --------------------------------------------------------
    # Convert index to string
    # --------------------------------------------------------

    df.index = [
        str(idx)
        for idx in df.index
    ]

    return df.to_dict()

def latest_column(df: pd.DataFrame) -> Optional[pd.Series]:
    """
    Return latest column from financial statements.

    Yahoo Finance financial statements are usually:
    columns = years
    rows = metrics

    Latest data is generally the first column.

    Parameters:
    -----------
    df : pd.DataFrame

    Returns:
    --------
    Optional[pd.Series]
    """

    if df is None or df.empty:
        return None

    return df.iloc[:, 0]


# ============================================================
# FINANCIAL HELPERS
# ============================================================

def calculate_book_value_per_share(
    shareholder_equity: Any,
    shares_outstanding: Any
) -> Optional[float]:
    """
    Calculate Book Value Per Share.

    Formula:
    --------
    Shareholder Equity / Shares Outstanding
    """

    return safe_divide(
        shareholder_equity,
        shares_outstanding,
        multiplier=1,
        precision=2
    )


def calculate_net_debt(
    total_debt: Any,
    cash_and_equivalents: Any
) -> Optional[float]:
    """
    Calculate Net Debt.

    Formula:
    --------
    Total Debt - Cash & Cash Equivalents
    """

    total_debt = safe_float(total_debt, 0)
    cash_and_equivalents = safe_float(cash_and_equivalents, 0)

    return round(
        total_debt - cash_and_equivalents,
        2
    )

def clean_info_dict(info: dict) -> dict:
    """
    Remove noisy/unnecessary Yahoo Finance fields.
    """

    remove_keys = [
        "companyOfficers",
        "executiveTeam",
        "fax",
        "phone",
    ]

    for key in remove_keys:
        info.pop(key, None)

    return info


def calculate_working_capital(
    current_assets: Any,
    current_liabilities: Any
) -> Optional[float]:
    """
    Calculate Working Capital.

    Formula:
    --------
    Current Assets - Current Liabilities
    """

    current_assets = safe_float(current_assets)
    current_liabilities = safe_float(current_liabilities)

    if current_assets is None or current_liabilities is None:
        return None

    return round(
        current_assets - current_liabilities,
        2
    )