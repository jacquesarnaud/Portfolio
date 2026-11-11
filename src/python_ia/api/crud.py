"""Routes HTTP CRUD du portfolio.

Ce module se limite à la couche HTTP. La logique métier et les transactions
sont déléguées à ``services.portfolio``.
"""

from fastapi import APIRouter, HTTPException, status

from python_ia.api.dependencies import CurrentAdmin
from python_ia.database.database import DbSession
from python_ia.models import (
    ContactMessage,
    Education,
    Experience,
    Profile,
    Project,
    ProjectImage,
    Skill,
)
from python_ia.schemas.crud import (
    ContactMessageCreate,
    ContactMessageRead,
    EducationCreate,
    EducationRead,
    ExperienceCreate,
    ExperienceRead,
    ProfileRead,
    ProfileUpdate,
    ProjectCreate,
    ProjectImageCreate,
    ProjectImageRead,
    ProjectRead,
    SkillCreate,
    SkillRead,
)
from python_ia.services import portfolio

router = APIRouter(prefix="/api/v1", tags=["portfolio"])


@router.get("/profile", response_model=ProfileRead)
async def read_profile(session: DbSession, _: CurrentAdmin) -> Profile:
    """Retourne les informations publiques du profil principal."""
    item = await portfolio.find_profile(session)
    if item is None:
        raise HTTPException(404, "Profil introuvable")
    return item


@router.put("/profile", response_model=ProfileRead)
async def update_profile(payload: ProfileUpdate, session: DbSession, _: CurrentAdmin) -> Profile:
    """Crée ou met à jour le profil unique du portfolio."""
    return await portfolio.save_profile(session, payload)


@router.get("/skills", response_model=list[SkillRead])
async def list_skills(session: DbSession, _: CurrentAdmin) -> list[Skill]:
    """Retourne les compétences triées."""
    return await portfolio.list_skills(session)


@router.post("/skills", response_model=SkillRead, status_code=status.HTTP_201_CREATED)
async def create_skill(payload: SkillCreate, session: DbSession, _: CurrentAdmin) -> Skill:
    """Ajoute une compétence technique."""
    return await portfolio.create_skill(session, payload)


@router.put("/skills/{skill_id}", response_model=SkillRead)
async def update_skill(skill_id: int, payload: SkillCreate, session: DbSession, _: CurrentAdmin) -> Skill:
    """Met à jour une compétence existante."""
    item = await session.get(Skill, skill_id)
    if item is None:
        raise HTTPException(404, "Compétence introuvable")
    return await portfolio.update_skill(session, item, payload)


@router.delete("/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(skill_id: int, session: DbSession, _: CurrentAdmin) -> None:
    """Supprime une compétence."""
    item = await session.get(Skill, skill_id)
    if item is None:
        raise HTTPException(404, "Compétence introuvable")
    await portfolio.delete_item(session, item)


@router.get("/projects", response_model=list[ProjectRead])
async def list_projects(session: DbSession, _: CurrentAdmin) -> list[Project]:
    """Retourne les projets du portfolio."""
    return await portfolio.list_projects(session)


@router.post("/projects", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(payload: ProjectCreate, session: DbSession, _: CurrentAdmin) -> Project:
    """Crée un projet."""
    return await portfolio.create_project(session, payload)


@router.get("/projects/{project_id}", response_model=ProjectRead)
async def read_project(project_id: int, session: DbSession, _: CurrentAdmin) -> Project:
    """Retourne le détail d'un projet."""
    item = await session.get(Project, project_id)
    if item is None:
        raise HTTPException(404, "Projet introuvable")
    return item


@router.put("/projects/{project_id}", response_model=ProjectRead)
async def update_project(project_id: int, payload: ProjectCreate, session: DbSession, _: CurrentAdmin) -> Project:
    """Met à jour un projet."""
    item = await session.get(Project, project_id)
    if item is None:
        raise HTTPException(404, "Projet introuvable")
    return await portfolio.update_project(session, item, payload)


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, session: DbSession, _: CurrentAdmin) -> None:
    """Supprime un projet et ses images."""
    item = await session.get(Project, project_id)
    if item is None:
        raise HTTPException(404, "Projet introuvable")
    await portfolio.delete_item(session, item)


@router.post("/projects/{project_id}/images", response_model=ProjectImageRead, status_code=status.HTTP_201_CREATED)
async def add_project_image(project_id: int, payload: ProjectImageCreate, session: DbSession, _: CurrentAdmin) -> ProjectImage:
    """Ajoute une image à un projet."""
    if await session.get(Project, project_id) is None:
        raise HTTPException(404, "Projet introuvable")
    return await portfolio.add_project_image(session, project_id, payload)


@router.delete("/projects/{project_id}/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_image(project_id: int, image_id: int, session: DbSession, _: CurrentAdmin) -> None:
    """Supprime une image de projet."""
    item = await session.get(ProjectImage, image_id)
    if item is None or item.project_id != project_id:
        raise HTTPException(404, "Image introuvable")
    await portfolio.delete_item(session, item)


@router.get("/experiences", response_model=list[ExperienceRead])
async def list_experiences(session: DbSession, _: CurrentAdmin) -> list[Experience]:
    """Retourne les expériences professionnelles."""
    return await portfolio.list_experiences(session)


@router.post("/experiences", response_model=ExperienceRead, status_code=status.HTTP_201_CREATED)
async def create_experience(payload: ExperienceCreate, session: DbSession, _: CurrentAdmin) -> Experience:
    """Ajoute une expérience professionnelle."""
    return await portfolio.create_experience(session, payload)


@router.put("/experiences/{experience_id}", response_model=ExperienceRead)
async def update_experience(experience_id: int, payload: ExperienceCreate, session: DbSession, _: CurrentAdmin) -> Experience:
    """Met à jour une expérience professionnelle."""
    item = await session.get(Experience, experience_id)
    if item is None:
        raise HTTPException(404, "Expérience introuvable")
    return await portfolio.update_experience(session, item, payload)


@router.delete("/experiences/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experience(experience_id: int, session: DbSession, _: CurrentAdmin) -> None:
    """Supprime une expérience professionnelle."""
    item = await session.get(Experience, experience_id)
    if item is None:
        raise HTTPException(404, "Expérience introuvable")
    await portfolio.delete_item(session, item)


@router.get("/educations", response_model=list[EducationRead])
async def list_educations(session: DbSession, _: CurrentAdmin) -> list[Education]:
    """Retourne les formations et certifications."""
    return await portfolio.list_educations(session)


@router.post("/educations", response_model=EducationRead, status_code=status.HTTP_201_CREATED)
async def create_education(payload: EducationCreate, session: DbSession, _: CurrentAdmin) -> Education:
    """Ajoute une formation ou une certification."""
    return await portfolio.create_education(session, payload)


@router.put("/educations/{education_id}", response_model=EducationRead)
async def update_education(education_id: int, payload: EducationCreate, session: DbSession, _: CurrentAdmin) -> Education:
    """Met à jour une formation ou une certification."""
    item = await session.get(Education, education_id)
    if item is None:
        raise HTTPException(404, "Formation introuvable")
    return await portfolio.update_education(session, item, payload)


@router.delete("/educations/{education_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_education(education_id: int, session: DbSession, _: CurrentAdmin) -> None:
    """Supprime une formation ou une certification."""
    item = await session.get(Education, education_id)
    if item is None:
        raise HTTPException(404, "Formation introuvable")
    await portfolio.delete_item(session, item)


@router.post("/contact", response_model=ContactMessageRead, status_code=status.HTTP_201_CREATED)
async def create_contact_message(payload: ContactMessageCreate, session: DbSession) -> ContactMessage:
    """Enregistre un message de contact."""
    return await portfolio.create_contact_message(session, payload)


@router.get("/contact", response_model=list[ContactMessageRead])
async def list_contact_messages(session: DbSession, _: CurrentAdmin) -> list[ContactMessage]:
    """Retourne les messages reçus."""
    return await portfolio.list_contact_messages(session)
