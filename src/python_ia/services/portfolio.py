"""Services métier du portfolio.

Les services ne connaissent pas FastAPI. Ils reçoivent une session SQLModel
et peuvent donc être réutilisés par les API, les tâches de fond ou les tests.
"""

from datetime import UTC, datetime

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

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
    EducationCreate,
    ExperienceCreate,
    ProfileUpdate,
    ProjectCreate,
    ProjectImageCreate,
    SkillCreate,
)


async def find_profile(session: AsyncSession, published_only: bool = False) -> Profile | None:
    """Recherche le profil unique du portfolio."""
    profile = await session.get(Profile, 1)
    if published_only and profile is not None and not profile.is_published:
        return None
    return profile


async def save_profile(session: AsyncSession, payload: ProfileUpdate) -> Profile:
    """Crée ou met à jour le profil principal."""
    profile = await find_profile(session)
    if profile is None:
        profile = Profile(id=1, **payload.model_dump())
        session.add(profile)
    else:
        for key, value in payload.model_dump().items():
            setattr(profile, key, value)
    await session.commit()
    await session.refresh(profile)
    return profile


async def list_skills(session: AsyncSession, published_only: bool = False) -> list[Skill]:
    """Retourne les compétences dans leur ordre d'affichage."""
    query = select(Skill)
    if published_only:
        query = query.where(Skill.is_published)
    return list((await session.exec(query.order_by(Skill.display_order, Skill.name))).all())


async def create_skill(session: AsyncSession, payload: SkillCreate) -> Skill:
    """Persiste une compétence."""
    item = Skill(**payload.model_dump())
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def update_skill(session: AsyncSession, item: Skill, payload: SkillCreate) -> Skill:
    """Met à jour une compétence existante."""
    for key, value in payload.model_dump().items():
        setattr(item, key, value)
    await session.commit()
    await session.refresh(item)
    return item


async def delete_item(session: AsyncSession, item: object) -> None:
    """Supprime une entité SQLModel et valide la transaction."""
    await session.delete(item)
    await session.commit()


async def list_projects(session: AsyncSession, published_only: bool = False) -> list[Project]:
    """Retourne les projets triés pour le portfolio."""
    query = select(Project)
    if published_only:
        query = query.where(Project.is_published)
    return list((await session.exec(query.order_by(Project.display_order, Project.created_at.desc()))).all())


async def create_project(session: AsyncSession, payload: ProjectCreate) -> Project:
    """Persiste un projet."""
    item = Project(**payload.model_dump())
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def update_project(session: AsyncSession, item: Project, payload: ProjectCreate) -> Project:
    """Met à jour un projet et sa date de modification."""
    for key, value in payload.model_dump().items():
        setattr(item, key, value)
    item.updated_at = datetime.now(UTC).replace(tzinfo=None)
    await session.commit()
    await session.refresh(item)
    return item


async def add_project_image(session: AsyncSession, project_id: int, payload: ProjectImageCreate) -> ProjectImage:
    """Ajoute une image à un projet."""
    item = ProjectImage(project_id=project_id, **payload.model_dump())
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def list_experiences(session: AsyncSession, published_only: bool = False) -> list[Experience]:
    """Retourne les expériences triées par date et ordre d'affichage."""
    query = select(Experience)
    if published_only:
        query = query.where(Experience.is_published)
    return list((await session.exec(query.order_by(Experience.display_order, Experience.start_date.desc()))).all())


async def create_experience(session: AsyncSession, payload: ExperienceCreate) -> Experience:
    """Persiste une expérience professionnelle."""
    item = Experience(**payload.model_dump())
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def update_experience(session: AsyncSession, item: Experience, payload: ExperienceCreate) -> Experience:
    """Met à jour une expérience professionnelle."""
    for key, value in payload.model_dump().items():
        setattr(item, key, value)
    await session.commit()
    await session.refresh(item)
    return item


async def list_educations(session: AsyncSession, published_only: bool = False) -> list[Education]:
    """Retourne les formations et certifications."""
    query = select(Education)
    if published_only:
        query = query.where(Education.is_published)
    return list((await session.exec(query.order_by(Education.display_order, Education.end_date.desc()))).all())


async def create_education(session: AsyncSession, payload: EducationCreate) -> Education:
    """Persiste une formation ou une certification."""
    item = Education(**payload.model_dump())
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def update_education(session: AsyncSession, item: Education, payload: EducationCreate) -> Education:
    """Met à jour une formation ou une certification."""
    for key, value in payload.model_dump().items():
        setattr(item, key, value)
    await session.commit()
    await session.refresh(item)
    return item


async def create_contact_message(session: AsyncSession, payload: ContactMessageCreate) -> ContactMessage:
    """Enregistre un message de contact."""
    item = ContactMessage(**payload.model_dump())
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def list_contact_messages(session: AsyncSession) -> list[ContactMessage]:
    """Retourne les messages du plus récent au plus ancien."""
    return list((await session.exec(select(ContactMessage).order_by(ContactMessage.created_at.desc()))).all())
