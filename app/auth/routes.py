from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.dependencies import get_current_user

from app.auth.security import (
    authenticate_user,
    create_access_token,
)


router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(
        form_data.username,
        form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    access_token = create_access_token(
        user["username"]
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }