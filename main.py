"""
main.py

Entry point for the AI Stock Analysis System.

Responsibilities:
-----------------
- initialize configuration
- initialize LLM
- initialize agents
- initialize tasks
- create CrewAI crew
- execute workflow
- save outputs
- print results

This file intentionally contains:
- orchestration only
- no business logic
"""

# ============================================================
# STANDARD LIBRARIES
# ============================================================

import json
import time
import os
from datetime import datetime

# ============================================================
# CREWAI
# ============================================================

from crewai import Crew

# ============================================================
# CONFIG
# ============================================================

from config import (
    AGENT_VERBOSE,
    API_KEY,
    BASE_URL,
    CREW_VERBOSE,
    ENABLE_MACRO_ANALYSIS,
    ENABLE_PORTFOLIO_ANALYSIS,
    MODEL_NAME,
    TEMPERATURE,
)

# ============================================================
# AGENTS
# ============================================================

from agents.agents import (
    create_fundamental_analyst_agent,
    create_investment_committee_agent,
    create_llm,
    create_macro_analyst_agent,
    create_news_analyst_agent,
    create_portfolio_risk_agent,
    create_risk_analyst_agent,
    create_stock_identifier_agent,
    create_technical_analyst_agent,
)

# ============================================================
# TASKS
# ============================================================

from agents.tasks import (
    create_final_investment_task,
    create_financial_metrics_task,
    create_fundamental_analysis_task,
    create_macro_analysis_task,
    create_news_analysis_task,
    create_portfolio_risk_task,
    create_risk_analysis_task,
    create_stock_identification_task,
    create_technical_analysis_task,
)

# ============================================================
# LOGGER
# ============================================================

from utils.logger import get_logger

logger = get_logger(__name__)

# ============================================================
# OUTPUT DIRECTORY
# ============================================================

OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# CREATE LLM
# ============================================================

logger.info("Initializing LLM...")

llm = create_llm(
    api_key=API_KEY,
    base_url=BASE_URL,
    model=MODEL_NAME,
    temperature=TEMPERATURE,
)

# ============================================================
# CREATE AGENTS
# ============================================================

logger.info("Creating agents...")

stock_identifier_agent = create_stock_identifier_agent(llm)

technical_analyst_agent = create_technical_analyst_agent(llm)

fundamental_analyst_agent = create_fundamental_analyst_agent(llm)

news_analyst_agent = create_news_analyst_agent(llm)

risk_analyst_agent = create_risk_analyst_agent(llm)

investment_committee_agent = (
    create_investment_committee_agent(llm)
)

# Optional advanced agents
macro_analyst_agent = None

portfolio_risk_agent = None

if ENABLE_MACRO_ANALYSIS:

    macro_analyst_agent = (
        create_macro_analyst_agent(llm)
    )

if ENABLE_PORTFOLIO_ANALYSIS:

    portfolio_risk_agent = (
        create_portfolio_risk_agent(llm)
    )

# ============================================================
# CREATE TASKS
# ============================================================

logger.info("Creating tasks...")

tasks = []

# ------------------------------------------------------------
# Core Tasks
# ------------------------------------------------------------

tasks.append(
    create_stock_identification_task(
        stock_identifier_agent
    )
)

tasks.append(
    create_technical_analysis_task(
        technical_analyst_agent
    )
)

tasks.append(
    create_fundamental_analysis_task(
        fundamental_analyst_agent
    )
)

tasks.append(
    create_financial_metrics_task(
        fundamental_analyst_agent
    )
)

tasks.append(
    create_news_analysis_task(
        news_analyst_agent
    )
)

tasks.append(
    create_risk_analysis_task(
        risk_analyst_agent
    )
)

# ------------------------------------------------------------
# Optional Advanced Tasks
# ------------------------------------------------------------

if macro_analyst_agent:

    tasks.append(
        create_macro_analysis_task(
            macro_analyst_agent
        )
    )

if portfolio_risk_agent:

    tasks.append(
        create_portfolio_risk_task(
            portfolio_risk_agent
        )
    )

# ------------------------------------------------------------
# Final Synthesis Task
# ------------------------------------------------------------

tasks.append(
    create_final_investment_task(
        investment_committee_agent
    )
)

# ============================================================
# CREATE CREW
# ============================================================

logger.info("Creating CrewAI crew...")

agents = [
    stock_identifier_agent,
    technical_analyst_agent,
    fundamental_analyst_agent,
    news_analyst_agent,
    risk_analyst_agent,
    investment_committee_agent,
]

if macro_analyst_agent:
    agents.append(macro_analyst_agent)

if portfolio_risk_agent:
    agents.append(portfolio_risk_agent)

crew = Crew(
    agents=agents,
    tasks=tasks,
    verbose=CREW_VERBOSE,
)

# ============================================================
# MAIN EXECUTION
# ============================================================

def run_stock_analysis():

    print("\n===================================")
    print(" AI STOCK ANALYSIS SYSTEM ")
    print("===================================\n")

    stock_name = input(
        "Enter stock/company name: "
    ).strip()

    if not stock_name:

        print("Stock name cannot be empty.")

        return

    logger.info(
        f"Starting analysis for: {stock_name}"
    )

    try:

        result = crew.kickoff(
            inputs={
                "stock_name": stock_name
            }
        )

        # ====================================================
        # PRINT OUTPUT
        # ====================================================

        print("\n===================================")
        print(" FINAL INVESTMENT ANALYSIS ")
        print("===================================\n")

        try:

            parsed_result = json.loads(
                str(result)
            )

            pretty_result = json.dumps(
                parsed_result,
                indent=2
            )

            print(pretty_result)

            return parsed_result



        except Exception:

            pretty_result = str(result)

            print(pretty_result)



        # ====================================================
        # SAVE OUTPUT
        # ====================================================

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            f"{stock_name.replace(' ', '_')}"
            f"_{timestamp}.json"
        )

        filepath = os.path.join(
            OUTPUT_DIR,
            filename
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(pretty_result)

        logger.info(
            f"Analysis saved to: {filepath}"
        )

        print(f"\nSaved report: {filepath}")

        return {

            "raw_result": pretty_result

        }


    except Exception as e:

        logger.exception(

            "Stock analysis failed."

        )

        print(f"\nError: {str(e)}")

        return {

            "error": str(e)

        }


# ============================================================
# SCRIPT ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run_stock_analysis()