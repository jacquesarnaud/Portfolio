"""Routes publiques consommées par le frontend indépendant."""

from fastapi import APIRouter

from python_ia.database.database import DbSession
from python_ia.models import Profile, Project
from python_ia.schemas.crud import ProfileRead, ProjectRead
from python_ia.services import portfolio

router = APIRouter(prefix="/api/v1/public", tags=["public"])


@router.get("/profile", response_model=ProfileRead | None)
async def read_public_profile(session: DbSession) -> Profile | None:
    return await portfolio.find_profile(session)


@router.get("/projects", response_model=list[ProjectRead])
async def read_public_projects(session: DbSession) -> list[Project]:
    return await portfolio.list_projects(session)
