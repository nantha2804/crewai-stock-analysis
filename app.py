
from pathlib import Path
import csv
import os

import gradio as gr

from crew import stock_crew


PROJECT_DIR = Path(__file__).resolve().parent
COMPANIES_FILE = PROJECT_DIR / "companies.csv"


def load_companies():
    companies = {}

    with open(COMPANIES_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            company = row["company"].strip()
            symbol = row["symbol"].strip()
            sector = row["sector"].strip()

            if company:
                companies[company] = {
                    "symbol": symbol,
                    "sector": sector,
                }

    return companies


# Sort company names alphabetically: A → Z
companies = load_companies()
company_names = sorted(companies.keys(), key=str.casefold)


def analyze_stock(company_name):
    if not company_name:
        return "## ⚠️ Please select a company."

    company = companies.get(company_name)

    if not company:
        return "## ⚠️ Invalid company selection."

    symbol = company["symbol"]
    sector = company["sector"]
    yahoo_symbol = f"{symbol}.NS"

    try:
        result = stock_crew.kickoff(
            inputs={"stock": yahoo_symbol}
        )

        return (
            f"# 📈 {company_name}\n\n"
            f"**Sector:** {sector}  \n"
            f"**NSE Symbol:** `{yahoo_symbol}`\n\n"
            f"---\n\n"
            f"# 🤖 AI Stock Analysis\n\n"
            f"{result}"
        )

    except Exception as e:
        return (
            f"# ❌ Analysis Error\n\n"
            f"Unable to analyze **{company_name}**.\n\n"
            f"```text\n{e}\n```"
        )


# Keep the page layout left-to-right
css = """
.gradio-container {
    direction: ltr;
}
"""


with gr.Blocks(
    title="AI Stock Analysis System"
) as app:

    gr.Markdown(
        """
        # 📈 AI Stock Analysis System

        ### Multi-Agent Stock Analysis powered by CrewAI

        Select an NSE-listed company to analyze its market
        information and generate an AI-powered
        **Buy / Sell / Hold recommendation**.
        """
    )

    with gr.Row():

        with gr.Column(scale=3):

            company_dropdown = gr.Dropdown(
                choices=company_names,
                label="🏢 Select Company",
                value=None,
                info="Choose an NSE-listed company (A → Z)",
                type="value"
            )

        with gr.Column(scale=1):

            analyze_button = gr.Button(
                "🔍 Analyze Stock",
                variant="primary",
                size="lg"
            )

    gr.Markdown("---")

    gr.Markdown(
        """
        ## 📊 Analysis Result

        Your multi-agent analysis will appear below.
        """
    )

    result = gr.Markdown(
        value="""
        ### 👋 Ready to Analyze

        1. Select a company from the dropdown.
        2. Click **Analyze Stock**.
        3. View the CrewAI analysis below.
        """,
        container=True
    )

    analyze_button.click(
        fn=analyze_stock,
        inputs=company_dropdown,
        outputs=result,
        show_progress="full"
    )


if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
        theme=gr.themes.Soft(),
        css=css
    )

