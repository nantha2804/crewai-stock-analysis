from dotenv import load_dotenv
from crewai import LLM
import os

load_dotenv()

llm = LLM(
    model="groq/openai/gpt-oss-20b",
    temperature=0
)

print("API key loaded:", bool(os.getenv("GROQ_API_KEY")))

response = llm.call("Say hello in one sentence.")

print(response)