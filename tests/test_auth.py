from app.auth.security import (
    create_access_token,
    hash_password,
    verify_password,
)


def test_password_hash_and_verify():

    password = "secret123"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong-password", hashed)


def test_create_access_token():

    token = create_access_token("admin")

    assert token
    assert isinstance(token, str)


def test_login(client):

    # This test assumes the temporary admin user
    # is configured with password "admin123".

    response = client.post(
        "/auth/login",
        json={
            "username": "admin",
            "password": "admin123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_invalid_login(client):

    response = client.post(
        "/auth/login",
        json={
            "username": "admin",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401


def test_missing_token_rejected(client):
    client.headers.pop("Authorization", None)
    response = client.get(
        "/claims/CLM-DOES-NOT-EXIST"
    )

    assert response.status_code == 401