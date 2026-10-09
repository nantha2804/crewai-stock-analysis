from crewai import Agent, LLM

from tools.stock_research_tool import get_stock_price

llm = LLM(
    model="groq/openai/gpt-oss-20b",
    temperature=0
)

trader_agent = Agent(
    role="Strategic Stock Trader",
    goal=(
        "Make a careful Buy, Sell, or Hold assessment using the "
        "available market data and financial analysis."
    ),
    backstory=(
        "You are a disciplined stock trader. You evaluate price changes, "
        "trading volume, and recent momentum. You must use the Live Stock "
        "Information Tool to retrieve market data before making a decision. "
        "Never invent missing prices or indicators. Explain uncertainty "
        "and remember that your output is informational, not a guarantee "
        "of future returns."
    ),
    tools=[get_stock_price],
    llm=llm,
    verbose=True
)
