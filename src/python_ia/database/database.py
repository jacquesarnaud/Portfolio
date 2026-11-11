"""Connexion asynchrone à PostgreSQL Neon avec SQLModel."""

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from python_ia.core.config import settings

engine = create_async_engine(
    settings.async_database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)

session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncIterator[AsyncSession]:
    """Fournit une session SQLModel à une route FastAPI.

    FastAPI ouvre cette dépendance pour chaque requête puis ferme la session
    automatiquement à la fin de la requête.
    """
    async with session_factory() as session:
        yield session


# Type de dépendance réutilisable dans toutes les routes et tous les services
# appelés par les routes. Il garantit qu'une seule session par requête est
# fournie par FastAPI.
DbSession = Annotated[AsyncSession, Depends(get_db)]

# Alias de compatibilité pour les anciens imports.
get_session = get_db
