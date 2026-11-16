"""Routes API d'authentification."""

import time
from collections import defaultdict

from fastapi import APIRouter, HTTPException, Request, Response, status

from python_ia.core.config import settings
from python_ia.database.database import DbSession
from python_ia.schemas.auth import LoginRequest, TokenResponse
from python_ia.services.auth import authenticate_admin, create_access_token

router = APIRouter(prefix="/api/v1/auth", tags=["authentification"])

_failed_logins: dict[str, list[float]] = defaultdict(list)
_MAX_FAILED_LOGINS = 5
_LOGIN_WINDOW_SECONDS = 15 * 60


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, request: Request, response: Response, session: DbSession) -> TokenResponse:
    """Authentifie l'administrateur et retourne un jeton Bearer signé."""
    address = request.client.host if request.client else "unknown"
    now = time.monotonic()
    attempts = [timestamp for timestamp in _failed_logins[address] if now - timestamp < _LOGIN_WINDOW_SECONDS]
    _failed_logins[address] = attempts
    if len(attempts) >= _MAX_FAILED_LOGINS:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Trop de tentatives. Réessayez plus tard.")

    admin = await authenticate_admin(session, payload.username, payload.password)
    if admin is None:
        _failed_logins[address].append(now)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Bearer"},
        )
    _failed_logins.pop(address, None)
    access_token = create_access_token(admin)
    response.set_cookie(
        "portfolio_admin_token",
        access_token,
        max_age=60 * settings.access_token_expire_minutes,
        httponly=True,
        secure=not settings.debug,
        samesite="strict",
        path="/",
    )
    return TokenResponse(
        access_token=access_token,
        expires_in=60 * settings.access_token_expire_minutes,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response) -> None:
    response.delete_cookie("portfolio_admin_token", path="/")
