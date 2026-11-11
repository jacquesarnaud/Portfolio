"""Dépendances communes aux routes API."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from python_ia.database.database import DbSession
from python_ia.models import AdminUser
from python_ia.services.auth import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_current_admin(
    session: DbSession,
    token: str | None = Depends(oauth2_scheme),
) -> str:
    """Retourne l'administrateur authentifié ou refuse l'accès."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification requise",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_access_token(token)
    username = payload.get("sub") if payload else None
    admin_id = payload.get("admin_id") if payload else None
    admin = await session.get(AdminUser, admin_id) if isinstance(admin_id, int) else None
    if not isinstance(username, str) or admin is None or not admin.is_active or admin.username != username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username


CurrentAdmin = Annotated[str, Depends(get_current_admin)]
