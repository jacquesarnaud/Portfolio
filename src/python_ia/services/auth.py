"""Services d'authentification sécurisée de l'administrateur."""

from datetime import UTC, datetime, timedelta

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from python_ia.core.config import settings
from python_ia.models import AdminUser

password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Hache un mot de passe avec Argon2id."""
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Vérifie un mot de passe sans jamais comparer les valeurs en clair."""
    try:
        return password_hasher.verify(password_hash, password)
    except (VerifyMismatchError, InvalidHashError):
        return False


async def ensure_admin(session: AsyncSession) -> AdminUser:
    """Crée le seul compte admin au premier démarrage s'il n'existe pas."""
    result = await session.exec(select(AdminUser).limit(1))
    admin = result.first()
    if admin is None:
        admin = AdminUser(
            id=1,
            username=settings.admin_username,
            password_hash=hash_password(settings.admin_password),
        )
        session.add(admin)
        await session.commit()
        await session.refresh(admin)
    return admin


async def authenticate_admin(session: AsyncSession, username: str, password: str) -> AdminUser | None:
    """Authentifie l'unique compte administrateur depuis PostgreSQL."""
    result = await session.exec(select(AdminUser).where(AdminUser.username == username))
    admin = result.first()
    if admin is None or not admin.is_active or not verify_password(password, admin.password_hash):
        return None
    return admin


def create_access_token(admin: AdminUser) -> str:
    """Crée un JWT signé avec une date d'expiration."""
    now = datetime.now(UTC)
    expires_at = now + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": admin.username,
        "admin_id": admin.id,
        "iat": now,
        "exp": expires_at,
        "type": "admin_access",
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, object] | None:
    """Décode et valide un JWT d'administration."""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except jwt.InvalidTokenError:
        return None
    if payload.get("type") != "admin_access" or not isinstance(payload.get("sub"), str):
        return None
    return payload
