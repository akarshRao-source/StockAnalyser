"""
fundamentals_tool.py

Fetches and analyzes company fundamental data.

This tool focuses on:
- valuation metrics
- profitability
- growth
- analyst sentiment
- balance sheet strength
- dividend profile
- company overview

Data Source:
------------
Yahoo Finance via yfinance
"""

from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel

from tools.base_models import FlexibleTickerInput
from tools.yahoo_finance_service import YahooFinanceService
from utils.helpers import (
    normalize_ticker,
    safe_float,
    safe_int,
    to_percentage,
)


class FundamentalDataTool(BaseTool):

    # ========================================================
    # TOOL METADATA
    # ========================================================

    name: str = "Fundamental Data Tool"

    description: str = (
        "Fetches company fundamentals including "
        "valuation, profitability, growth metrics, "
        "analyst sentiment, dividend profile, "
        "and financial health."
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

        info = YahooFinanceService.get_info(
            stock
        )

        if not info:

            return YahooFinanceService.to_json({
                "ticker": ticker,
                "error": "Fundamental data unavailable"
            })

        # ====================================================
        # COMPANY PROFILE
        # ====================================================

        company_profile = {
            "company_name":
                info.get("longName"),

            "sector":
                info.get("sector"),

            "industry":
                info.get("industry"),

            "website":
                info.get("website"),

            "country":
                info.get("country"),

            "city":
                info.get("city"),

            "employee_count":
                safe_int(info.get("fullTimeEmployees")),

            "business_summary":
                info.get("longBusinessSummary"),
        }

        # ====================================================
        # VALUATION METRICS
        # ====================================================

        valuation_metrics = {
            "market_cap":
                safe_int(info.get("marketCap")),

            "enterprise_value":
                safe_int(info.get("enterpriseValue")),

            "trailing_pe":
                safe_float(info.get("trailingPE")),

            "forward_pe":
                safe_float(info.get("forwardPE")),

            "peg_ratio":
                safe_float(info.get("pegRatio")),

            "price_to_book":
                safe_float(info.get("priceToBook")),

            "price_to_sales":
                safe_float(info.get("priceToSalesTrailing12Months")),

            "enterprise_to_revenue":
                safe_float(info.get("enterpriseToRevenue")),

            "enterprise_to_ebitda":
                safe_float(info.get("enterpriseToEbitda")),
        }

        # ====================================================
        # PROFITABILITY METRICS
        # ====================================================

        profitability_metrics = {
            "profit_margin_percent":
                to_percentage(info.get("profitMargins")),

            "gross_margin_percent":
                to_percentage(info.get("grossMargins")),

            "operating_margin_percent":
                to_percentage(info.get("operatingMargins")),

            "ebitda_margin_percent":
                to_percentage(info.get("ebitdaMargins")),

            "return_on_equity_percent":
                to_percentage(info.get("returnOnEquity")),

            "return_on_assets_percent":
                to_percentage(info.get("returnOnAssets")),

            "earnings_per_share":
                safe_float(info.get("trailingEps")),

            "forward_eps":
                safe_float(info.get("forwardEps")),
        }

        # ====================================================
        # GROWTH METRICS
        # ====================================================

        growth_metrics = {
            "revenue_growth_percent":
                to_percentage(info.get("revenueGrowth")),

            "earnings_growth_percent":
                to_percentage(info.get("earningsGrowth")),

            "quarterly_earnings_growth_percent":
                to_percentage(info.get("earningsQuarterlyGrowth")),

            "revenue_per_share":
                safe_float(info.get("revenuePerShare")),
        }

        # ====================================================
        # FINANCIAL HEALTH
        # ====================================================

        financial_health = {
            "total_cash":
                safe_int(info.get("totalCash")),

            "total_debt":
                safe_int(info.get("totalDebt")),

            "debt_to_equity":
                safe_float(info.get("debtToEquity")),

            "current_ratio":
                safe_float(info.get("currentRatio")),

            "quick_ratio":
                safe_float(info.get("quickRatio")),

            "book_value":
                safe_float(info.get("bookValue")),

            "free_cashflow":
                safe_int(info.get("freeCashflow")),

            "operating_cashflow":
                safe_int(info.get("operatingCashflow")),
        }

        # ====================================================
        # MARKET DATA
        # ====================================================

        market_data = {
            "beta":
                safe_float(info.get("beta")),

            "fifty_two_week_high":
                safe_float(info.get("fiftyTwoWeekHigh")),

            "fifty_two_week_low":
                safe_float(info.get("fiftyTwoWeekLow")),

            "fifty_day_average":
                safe_float(info.get("fiftyDayAverage")),

            "two_hundred_day_average":
                safe_float(info.get("twoHundredDayAverage")),
        }

        # ====================================================
        # DIVIDEND PROFILE
        # ====================================================

        dividend_profile = {
            "dividend_yield_percent":
                to_percentage(info.get("dividendYield")),

            "dividend_rate":
                safe_float(info.get("dividendRate")),

            "payout_ratio_percent":
                to_percentage(info.get("payoutRatio")),
        }

        # ====================================================
        # ANALYST SENTIMENT
        # ====================================================

        analyst_sentiment = {
            "recommendation":
                info.get("recommendationKey"),

            "recommendation_mean":
                safe_float(info.get("recommendationMean")),

            "number_of_analyst_opinions":
                safe_int(info.get("numberOfAnalystOpinions")),

            "target_mean_price":
                safe_float(info.get("targetMeanPrice")),

            "target_high_price":
                safe_float(info.get("targetHighPrice")),

            "target_low_price":
                safe_float(info.get("targetLowPrice")),
        }

        # ====================================================
        # OWNERSHIP
        # ====================================================

        ownership = {
            "institutional_holding_percent":
                to_percentage(info.get("heldPercentInstitutions")),

            "insider_holding_percent":
                to_percentage(info.get("heldPercentInsiders")),
        }

        # ====================================================
        # FINAL RESPONSE
        # ====================================================

        result = {
            "ticker": ticker,

            "company_profile":
                company_profile,

            "valuation_metrics":
                valuation_metrics,

            "profitability_metrics":
                profitability_metrics,

            "growth_metrics":
                growth_metrics,

            "financial_health":
                financial_health,

            "market_data":
                market_data,

            "dividend_profile":
                dividend_profile,

            "analyst_sentiment":
                analyst_sentiment,

            "ownership":
                ownership,

            "data_source":
                "Yahoo Finance via yfinance"
        }

        return YahooFinanceService.to_json(result)
    async def _arun(self, *args, **kwargs):
        raise NotImplementedError()