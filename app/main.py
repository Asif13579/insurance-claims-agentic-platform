from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="Insurance Claims Agentic Platform",
    version="0.1.0",
)

app.include_router(router)


@app.get("/")
async def root():
    return {
        "message": "Insurance Claims Agentic Platform"
    }
