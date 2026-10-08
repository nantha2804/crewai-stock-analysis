from pathlib import Path
import csv

import gradio as gr

from crew import stock_crew


PROJECT_DIR = Path(__file__).resolve().parent
COMPANIES_FILE = PROJECT_DIR / "companies.csv"


def load_companies():
    companies = {}

    with open(COMPANIES_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            company = row["company"]
            symbol = row["symbol"]
            sector = row["sector"]

            companies[company] = {
                "symbol": symbol,
                "sector": sector,
            }

    return companies


companies = load_companies()
company_names = list(companies.keys())


def analyze_stock(company_name):
    if not company_name:
        return "Please select a company."

    company = companies[company_name]

    symbol = company["symbol"]
    sector = company["sector"]

    # Yahoo Finance NSE symbol
    yahoo_symbol = f"{symbol}.NS"

    try:
        result = stock_crew.kickoff(
            inputs={
                "stock": yahoo_symbol
            }
        )

        return (
            f"## {company_name}\n\n"
            f"**Sector:** {sector}\n\n"
            f"**NSE Symbol:** `{yahoo_symbol}`\n\n"
            f"---\n\n"
            f"## AI Stock Analysis\n\n"
            f"{result}"
        )

    except Exception as e:
        return (
            f"### Error\n\n"
            f"Unable to analyze **{company_name}**.\n\n"
            f"```text\n{e}\n```"
        )


with gr.Blocks(title="AI Stock Analysis") as app:

    gr.Markdown(
        """
        # 📈 AI Stock Analysis System

        Select an NSE-listed company and let the CrewAI agents
        analyze its live market information and provide a
        **Buy / Sell / Hold** recommendation.
        """
    )

    with gr.Row():

        company_dropdown = gr.Dropdown(
            choices=company_names,
            label="Select Company",
            value="HCL Technologies",
            info="Select an NSE-listed company"
        )

        analyze_button = gr.Button(
            "🔍 Analyze Stock",
            variant="primary"
        )

    result = gr.Markdown(
        value="Select a company and click **Analyze Stock**."
    )

    analyze_button.click(
        fn=analyze_stock,
        inputs=company_dropdown,
        outputs=result
    )


if __name__ == "__main__":
    app.launch(share=True)