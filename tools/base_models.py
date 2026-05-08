"""
base_models.py

Centralized Pydantic input schemas used across tools.

Keeping schemas centralized:
- avoids duplication
- improves maintainability
- standardizes validation
"""

from typing import Optional

from pydantic import BaseModel, Field


# ============================================================
# FLEXIBLE TICKER INPUT
# ============================================================

class FlexibleTickerInput(BaseModel):
    """
    Flexible ticker schema.

    Allows multiple input names so CrewAI agents
    can pass values using different key names.
    """

    ticker: Optional[str] = Field(
        default=None,
        description="Yahoo Finance ticker symbol"
    )

    stock_symbol: Optional[str] = Field(
        default=None,
        description="Alternative ticker field"
    )

    symbol: Optional[str] = Field(
        default=None,
        description="Alternative ticker field"
    )


# ============================================================
# STOCK NAME INPUT
# ============================================================

class StockNameInput(BaseModel):
    """
    Used for stock/company name resolution.
    """

    stock_name: str = Field(
        ...,
        description="Company or stock name"
    )
    async def _arun(self, *args, **kwargs):
        raise NotImplementedError()