"""
yahoo_finance_service.py

Centralized Yahoo Finance service layer.

Purpose:
--------
- reduce duplicate logic
- standardize error handling
- simplify retries/caching later
- centralize yfinance interactions
"""

import json
from tenacity import retry, stop_after_attempt, wait_fixed
import pandas as pd
import yfinance as yf


class YahooFinanceService:
    """
    Wrapper around yfinance.
    """

    # ========================================================
    # TICKER OBJECT
    # ========================================================

    @staticmethod
    @retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    reraise=True
)
    def get_stock(ticker: str):
        """
        Return yfinance Ticker object.
        """

        return yf.Ticker(ticker)

    # ========================================================
    # STOCK INFO
    # ========================================================

    @staticmethod
    @retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    reraise=True
)
    def get_info(stock) -> dict:
        """
        Safely fetch stock info.
        """

        try:
            return stock.info or {}

        except Exception:
            return {}

    # ========================================================
    # PRICE HISTORY
    # ========================================================

    @staticmethod
    @retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    reraise=True
)
    def get_history(
        stock,
        period: str = "6mo"
    ) -> pd.DataFrame:
        """
        Safely fetch historical data.
        """

        try:
            return stock.history(
                period=period,
                auto_adjust=False
            )

        except Exception:
            return pd.DataFrame()

    # ========================================================
    # NEWS
    # ========================================================

    @staticmethod
    @retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    reraise=True
)
    def get_news(stock):
        """
        Safely fetch stock news.
        """

        try:
            return stock.news or []

        except Exception:
            return []

    # ========================================================
    # BALANCE SHEET
    # ========================================================

    @staticmethod
    @retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    reraise=True
)
    def get_balance_sheet(stock):
        """
        Safely fetch balance sheet.
        """
        result = stock.balance_sheet

        if result is None:
            return pd.DataFrame()

        if not isinstance(result, pd.DataFrame):
            return pd.DataFrame()

        return result

        try:
            return stock.balance_sheet

        except Exception:
            return pd.DataFrame()

    # ========================================================
    # FINANCIALS
    # ========================================================

    @staticmethod
    @retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    reraise=True
)
    def get_financials(stock):
        """
        Safely fetch income statement.
        """

        try:
            return stock.financials

        except Exception:
            return pd.DataFrame()

    # ========================================================
    # CASHFLOW
    # ========================================================

    @staticmethod
    @retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    reraise=True
)
    def get_cashflow(stock):
        """
        Safely fetch cashflow statement.
        """

        try:
            return stock.cashflow

        except Exception:
            return pd.DataFrame()

    # ========================================================
    # JSON RESPONSE
    # ========================================================

    @staticmethod
    @retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    reraise=True
)
    def to_json(data: dict) -> str:
        """
        Safely serialize data into JSON.
        """

        return json.dumps(
            data,
            default=str
        )

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError()