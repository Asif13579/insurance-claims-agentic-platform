from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # ==========================================
    # Application
    # ==========================================
    APP_NAME: str="Telecom Agentic AI Platform"
    APP_VERSION: str="1.0.0"
    ENVIRONMENT: str="dev"
    DEBUG: bool=True

    # ==========================================
    # OpenAI / LLM
    # ==========================================
    OPENAI_API_KEY: str=""
    OPENAI_MODEL:str="gpt-4o"

    # Anthropic
    ANTHROPIC_API_KEY: str=""
    ANTHROPIC_MODEL:str="claude-sonnet-4"

    # ==========================================
    # Embeddings
    # ==========================================
    EMBEDDING_MODEL:str="text-embedding-3-large"
    # ==========================================
    # PostgreSQL
    # ==========================================
    DATABASE_URL: str=("postgresql+psycopg2://postgres:Welcome$401@localhost:5432/telecom_ai")

    # ==========================================
    # Redis Memory
    # ==========================================
    REDIS_HOST: str="localhost"
    REDIS_PORT:int=6379

    # ==========================================
    # Qdrant
    # ==========================================
    QDRANT_HOST: str="localhost"
    QDRANT_PORT: int=6333
    QDRANT_COLLECTION: str="telecom_knowleadge"

    # ==========================================
    # Neo4j
    # ==========================================
    NEO4J_URI: str="bolt://localhost:7687"
    NEO4J_USERNAME: str="neo4j"
    NEO4J_PASSWORD: str="Password"

    # ==========================================
    # LangSmith
    # ==========================================
    LANGCHAIN_TRACING_V2:bool=True
    LANGCHAIN_API_KEY: str=""
    LANGCHAIN_PROJECT: str="telecom-agentic-ai"

    # ==========================================
    # AWS
    # ==========================================
    AWS_ACCESS_KEY_ID:str=""
    AWS_SECRET_ACCESS_KEY: str=""
    AWS_REGION: str="ap-south-1" 
    S3_BUCKET_NAME: str = "telecom-agentic-docs"

    # ==========================================
    # MCP
    # ==========================================
    MCP_SERVER_URL:str="http://localhost:8001"

    # ==========================================
    # Agent Configuration
    # ==========================================
    MAX_AGENT_ITERATIONS: int=10
    AGENT_TIMEOUT_SECONDS: int=300

    # ==========================================
    # Logging
    # ==========================================
    LOG_LEVEL: str="INFO"
    model_config=SettingsConfigDict(env_file='.env',case_sensitive=True,extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings=get_settings()

