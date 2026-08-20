from app.config.database import Base
from app.config.database import engine

from app.models.claim import Claim

def init_db():
    print("🚀 Initializing database...")

    print(
        "Registered tables:",
        Base.metadata.tables.keys()
    )
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully")


if __name__ == "__main__":
    init_db()

