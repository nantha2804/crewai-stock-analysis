from dotenv import load_dotenv
import os
from crew import stock_crew


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

def run(stock: str):
    result = stock_crew.kickoff(inputs={"stock": stock})
    print(result)


if __name__ == "__main__":
    run("MSFT")

