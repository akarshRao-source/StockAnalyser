"""
balance_sheet_tool.py

Fetches historical:
- balance sheet
- income statement
- cashflow statement

Used for:
- multi-year trend analysis
- liquidity analysis
- leverage analysis
- cashflow analysis
"""

from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel

from tools.base_models import FlexibleTickerInput
from tools.yahoo_finance_service import YahooFinanceService
from utils.helpers import (
    dataframe_to_serializable_dict,
    normalize_ticker,
    sanitize_dataframe,
)


class BalanceSheetTool(BaseTool):

    # ========================================================
    # TOOL METADATA
    # ========================================================

    name: str = "Balance Sheet Analysis Tool"

    description: str = (
        "Fetches historical balance sheet, "
        "income statement, and cashflow data."
    )

    args_schema: Type[BaseModel] = FlexibleTickerInput

    # ========================================================
    # MAIN TOOL EXECUTION
    # ========================================================

    def _run(
        self,
        ticker=None,
        stock_symbol=None,
        symbol=None
    ) -> str:



        # ----------------------------------------------------
        # Normalize ticker
        # ----------------------------------------------------

        ticker = normalize_ticker(
            ticker,
            stock_symbol,
            symbol
        )

        if not ticker:

            return YahooFinanceService.to_json({
                "error": "Missing ticker"
            })

        # ----------------------------------------------------
        # Fetch stock object
        # ----------------------------------------------------

        stock = YahooFinanceService.get_stock(
            ticker
        )

        # ====================================================
        # FETCH FINANCIAL STATEMENTS
        # ====================================================

        try:

            balance_sheet = (
                YahooFinanceService.get_balance_sheet(stock)
            )

            financials = (
                YahooFinanceService.get_financials(stock)
            )

            cashflow = (
                YahooFinanceService.get_cashflow(stock)
            )

        except Exception as e:

            return YahooFinanceService.to_json({
                "ticker": ticker,
                "error": f"Failed fetching financial statements: {str(e)}"
            })

        # ====================================================
        # SANITIZE DATAFRAMES
        # ====================================================

        balance_sheet = sanitize_dataframe(
            balance_sheet
        )

        financials = sanitize_dataframe(
            financials
        )

        cashflow = sanitize_dataframe(
            cashflow
        )

        # ====================================================
        # FINAL RESPONSE
        # ====================================================

        result = {
            "ticker": ticker,

            "balance_sheet":
                dataframe_to_serializable_dict(
                    balance_sheet
                ),

            "financials":
                dataframe_to_serializable_dict(
                    financials
                ),

            "cashflow":
                dataframe_to_serializable_dict(
                    cashflow
                ),

            "data_source":
                "Yahoo Finance Financial Statements"
        }

        return YahooFinanceService.to_json(
            result
        )

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError()