from fastapi import FastAPI
from app.core.logging import configure_logging
from app.api.routes import router
from app.api.auth_routes import router as auth_router
from app.middleware.logging import (
    RequestLoggingMiddleware,
)

configure_logging()


app = FastAPI(
    title="Insurance Claims Agentic Platform",
    version="0.1.0",
)
app.add_middleware(
    RequestLoggingMiddleware
)

app.include_router(auth_router)
app.include_router(router)


@app.get("/")
async def root():
    return {
        "message": "Insurance Claims Agentic Platform"
    }