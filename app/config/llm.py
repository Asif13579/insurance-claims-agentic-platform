import os
from langchain_openrouter import ChatOpenRouter


def get_llm():

    return ChatOpenRouter(
        model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o"),
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0,
    )