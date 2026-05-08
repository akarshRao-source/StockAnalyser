"""
price_tool.py

Fetches stock market price data and volume statistics.
"""

from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel

from tools.base_models import FlexibleTickerInput
from tools.yahoo_finance_service import YahooFinanceService
from utils.helpers import (
    normalize_ticker,
    percentage_change,
    safe_float,
    safe_int,
)


class StockPriceDataTool(BaseTool):

    name: str = "Stock Price Data Tool"

    description: str = (
        "Fetches recent stock price, volume, "
        "and return statistics."
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

        if not ticker:

            return YahooFinanceService.to_json({
                "error": "Missing ticker"
            })

        stock = YahooFinanceService.get_stock(ticker)

        hist = YahooFinanceService.get_history(
            stock,
            period="6mo"
        )

        if hist.empty:

            return YahooFinanceService.to_json({
                "ticker": ticker,
                "error": "No historical data found"
            })

        latest = hist.iloc[-1]
        first = hist.iloc[0]

        current_price = safe_float(
            latest["Close"]
        )

        start_price = safe_float(
            first["Close"]
        )

        latest_volume = safe_int(
            latest["Volume"]
        )

        avg_volume = safe_int(
            hist["Volume"].tail(20).mean()
        )

        result = {
            "ticker": ticker,

            "current_price": current_price,

            "six_month_return_percent":
                percentage_change(
                    current_price,
                    start_price
                ),

            "six_month_high":
                safe_float(hist["High"].max()),

            "six_month_low":
                safe_float(hist["Low"].min()),

            "latest_volume":
                latest_volume,

            "average_20_day_volume":
                avg_volume,

            "volume_vs_20_day_average":
                round(
                    latest_volume / avg_volume,
                    2
                ) if avg_volume else None,

            "data_source":
                "Yahoo Finance via yfinance"
        }

        return YahooFinanceService.to_json(result)

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError()