"""Routeur principal : les routeurs métier seront enregistrés ici."""

from fastapi import APIRouter
from sqlalchemy import text

from python_ia.api.auth import router as auth_router
from python_ia.api.crud import router as crud_router
from python_ia.api.public import router as public_router
from python_ia.database.database import DbSession

router = APIRouter()
router.include_router(crud_router)
router.include_router(auth_router)
router.include_router(public_router)


@router.get("/health", tags=["système"])
async def health_check() -> dict[str, str]:
    """Endpoint minimal utilisé par les plateformes de déploiement."""
    return {"status": "ok"}


@router.get("/health/database", tags=["système"])
async def database_health_check(
    session: DbSession,
) -> dict[str, str]:
    """Vérifie que l'application peut atteindre la base Neon."""
    await session.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
