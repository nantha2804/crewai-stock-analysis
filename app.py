
from pathlib import Path
import csv
import os

import gradio as gr

from crew import stock_crew


PROJECT_DIR = Path(__file__).resolve().parent
COMPANIES_FILE = PROJECT_DIR / "companies.csv"


def load_companies():
    companies = {}

    with COMPANIES_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        required_columns = {"company", "symbol", "sector"}
        actual_columns = set(reader.fieldnames or [])

        if not required_columns.issubset(actual_columns):
            raise ValueError(
                "companies.csv must contain: company, symbol, sector"
            )

        for row in reader:
            company = (row.get("company") or "").strip()
            symbol = (row.get("symbol") or "").strip()
            sector = (row.get("sector") or "").strip()

            if company and symbol:
                companies[company] = {
                    "symbol": symbol,
                    "sector": sector or "Not specified",
                }

    return companies


companies = load_companies()
company_names = sorted(companies.keys(), key=str.casefold)


def analyze_stock(company_name):
    if not company_name:
        return "## Please select a company first."

    company = companies.get(company_name)

    if not company:
        return "## Invalid company selection."

    symbol = company["symbol"]
    sector = company["sector"]

    yahoo_symbol = (
        symbol if symbol.endswith(".NS") else f"{symbol}.NS"
    )

    try:
        result = stock_crew.kickoff(
            inputs={"stock": yahoo_symbol}
        )

        return (
            f"# {company_name}\n\n"
            f"**Sector:** {sector}\n\n"
            f"**NSE Symbol:** `{yahoo_symbol}`\n\n"
            "---\n\n"
            "## AI Stock Analysis\n\n"
            f"{result}"
        )

    except Exception as error:
        print(
            f"Stock analysis failed for {yahoo_symbol}: "
            f"{type(error).__name__}: {error}"
        )

        return (
            "## Stock analysis failed\n\n"
            "Please check the PowerShell terminal for the error "
            "and verify your API configuration."
        )


with gr.Blocks(
    theme=gr.themes.Soft(),
    title="AI Stock Analysis"
) as app:

    gr.Markdown(
        """
        # AI Stock Analysis System

        Analyze NSE-listed companies using your CrewAI
        multi-agent stock analyst and trader.
        """
    )

    with gr.Row():
        company_dropdown = gr.Dropdown(
            choices=company_names,
            value=None,
            label="Select Company",
            info="Choose an NSE-listed company."
        )

        analyze_button = gr.Button(
            "Analyze Stock",
            variant="primary"
        )

    gr.Markdown("---")
    gr.Markdown("## Analysis Result")

    result = gr.Markdown(
        value=(
            "Select a company and click **Analyze Stock** "
            "to begin your analysis."
        ),
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
        server_port=int(os.environ.get("PORT", 7860))
    )