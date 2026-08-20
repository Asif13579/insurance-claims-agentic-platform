from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError

from app.config.settings import settings



# SQLAlchemy Engine
# ==================================================
#engine=create_engine(settings.DATABASE_URL,pool_size=20,max_overflow=10,pool_pre_ping=True,pool_recycle=1800,echo=False,future=True)
engine=create_engine(settings.DATABASE_URL,pool_size=20,max_overflow=10,pool_pre_ping=True,pool_recycle=1800,echo=False,future=True)
# ==================================================
# Session Factory
# ==================================================
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine,expire_on_commit=False)

# ==================================================
# Base Model
# ==================================================
Base=declarative_base()

# ==================================================
# FastAPI Dependency
# ==================================================
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

    
# ==================================================
# Transaction Context Manager
# ==================================================
@contextmanager
def db_transaction():
    session=SessionLocal()
    try:
        yield session
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()

# ==================================================
# Health Check
# ==================================================
def check_database_health():
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return {
            "status":"healthy",
            "database":"connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error":str(e)
        }