"""Insère des données fictives de démonstration dans le portfolio.

Le script est idempotent : il peut être relancé sans créer de doublons.
Les valeurs sont volontairement fictives et doivent être remplacées avant la
mise en production.
"""

import asyncio
from datetime import date

from sqlmodel import select

from python_ia.database.database import session_factory
from python_ia.models import Education, Experience, Profile, Project, SiteSettings, Skill


SKILLS = [
    ("Python", "Langages", 95, "fa-brands fa-python"),
    ("FastAPI", "Backend", 90, "fa-solid fa-bolt"),
    ("SQLModel", "Bases de données", 85, "fa-solid fa-database"),
    ("PostgreSQL", "Bases de données", 85, "fa-solid fa-database"),
    ("JavaScript", "Frontend", 78, "fa-brands fa-js"),
    ("HTML / CSS", "Frontend", 88, "fa-brands fa-html5"),
    ("Docker", "Outils", 82, "fa-brands fa-docker"),
    ("Git", "Outils", 90, "fa-brands fa-git-alt"),
]

PROJECTS = [
    {
        "title": "Nexus Portfolio",
        "slug": "nexus-portfolio",
        "short_description": "Portfolio professionnel administrable et responsive.",
        "description": "Une plateforme conçue pour présenter un parcours, des projets et des compétences avec une interface d'administration simple.",
        "technologies": "FastAPI, Jinja2, HTMX, PostgreSQL, Docker",
        "repository_url": "https://github.com/demo/nexus-portfolio",
        "live_url": "https://portfolio.example.com",
        "is_featured": True,
        "display_order": 1,
    },
    {
        "title": "Clarity Tasks",
        "slug": "clarity-tasks",
        "short_description": "Application de gestion de tâches pour petites équipes.",
        "description": "Une application collaborative avec gestion des priorités, filtres et suivi de l'avancement des tâches.",
        "technologies": "Python, FastAPI, PostgreSQL, Bootstrap",
        "repository_url": "https://github.com/demo/clarity-tasks",
        "live_url": "https://clarity.example.com",
        "is_featured": True,
        "display_order": 2,
    },
    {
        "title": "DataPulse",
        "slug": "datapulse",
        "short_description": "Tableau de bord pour visualiser des indicateurs métier.",
        "description": "Un tableau de bord qui agrège des données et fournit une lecture claire des indicateurs essentiels.",
        "technologies": "Python, SQL, JavaScript, Chart.js",
        "repository_url": "https://github.com/demo/datapulse",
        "live_url": "",
        "is_featured": True,
        "display_order": 3,
    },
    {
        "title": "API Atlas",
        "slug": "api-atlas",
        "short_description": "API de catalogue documentée et sécurisée.",
        "description": "Une API REST modulaire avec authentification, validation des données et documentation OpenAPI.",
        "technologies": "FastAPI, JWT, SQLAlchemy, Docker",
        "repository_url": "https://github.com/demo/api-atlas",
        "live_url": "",
        "is_featured": False,
        "display_order": 4,
    },
]


async def seed() -> None:
    async with session_factory() as session:
        profile = await session.get(Profile, 1)
        if profile is None:
            session.add(Profile(
                id=1,
                full_name="Alex Martin",
                headline="Développeur Python & Backend",
                biography="Je conçois des applications web fiables et utiles, de l'API jusqu'à l'expérience utilisateur.",
                email="alex.martin@example.com",
                phone="+33 6 00 00 00 00",
                location="Lyon, France",
                avatar_url="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400",
                cv_url="/static/uploads/cv-alex-martin.pdf",
                github_url="https://github.com/demo",
                linkedin_url="https://www.linkedin.com/in/demo",
                website_url="https://portfolio.example.com",
            ))

        if await session.get(SiteSettings, 1) is None:
            session.add(SiteSettings(id=1, site_name="Alex Martin — Portfolio", meta_description="Portfolio fictif d'un développeur Python et backend.", accent_color="#38bdf8"))

        existing_skills = {item.name for item in (await session.exec(select(Skill))).all()}
        for order, (name, category, proficiency, icon) in enumerate(SKILLS, 1):
            if name not in existing_skills:
                session.add(Skill(name=name, category=category, proficiency=proficiency, icon=icon, display_order=order))

        for data in PROJECTS:
            result = await session.exec(select(Project).where(Project.slug == data["slug"]))
            project = result.first()
            if project is None:
                session.add(Project(**data))
            else:
                for key, value in data.items():
                    setattr(project, key, value)

        if not (await session.exec(select(Experience).where(Experience.company == "Studio Horizon"))).first():
            session.add(Experience(company="Studio Horizon", position="Développeur Python", location="Lyon", description="Conception d'API, automatisation de processus et amélioration de la qualité logicielle.", start_date=date(2023, 1, 1), end_date=date(2025, 6, 30), display_order=1))
        if not (await session.exec(select(Experience).where(Experience.company == "Atelier Numérique"))).first():
            session.add(Experience(company="Atelier Numérique", position="Développeur backend junior", location="Grenoble", description="Développement de fonctionnalités web et maintenance de services internes.", start_date=date(2021, 9, 1), end_date=date(2022, 12, 31), display_order=2))

        if not (await session.exec(select(Education).where(Education.title == "Master Ingénierie Logicielle"))).first():
            session.add(Education(institution="Université Lumière", title="Master Ingénierie Logicielle", description="Formation fictive en architecture logicielle et développement web.", start_date=date(2019, 9, 1), end_date=date(2021, 6, 30), display_order=1))
        if not (await session.exec(select(Education).where(Education.title == "Certification Cloud Developer"))).first():
            session.add(Education(institution="Tech Academy", title="Certification Cloud Developer", description="Certification fictive orientée déploiement et conteneurisation.", start_date=date(2022, 3, 1), end_date=date(2022, 6, 30), is_certification=True, display_order=2))

        await session.commit()
        print("Données fictives insérées avec succès.")


if __name__ == "__main__":
    asyncio.run(seed())
