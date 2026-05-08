# StockAnalyser
## AI-Powered Multi-Agent Stock Analysis System

An advanced multi-agent equity research platform built using CrewAI
, Yahoo Finance (yfinance)
, and LLM-powered financial intelligence to perform comprehensive stock analysis for Indian equities.


# Project Structure

```
stock_analysis_project/
│
├── main.py
├── app.py
├── config.py
├── requirements.txt
├── .env
│
├── tools/
│   ├── base_models.py
│   ├── yahoo_finance_service.py
│   ├── stock_symbol_tool.py
│   ├── price_tool.py
│   ├── technical_tool.py
│   ├── fundamentals_tool.py
│   ├── balance_sheet_tool.py
│   ├── financial_metrics_tool.py
│   └── news_tool.py
│
├── agents/
│   ├── agents.py
│   └── tasks.py
│
└── utils/
    ├── helpers.py
    └── logger.py
```


The system combines multiple specialized AI agents that collaboratively analyze:

* technical indicators
* company fundamentals
* financial statements
* market sentiment
* news flow
* investment risks
* macroeconomic conditions

to generate a structured, evidence-based investment outlook.

Designed with a modular and production-ready architecture, the platform separates:

* tools
* agents
* tasks
* utilities
* configuration

making it scalable, maintainable, and extensible for future institutional-grade financial research workflows.

# Key Features
## Multi-Agent Financial Intelligence

The platform uses multiple specialized AI agents including:

* Stock Identification Agent
* Technical Analyst
* Fundamental Analyst
* News & Sentiment Analyst
* Risk Analyst
* Investment Committee Agent

Each agent independently evaluates different dimensions of a stock before synthesizing a final investment assessment.

## Technical Analysis Engine

Performs advanced technical analysis using:

* RSI (Relative Strength Index)
* Moving averages (20 DMA / 50 DMA / 200 DMA)
* Momentum analysis
* Volume analysis
* Trend detection
* Return calculations

Provides bullish, bearish, or neutral technical outlooks based on actual market data.

## Fundamental Analysis Engine

Analyzes:

* valuation metrics
* profitability
* liquidity
* leverage
* growth trends
* cash flow quality
* dividend sustainability
* analyst recommendations
* institutional ownership

using real-time financial data from Yahoo Finance.

## Financial Statement Intelligence

Processes:

* balance sheets
* income statements
* cash flow statements

to calculate advanced financial ratios such as:

* ROE
* ROA
* Current Ratio
* Quick Ratio
* Debt-to-Assets Ratio
* Asset Turnover Ratio
* Net Debt
* Working Capital

with built-in validation and missing-data handling.

## News & Sentiment Analysis

Fetches and analyzes recent company-related news headlines to identify:

positive catalysts
negative developments
regulatory concerns
earnings-related events
sentiment direction

for near-term market impact assessment.

## Risk Assessment Framework

Identifies:

* valuation risks
* leverage risks
* technical downside
* macroeconomic risks
* sector-specific threats
* data reliability concerns

to provide balanced and evidence-based investment reasoning.

## Production-Ready Architecture

The system is designed using:

* modular tool architecture
* centralized configuration
* reusable helper utilities
* centralized logging
* retry mechanisms
* JSON-safe serialization
* extensible agent/task orchestration

making it suitable for future scaling into:

* autonomous finance agents
* AI research copilots
* portfolio intelligence systems
* institutional research platforms

## Technology Stack

* Python
* CrewAI
* LangChain OpenAI
* Yahoo Finance (yfinance)
* Pandas
* NumPy
* Pydantic
* Tenacity
* dotenv


## Future Enhancements

Planned future upgrades include:

* RAG over annual reports
* PDF research report generation
* portfolio-level analysis
* peer comparison engine
* intrinsic valuation models
* real-time market feeds
* LangGraph orchestration
* vector database integration
* backtesting engine
* alerting and monitoring systems

### Disclaimer

This project is intended for educational and research purposes only and does not provide financial advice. Users should consult qualified financial advisors before making investment decisions.
