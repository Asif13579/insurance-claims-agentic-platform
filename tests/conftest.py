import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.config.database import Base, get_db


# --------------------------------------------------
# Test database
# --------------------------------------------------

TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)


# --------------------------------------------------
# Create a fresh database for every test
# --------------------------------------------------

@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


# --------------------------------------------------
# FastAPI test client
# --------------------------------------------------

@pytest.fixture()
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        # Authenticate once for tests that exercise protected routes.
        response = test_client.post(
            "/auth/login",
            json={
                "username": "admin",
                "password": "admin123",
            },
        )

        assert response.status_code == 200

        token = response.json()["access_token"]

        test_client.headers.update(
            {
                "Authorization": f"Bearer {token}"
            }
        )

        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture()
def authenticated_client(client):
    response = client.post(
        "/auth/login",
        json={
            "username": "admin",
            "password": "admin123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    client.headers.update(
        {
            "Authorization": f"Bearer {token}"
        }
    )

    return client