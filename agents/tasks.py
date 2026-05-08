"""
tasks.py

Defines all CrewAI tasks for the stock analysis workflow.

This file contains ONLY:
- task descriptions
- expected outputs
- task orchestration

No agent creation logic should exist here.
"""

from crewai import Task


# ============================================================
# STOCK IDENTIFICATION TASK
# ============================================================

def create_stock_identification_task(agent) -> Task:
    """
    Resolve company name into Yahoo Finance ticker.
    """

    return Task(
        description="""
        The user provided stock name: "{stock_name}"

        Identify:
        - correct company
        - ticker symbol
        - exchange
        - sector
        - industry

        Rules:
        - Prefer NSE listings
        - Mention ambiguity if multiple companies match
        - Avoid assumptions

        Return structured output.
        """,

        expected_output="""
        Structured stock identification including:
        - stock name
        - company name
        - ticker
        - exchange
        - sector
        - industry
        - ambiguity notes
        """,

        agent=agent,
    )


# ============================================================
# TECHNICAL ANALYSIS TASK
# ============================================================

def create_technical_analysis_task(agent) -> Task:
    """
    Analyze stock technical indicators.
    """

    return Task(
        description="""
        Use the resolved ticker.

        Analyze:
        - current price
        - 6-month return
        - RSI
        - moving averages
        - volume strength
        - momentum
        - trend signal

        Determine:
        - bullish/neutral/bearish trend
        - confidence level
        - technical risks

        Use actual tool data only.
        """,

        expected_output="""
        Technical analysis summary including:
        - trend direction
        - RSI analysis
        - momentum assessment
        - moving average analysis
        - confidence level
        - technical risks
        """,

        agent=agent,
    )


# ============================================================
# FUNDAMENTAL ANALYSIS TASK
# ============================================================

def create_fundamental_analysis_task(agent) -> Task:
    """
    Analyze company fundamentals and balance sheet.
    """

    return Task(
        description="""
        Analyze the company's fundamentals.

        Include:
        - valuation
        - profitability
        - liquidity
        - debt profile
        - growth
        - margins
        - balance sheet quality
        - cashflow health
        - analyst sentiment
        - dividend sustainability

        If historical balance sheet data exists:
        - analyze trends
        - identify improving/deteriorating metrics

        Avoid unsupported assumptions.
        Use actual financial evidence.
        """,

        expected_output="""
        Detailed fundamental analysis including:
        - valuation assessment
        - profitability assessment
        - debt analysis
        - liquidity assessment
        - growth analysis
        - dividend analysis
        - financial health summary
        - key strengths
        - key weaknesses
        - balance sheet trend analysis
        """,

        agent=agent,
    )


# ============================================================
# FINANCIAL METRICS TASK
# ============================================================

def create_financial_metrics_task(agent) -> Task:
    """
    Calculate missing financial metrics.
    """

    return Task(
        description="""
        Calculate financial ratios using available data.

        Calculate if possible:
        - ROE
        - ROA
        - Current Ratio
        - Quick Ratio
        - Debt-to-Assets Ratio
        - Asset Turnover Ratio
        - Working Capital
        - Net Debt
        - Book Value Per Share

        Rules:
        - Avoid divide-by-zero
        - Mention missing dependencies
        - Mention confidence level
        - Mention approximations clearly
        """,

        expected_output="""
        Structured financial metrics summary including:
        - calculated metrics
        - formulas used
        - assumptions
        - missing data
        - reliability assessment
        """,

        agent=agent,
    )


# ============================================================
# NEWS SENTIMENT TASK
# ============================================================

def create_news_analysis_task(agent) -> Task:
    """
    Analyze recent company news and sentiment.
    """

    return Task(
        description="""
        Analyze recent stock-related news.

        Determine:
        - overall sentiment
        - positive developments
        - negative developments
        - regulatory concerns
        - earnings/news impact

        Mention if news data is insufficient.
        """,

        expected_output="""
        News sentiment analysis including:
        - sentiment direction
        - positive catalysts
        - negative catalysts
        - event risks
        - near-term implications
        """,

        agent=agent,
    )


# ============================================================
# RISK ANALYSIS TASK
# ============================================================

def create_risk_analysis_task(agent) -> Task:
    """
    Identify major downside risks.
    """

    return Task(
        description="""
        Identify:
        - valuation risks
        - debt risks
        - technical downside
        - macroeconomic risks
        - sector risks
        - governance risks
        - liquidity risks
        - news/event risks

        Determine:
        - severity
        - probability
        - impact level
        """,

        expected_output="""
        Structured risk report including:
        - major risks
        - severity assessment
        - downside scenarios
        - risk probability
        - investment caution areas
        """,

        agent=agent,
    )


# ============================================================
# MACRO ANALYSIS TASK
# ============================================================

def create_macro_analysis_task(agent) -> Task:
    """
    Optional advanced macroeconomic analysis.
    """

    return Task(
        description="""
        Analyze macroeconomic conditions affecting the company.

        Include:
        - RBI policy impact
        - inflation impact
        - interest rate sensitivity
        - sector cyclicality
        - economic slowdown risks
        - commodity exposure if applicable
        """,

        expected_output="""
        Macro analysis summary including:
        - economic risks
        - policy impact
        - sector outlook
        - macro sensitivity
        """,

        agent=agent,
    )


# ============================================================
# PORTFOLIO RISK TASK
# ============================================================

def create_portfolio_risk_task(agent) -> Task:
    """
    Optional advanced portfolio suitability analysis.
    """

    return Task(
        description="""
        Evaluate portfolio suitability.

        Analyze:
        - volatility
        - diversification value
        - concentration risk
        - portfolio fit
        - risk-adjusted suitability
        """,

        expected_output="""
        Portfolio suitability summary including:
        - volatility assessment
        - diversification impact
        - concentration concerns
        - suitability observations
        """,

        agent=agent,
    )


# ============================================================
# FINAL INVESTMENT COMMITTEE TASK
# ============================================================

def create_final_investment_task(agent) -> Task:
    """
    Generate final structured stock assessment.
    """

    return Task(
        description="""
        Combine all prior analyses.

        Return STRICT VALID JSON.

        Structure:
        {
          "stock": "",
          "resolved_ticker": "",
          "market": "NSE",
          "near_term_view": "",
          "confidence": "",
          "technical_view": "",
          "fundamental_view": "",
          "news_sentiment_view": "",
          "risk_level": "",
          "key_growth_drivers": [],
          "key_risks": [],
          "data_limitations": [],
          "final_reasoning": "",
          "suggested_action": "",
          "further_research": [],
          "disclaimer": "",
          "failed_tasks":[]
        }

        Rules:
        - No guaranteed predictions
        - No financial advice
        - Be evidence-based
        - Mention missing data clearly
        """,

        expected_output="""
        Final structured investment outlook in valid JSON.
        """,

        agent=agent,
    )