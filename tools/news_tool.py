"""
news_tool.py

Fetches recent stock-related news headlines.

This tool focuses on:
- recent developments
- market sentiment
- company announcements
- event-driven catalysts
"""

from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel

from tools.base_models import FlexibleTickerInput
from tools.yahoo_finance_service import YahooFinanceService
from utils.helpers import normalize_ticker


class StockNewsTool(BaseTool):

    # ========================================================
    # TOOL METADATA
    # ========================================================

    name: str = "Stock News Tool"

    description: str = (
        "Fetches recent stock-related news headlines "
        "and publisher information."
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

        news_items = YahooFinanceService.get_news(
            stock
        )

        if not news_items:

            return YahooFinanceService.to_json({
                "ticker": ticker,
                "recent_news": [],
                "message": "No recent news found"
            })

        # ====================================================
        # PARSE NEWS
        # ====================================================

        parsed_news = []

        for item in news_items[:10]:

            # Yahoo structure can vary
            content = item.get(
                "content",
                item
            )

            parsed_news.append({

                "title":
                    (
                        content.get("title")
                        or item.get("title")
                    ),

                "publisher":
                    (
                        content.get(
                            "provider",
                            {}
                        ).get("displayName")
                        or item.get("publisher")
                    ),

                "published_at":
                    (
                        content.get("pubDate")
                        or item.get("providerPublishTime")
                    ),

                "summary":
                    (
                        content.get("summary")
                        or item.get("summary")
                    ),

                "link":
                    (
                        content.get(
                            "canonicalUrl",
                            {}
                        ).get("url")
                        or item.get("link")
                    ),
            })

        # ====================================================
        # FINAL RESPONSE
        # ====================================================

        result = {
            "ticker": ticker,

            "recent_news":
                parsed_news,

            "news_count":
                len(parsed_news),

            "data_source":
                "Yahoo Finance News"
        }

        return YahooFinanceService.to_json(
            result
        )


    async def _arun(self, *args, **kwargs):
        raise NotImplementedError()