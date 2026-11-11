"""Routes HTML publiques et interface d'administration."""

from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select

from python_ia.database.database import DbSession
from python_ia.models import ContactMessage, Project
from python_ia.schemas.crud import ContactMessageCreate
from python_ia.services import portfolio

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter(tags=["interface web"])


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, session: DbSession):
    """Affiche la page d'accueil publique."""
    return templates.TemplateResponse(
        request,
        "home.html",
        {"profile": await portfolio.find_profile(session), "projects": await portfolio.list_projects(session), "skills": await portfolio.list_skills(session), "experiences": await portfolio.list_experiences(session)},
    )


@router.get("/projets", response_class=HTMLResponse)
async def projects(request: Request, session: DbSession):
    """Affiche la liste publique des projets."""
    return templates.TemplateResponse(request, "projects.html", {"projects": await portfolio.list_projects(session)})


@router.get("/projets/{slug}", response_class=HTMLResponse)
async def project_detail(slug: str, request: Request, session: DbSession):
    result = await session.exec(select(Project).where(Project.slug == slug, Project.is_published))
    project = result.first()
    if project is None:
        raise HTTPException(status_code=404, detail="Projet introuvable")
    return templates.TemplateResponse(request, "project_detail.html", {"project": project})


@router.get("/a-propos", response_class=HTMLResponse)
async def about(request: Request, session: DbSession):
    return templates.TemplateResponse(request, "about.html", {"profile": await portfolio.find_profile(session)})


@router.get("/competences", response_class=HTMLResponse)
async def skills(request: Request, session: DbSession):
    return templates.TemplateResponse(request, "skills.html", {"skills": await portfolio.list_skills(session)})


@router.get("/experiences", response_class=HTMLResponse)
async def experiences(request: Request, session: DbSession):
    return templates.TemplateResponse(request, "experiences.html", {"experiences": await portfolio.list_experiences(session)})


@router.get("/formations", response_class=HTMLResponse)
async def education(request: Request, session: DbSession):
    return templates.TemplateResponse(request, "education.html", {"educations": await portfolio.list_educations(session)})


@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse(request, "contact.html", {"sent": False})


@router.post("/contact", response_class=HTMLResponse)
async def submit_contact(
    request: Request,
    session: DbSession,
    sender_name: str = Form(...),
    sender_email: str = Form(...),
    subject: str = Form(""),
    body: str = Form(...),
):
    payload = ContactMessageCreate(sender_name=sender_name, sender_email=sender_email, subject=subject, body=body)
    await portfolio.create_contact_message(session, payload)
    return templates.TemplateResponse(request, "contact.html", {"sent": True})


@router.get("/admin/login", response_class=HTMLResponse)
async def admin_login(request: Request):
    """Affiche le formulaire de connexion administrateur."""
    return templates.TemplateResponse(request, "admin/login.html")


@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, session: DbSession):
    """Affiche le dashboard ; les actions restent protégées par les API."""
    projects = await portfolio.list_projects(session)
    skills = await portfolio.list_skills(session)
    experiences = await portfolio.list_experiences(session)
    educations = await portfolio.list_educations(session)
    messages = await portfolio.list_contact_messages(session)
    return templates.TemplateResponse(
        request,
        "admin/dashboard.html",
        {"stats": {"projects": len(projects), "skills": len(skills), "experiences": len(experiences), "educations": len(educations), "messages": len(messages), "unread": sum(not item.is_read for item in messages)}},
    )
