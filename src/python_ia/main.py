"""Point d'entrée de l'application FastAPI."""

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from python_ia.api.router import router
from python_ia.core.config import settings
from python_ia.database.database import session_factory
from python_ia.services.auth import ensure_admin
from python_ia.web.routes import router as web_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialise le compte administrateur unique au démarrage."""
    async with session_factory() as session:
        await ensure_admin(session)
    yield


def create_app() -> FastAPI:
    """Construit l'application afin de faciliter les tests et le déploiement."""
    application = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)
    application.mount("/static", StaticFiles(directory=Path(__file__).parent / "web" / "static"), name="static")
    application.include_router(router)
    application.include_router(web_router)
    return application


app = create_app()
