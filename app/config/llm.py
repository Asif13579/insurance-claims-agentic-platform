from langchain_openrouter import ChatOpenRouter
from app.config.settings import settings


def get_llm() -> ChatOpenRouter:

    if not settings.OPENROUTER_API_KEY:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not configured"
        )

    return ChatOpenRouter(
        model=settings.OPENROUTER_MODEL,
        api_key=settings.OPENROUTER_API_KEY,
        temperature=0,
    )