"""
stock_symbol_tool.py

Resolves stock/company names into Yahoo Finance ticker symbols.
"""

import json
from typing import Type

import yfinance as yf
from crewai.tools import BaseTool
from pydantic import BaseModel

from tools.base_models import StockNameInput


class StockSymbolResolverTool(BaseTool):

    name: str = "Stock Symbol Resolver Tool"

    description: str = (
        "Resolves company names into Yahoo Finance "
        "ticker symbols."
    )

    args_schema: Type[BaseModel] = StockNameInput

    def _run(self, stock_name: str) -> str:

        try:

            search = yf.Search(
                stock_name,
                max_results=10
            )

            if not search.quotes:

                return json.dumps({
                    "error": f"No matches found for {stock_name}"
                })

            # Prefer NSE listing
            for result in search.quotes:

                symbol = result.get("symbol", "")

                if symbol.endswith(".NS"):

                    return json.dumps({
                        "stock_name": stock_name,
                        "ticker": symbol,
                        "exchange": "NSE"
                    })

            # Prefer BSE if NSE unavailable
            for result in search.quotes:

                symbol = result.get("symbol", "")

                if symbol.endswith(".BO"):

                    return json.dumps({
                        "stock_name": stock_name,
                        "ticker": symbol,
                        "exchange": "BSE"
                    })

            # Final fallback
            first = search.quotes[0]

            return json.dumps({
                "stock_name": stock_name,
                "ticker": first.get("symbol"),
                "exchange": first.get("exchange")
            })

        except Exception as e:

            return json.dumps({
                "stock_name": stock_name,
                "error": str(e)
            })

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError()