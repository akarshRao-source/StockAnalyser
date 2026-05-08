"""
financial_metrics_tool.py

Calculates advanced financial ratios and metrics.
"""

from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel

from tools.base_models import FlexibleTickerInput
from tools.yahoo_finance_service import YahooFinanceService
from utils.helpers import (
    calculate_net_debt,
    calculate_working_capital,
    latest_column,
    normalize_ticker,
    safe_divide,
)


class FinancialMetricsCalculatorTool(BaseTool):

    name: str = "Financial Metrics Calculator Tool"

    description: str = (
        "Calculates advanced financial metrics "
        "using company financial statements."
    )

    args_schema: Type[BaseModel] = FlexibleTickerInput

    def _run(
        self,
        ticker=None,
        stock_symbol=None,
        symbol=None
    ) -> str:

        ticker = normalize_ticker(
            ticker,
            stock_symbol,
            symbol
        )

        stock = YahooFinanceService.get_stock(
            ticker
        )

        balance_sheet = YahooFinanceService.get_balance_sheet(
            stock
        )

        financials = YahooFinanceService.get_financials(
            stock
        )

        if balance_sheet.empty or financials.empty:

            return YahooFinanceService.to_json({
                "ticker": ticker,
                "error": "Financial statements unavailable"
            })

        bs = latest_column(balance_sheet)

        fin = latest_column(financials)

        total_assets = bs.get("Total Assets")

        current_assets = bs.get("Current Assets")

        current_liabilities = bs.get(
            "Current Liabilities"
        )

        inventory = bs.get("Inventory")

        total_debt = bs.get("Total Debt")

        shareholder_equity = bs.get(
            "Stockholders Equity"
        )

        cash = bs.get(
            "Cash And Cash Equivalents"
        )

        net_income = fin.get("Net Income")

        total_revenue = fin.get(
            "Total Revenue"
        )

        result = {
            "ticker": ticker,

            "return_on_equity_percent":
                safe_divide(
                    net_income,
                    shareholder_equity,
                    multiplier=100
                ),

            "return_on_assets_percent":
                safe_divide(
                    net_income,
                    total_assets,
                    multiplier=100
                ),

            "current_ratio":
                safe_divide(
                    current_assets,
                    current_liabilities
                ),

            "quick_ratio":
                safe_divide(
                    (
                        current_assets - inventory
                        if inventory is not None
                        else None
                    ),
                    current_liabilities
                ),

            "debt_to_assets_ratio":
                safe_divide(
                    total_debt,
                    total_assets
                ),

            "asset_turnover_ratio":
                safe_divide(
                    total_revenue,
                    total_assets
                ),

            "working_capital":
                calculate_working_capital(
                    current_assets,
                    current_liabilities
                ),

            "net_debt":
                calculate_net_debt(
                    total_debt,
                    cash
                ),
        }

        return YahooFinanceService.to_json(result)

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError()