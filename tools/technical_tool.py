"""
technical_tool.py

Performs technical analysis calculations.

Includes:
- moving averages
- RSI
- momentum
- trend signals
"""

from typing import Type

import numpy as np
from crewai.tools import BaseTool
from pydantic import BaseModel

from tools.base_models import FlexibleTickerInput
from tools.yahoo_finance_service import YahooFinanceService
from utils.helpers import (
    normalize_ticker,
    percentage_change,
    safe_float,
)


class TechnicalAnalysisTool(BaseTool):

    name: str = "Technical Analysis Tool"

    description: str = (
        "Calculates RSI, moving averages, "
        "returns, and technical trend signals."
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

        hist = YahooFinanceService.get_history(
            stock,
            period="6mo"
        )

        if hist.empty or len(hist) < 60:

            return YahooFinanceService.to_json({
                "ticker": ticker,
                "error": "Insufficient data"
            })

        close = hist["Close"]

        # ====================================================
        # MOVING AVERAGES
        # ====================================================

        sma_20 = close.rolling(20).mean().iloc[-1]

        sma_50 = close.rolling(50).mean().iloc[-1]

        latest_close = close.iloc[-1]

        # ====================================================
        # RSI
        # ====================================================

        delta = close.diff()

        gain = (
            delta.where(delta > 0, 0)
            .rolling(14)
            .mean()
        )

        loss = (
            (-delta.where(delta < 0, 0))
            .rolling(14)
            .mean()
        )

        rs = gain / loss.replace(0, np.nan)

        rsi = 100 - (100 / (1 + rs))

        latest_rsi = rsi.iloc[-1]

        # ====================================================
        # RETURNS
        # ====================================================

        one_month_return = percentage_change(
            close.iloc[-1],
            close.iloc[-22]
        )

        three_month_return = percentage_change(
            close.iloc[-1],
            close.iloc[-63]
        )

        # ====================================================
        # TREND SIGNAL
        # ====================================================

        if (
            latest_close > sma_20 > sma_50
            and latest_rsi < 70
        ):

            trend_signal = "Bullish"

        elif latest_close < sma_20 < sma_50:

            trend_signal = "Bearish"

        else:

            trend_signal = "Neutral"

        result = {
            "ticker": ticker,

            "latest_close":
                safe_float(latest_close),

            "sma_20":
                safe_float(sma_20),

            "sma_50":
                safe_float(sma_50),

            "rsi_14":
                safe_float(latest_rsi),

            "one_month_return_percent":
                one_month_return,

            "three_month_return_percent":
                three_month_return,

            "technical_signal":
                trend_signal,
        }

        return YahooFinanceService.to_json(result)

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError()