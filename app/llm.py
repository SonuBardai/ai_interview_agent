import os
from crewai import LLM


# model = "llama3"
# ollama = LLM(model=f"ollama/{model}", base_url="http://localhost:11434")
# llm = ollama

gemini = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
    api_key=os.getenv("GEMINI_API_KEY"),
)
llm = gemini
