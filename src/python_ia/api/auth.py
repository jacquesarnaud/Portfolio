"""Routes API d'authentification."""

from fastapi import APIRouter, HTTPException, status

from python_ia.core.config import settings
from python_ia.database.database import DbSession
from python_ia.schemas.auth import LoginRequest, TokenResponse
from python_ia.services.auth import authenticate_admin, create_access_token

router = APIRouter(prefix="/api/v1/auth", tags=["authentification"])


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, session: DbSession) -> TokenResponse:
    """Authentifie l'administrateur et retourne un jeton Bearer signé."""
    admin = await authenticate_admin(session, payload.username, payload.password)
    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenResponse(
        access_token=create_access_token(admin),
        expires_in=60 * settings.access_token_expire_minutes,
    )
