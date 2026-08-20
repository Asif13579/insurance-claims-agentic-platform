import os
from langchain_openrouter import ChatOpenRouter

def get_llm() -> ChatOpenRouter:
    api_key=os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not configured")
    model=os.getenv("OPENROUTER_MODEL","openai/gpt-4o")
    return ChatOpenRouter(
        model=model,
        api_key=api_key,
        temperature=0
    )


# def get_llm():
#     return ChatOpenRouter(model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o"),api_key=os.getenv("OPENROUTER_API_KEY"),temperature=0,)
