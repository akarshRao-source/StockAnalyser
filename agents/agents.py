"""
agents.py

Defines all CrewAI agents used in the stock analysis system.

This file focuses ONLY on:
- agent responsibilities
- goals
- tools
- LLM configuration

No business logic should exist here.
No task descriptions should exist here.

That separation keeps the system:
- maintainable
- modular
- scalable
"""

from crewai import Agent, LLM

from tools.balance_sheet_tool import BalanceSheetTool
from tools.financial_metrics_tool import FinancialMetricsCalculatorTool
from tools.fundamentals_tool import FundamentalDataTool
from tools.news_tool import StockNewsTool
from tools.price_tool import StockPriceDataTool
from tools.stock_symbol_tool import StockSymbolResolverTool
from tools.technical_tool import TechnicalAnalysisTool


# ============================================================
# TOOL INITIALIZATION
# ============================================================

symbol_resolver_tool = StockSymbolResolverTool()

price_tool = StockPriceDataTool()

technical_tool = TechnicalAnalysisTool()

fundamental_tool = FundamentalDataTool()

balance_sheet_tool = BalanceSheetTool()

financial_metrics_tool = FinancialMetricsCalculatorTool()

news_tool = StockNewsTool()


# ============================================================
# AGENT FACTORY
# ============================================================

def create_llm(
    api_key: str,
    base_url: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0
) -> LLM:
    """
    Create shared LLM instance.

    Parameters:
    -----------
    api_key : str
    base_url : str
    model : str
    temperature : float

    Returns:
    --------
    LLM
    """

    return LLM(
        model=model,
        temperature=temperature,
        api_key=api_key,
        base_url=base_url,
    )


# ============================================================
# STOCK IDENTIFIER AGENT
# ============================================================

def create_stock_identifier_agent(llm: LLM) -> Agent:
    """
    Agent responsible for:
    - resolving stock tickers
    - identifying company details
    - avoiding symbol ambiguity
    """

    return Agent(
        role="NSE Stock Identification Specialist",

        goal=(
            "Identify the correct NSE/BSE-listed company "
            "and Yahoo Finance ticker from user input."
        ),

        backstory=(
            "You are an Indian stock market specialist skilled "
            "at mapping company names to the correct exchange-listed "
            "ticker symbols. You carefully avoid confusion between "
            "companies with similar names."
        ),

        tools=[symbol_resolver_tool],

        llm=llm,

        verbose=True,

        allow_delegation=False,

        max_iter=5,
    )


# ============================================================
# TECHNICAL ANALYST AGENT
# ============================================================

def create_technical_analyst_agent(llm: LLM) -> Agent:
    """
    Agent responsible for:
    - technical analysis
    - price action analysis
    - trend analysis
    - RSI/moving average interpretation
    """

    return Agent(
        role="Technical Market Analyst",

        goal=(
            "Analyze price action, trend strength, "
            "momentum, volume, and technical indicators."
        ),

        backstory=(
            "You are a professional technical analyst "
            "specializing in Indian equities. "
            "You interpret moving averages, RSI, momentum, "
            "and volume to determine market direction."
        ),

        tools=[
            price_tool,
            technical_tool,
        ],

        llm=llm,

        verbose=True,

        allow_delegation=False,

        max_iter=5,
    )


# ============================================================
# FUNDAMENTAL ANALYST AGENT
# ============================================================

def create_fundamental_analyst_agent(llm: LLM) -> Agent:
    """
    Agent responsible for:
    - financial statement analysis
    - valuation analysis
    - growth analysis
    - debt/liquidity analysis
    """

    return Agent(
        role="Fundamental Equity Analyst",

        goal=(
            "Evaluate the company's valuation, "
            "financial health, profitability, "
            "growth potential, and sustainability."
        ),

        backstory=(
            "You are an institutional-grade equity research analyst "
            "specializing in company fundamentals, "
            "balance sheets, earnings quality, "
            "cashflow analysis, and long-term business quality."
        ),

        tools=[
            fundamental_tool,
            balance_sheet_tool,
            financial_metrics_tool,
        ],

        llm=llm,

        verbose=True,

        allow_delegation=False,

        max_iter=6,
    )


# ============================================================
# NEWS & SENTIMENT ANALYST
# ============================================================

def create_news_analyst_agent(llm: LLM) -> Agent:
    """
    Agent responsible for:
    - recent news analysis
    - sentiment analysis
    - headline interpretation
    - event-driven risk analysis
    """

    return Agent(
        role="News and Sentiment Analyst",

        goal=(
            "Analyze recent news flow, market sentiment, "
            "and event-driven developments impacting the stock."
        ),

        backstory=(
            "You are a market sentiment expert who evaluates "
            "corporate announcements, earnings updates, "
            "industry developments, and investor sentiment."
        ),

        tools=[news_tool],

        llm=llm,

        verbose=True,

        allow_delegation=False,

        max_iter=4,
    )


# ============================================================
# RISK ANALYST AGENT
# ============================================================

def create_risk_analyst_agent(llm: LLM) -> Agent:
    """
    Agent responsible for:
    - downside analysis
    - identifying hidden risks
    - challenging bullish assumptions
    """

    return Agent(
        role="Investment Risk Analyst",

        goal=(
            "Identify financial, technical, "
            "valuation, sector, and macroeconomic risks."
        ),

        backstory=(
            "You are a conservative risk analyst. "
            "You specialize in finding weaknesses, "
            "hidden liabilities, overvaluation risks, "
            "and downside threats before investment decisions are made."
        ),

        llm=llm,

        verbose=True,

        allow_delegation=False,

        max_iter=5,
    )


# ============================================================
# MACRO ANALYST AGENT
# ============================================================

def create_macro_analyst_agent(llm: LLM) -> Agent:
    """
    Optional advanced agent.

    Responsible for:
    - interest rate analysis
    - inflation analysis
    - RBI/macroeconomic trends
    - sector cyclicality
    """

    return Agent(
        role="Macro Economic Analyst",

        goal=(
            "Analyze macroeconomic and sector-wide conditions "
            "that may impact stock performance."
        ),

        backstory=(
            "You are a macro strategist specializing in "
            "interest rates, inflation, liquidity cycles, "
            "economic growth, and sector rotation."
        ),

        llm=llm,

        verbose=True,

        allow_delegation=False,

        max_iter=4,
    )


# ============================================================
# PORTFOLIO RISK ANALYST
# ============================================================

def create_portfolio_risk_agent(llm: LLM) -> Agent:
    """
    Optional advanced agent.

    Responsible for:
    - portfolio suitability
    - volatility considerations
    - diversification impact
    """

    return Agent(
        role="Portfolio Risk Manager",

        goal=(
            "Evaluate how suitable the stock may be "
            "within a diversified investment portfolio."
        ),

        backstory=(
            "You are a portfolio construction expert "
            "focused on volatility, correlation, "
            "risk-adjusted returns, and diversification."
        ),

        llm=llm,

        verbose=True,

        allow_delegation=False,

        max_iter=4,
    )


# ============================================================
# FINAL INVESTMENT COMMITTEE AGENT
# ============================================================

def create_investment_committee_agent(llm: LLM) -> Agent:
    """
    Final synthesis agent.

    Responsible for:
    - combining all prior analyses
    - generating balanced final view
    - producing final structured output
    """

    return Agent(
        role="Investment Committee Chair",

        goal=(
            "Combine all technical, fundamental, risk, "
            "and sentiment analysis into a balanced "
            "investment outlook."
            "List Failed Tasks and its descriptions if any"
        ),

        backstory=(
            "You are the chairperson of an institutional "
            "investment committee. "
            "You carefully synthesize all analyst reports "
            "into a final evidence-based assessment."
        ),

        llm=llm,

        verbose=True,

        allow_delegation=True,

        max_iter=6,
    )