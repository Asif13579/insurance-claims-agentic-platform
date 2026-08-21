from fastapi import APIRouter, HTTPException, status

from app.auth.schemas import LoginRequest, TokenResponse
from app.auth.security import create_access_token, verify_password


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# Temporary user store.
# We will move this to PostgreSQL in the next authentication step.
USERS = {
    "admin": {
        "username": "admin",
        "hashed_password": (
            "$argon2id$v=19$m=65536,t=3,p=4$"
            "5pCzEUPv0iTKxF9376ZrTA$"
            "KZbIkG7ONT6OJ+TUGbPKFzQlxQ2zZ4GmPb6jQmxKnew"
        ),
    }
}


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(request: LoginRequest):

    user = USERS.get(request.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if not verify_password(
        request.password,
        user["hashed_password"],
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = create_access_token(
        subject=user["username"],
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
    )