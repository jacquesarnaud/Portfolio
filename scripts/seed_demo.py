"""Insère des données fictives de démonstration dans le portfolio.

Le script est idempotent : il peut être relancé sans créer de doublons.
Les valeurs sont volontairement fictives et doivent être remplacées avant la
mise en production.
"""

import asyncio
from datetime import date

from sqlmodel import delete, select

from python_ia.database.database import session_factory
from python_ia.models import ContactMessage, Education, Experience, Profile, Project, ProjectImage, SiteSettings, Skill


SKILLS = [
    ("Python", "Programmation", 95, "devicon-python-plain"),
    ("JavaScript", "Programmation", 78, "devicon-javascript-plain"),
    ("HTML5", "Programmation", 90, "devicon-html5-plain"),
    ("CSS3", "Programmation", 88, "devicon-css3-plain"),
    ("FastAPI", "Backend", 92, "devicon-fastapi-plain"),
    ("Django", "Backend", 82, "devicon-django-plain"),
    ("Flask", "Backend", 78, "devicon-flask-original"),
    ("API REST", "Backend", 90, "fa-solid fa-code-branch"),
    ("WebSocket", "Backend", 72, "fa-solid fa-bolt"),
    ("JWT", "Sécurité", 80, "fa-solid fa-shield-halved"),
    ("PostgreSQL", "Bases de données", 88, "devicon-postgresql-plain"),
    ("SQLite", "Bases de données", 85, "devicon-sqlite-plain"),
    ("SQLAlchemy", "Bases de données", 84, "fa-solid fa-database"),
    ("Alembic", "Bases de données", 78, "fa-solid fa-arrows-rotate"),
    ("RAG & LLM", "Intelligence artificielle", 78, "fa-solid fa-brain"),
    ("Embeddings", "Intelligence artificielle", 74, "fa-solid fa-vector-square"),
    ("Git & GitHub", "Outils", 90, "devicon-github-original"),
    ("Docker", "Outils", 82, "devicon-docker-plain"),
    ("Linux", "Systèmes & réseaux", 76, "devicon-linux-plain"),
    ("Cybersécurité", "Systèmes & réseaux", 72, "fa-solid fa-lock"),
]

PROJECTS = [
    {
        "title": "Portfolio professionnel",
        "slug": "portfolio-professionnel",
        "short_description": "Une vitrine moderne pour présenter mon parcours, mes compétences et mes réalisations.",
        "description": "Plateforme portfolio construite avec FastAPI, Jinja2, HTMX, SQLModel, PostgreSQL et Docker. Elle intègre un espace d'administration et une API REST.",
        "technologies": "FastAPI, Jinja2, HTMX, PostgreSQL, Docker",
        "repository_url": "",
        "live_url": "",
        "cover_image_url": "/static/images/cover.jpg",
        "is_featured": True,
        "display_order": 1,
    },
    {
        "title": "MaquisManager",
        "slug": "maquismanager",
        "short_description": "Solution de gestion des commandes, des stocks et de la caisse pour les maquis et restaurants.",
        "description": "Une solution métier pensée pour simplifier le quotidien des restaurateurs et centraliser les opérations essentielles.",
        "technologies": "Python, FastAPI, PostgreSQL, Docker",
        "repository_url": "",
        "live_url": "",
        "cover_image_url": "/static/images/project1.jpg",
        "is_featured": True,
        "display_order": 2,
    },
    {
        "title": "School Management",
        "slug": "school-management",
        "short_description": "Application Django pour organiser la gestion d'un établissement scolaire.",
        "description": "Projet de gestion scolaire destiné à structurer les informations des élèves, des classes et de la vie académique.",
        "technologies": "Python, Django, PostgreSQL, HTML, CSS",
        "repository_url": "",
        "live_url": "",
        "cover_image_url": "/static/images/project2.jpg",
        "is_featured": True,
        "display_order": 3,
    },
    {
        "title": "Bot Telegram de téléchargement",
        "slug": "bot-telegram-telechargement",
        "short_description": "Bot Telegram connecté à une API FastAPI pour automatiser le téléchargement de vidéos.",
        "description": "Expérimentation d'un service asynchrone combinant bot Telegram, API web et traitement de requêtes utilisateurs.",
        "technologies": "Python, FastAPI, Telegram Bot API, WebSocket",
        "repository_url": "",
        "live_url": "",
        "cover_image_url": "/static/images/project1small.jpg",
        "is_featured": False,
        "display_order": 4,
    },
    {
        "title": "Projets IA & RAG",
        "slug": "projets-ia-rag",
        "short_description": "Expérimentations autour des LLM, des documents et de la recherche sémantique.",
        "description": "Conception de prototypes capables d'exploiter des documents, de générer des réponses contextualisées et de rechercher par similarité.",
        "technologies": "Python, RAG, LLM, Embeddings, API IA",
        "repository_url": "",
        "live_url": "",
        "cover_image_url": "/static/images/project2small.jpg",
        "is_featured": True,
        "display_order": 5,
    },
]


async def seed() -> None:
    async with session_factory() as session:
        # Le contenu de démonstration est remplacé par le profil réel. Le compte
        # administrateur n'est volontairement pas supprimé.
        for model in (ProjectImage, ContactMessage, Project, Skill, Experience, Education, Profile, SiteSettings):
            await session.exec(delete(model))

        session.add(Profile(
            id=1,
            full_name="Boua Bi Irie Jacques Arnaud",
            headline="Développeur Python · Backend & Intelligence artificielle",
            biography=("Je suis développeur Python passionné par le développement logiciel, "
                       "l'intelligence artificielle et les nouvelles technologies. Titulaire "
                       "d'une Licence en Informatique et Sciences du Numérique, spécialité "
                       "Réseaux et Sécurité Informatique, je conçois des APIs, des applications "
                       "web et des solutions utiles répondant à des problèmes concrets."),
            email="",
            phone="",
            location="Abidjan, Côte d'Ivoire",
            avatar_url="/static/images/Logo BJA — Développeur Python.png",
            cv_url="",
            github_url="",
            linkedin_url="",
            website_url="",
        ))
        session.add(SiteSettings(
            id=1,
            site_name="BJA — Développeur Python",
            meta_description="Portfolio de Boua Bi Irie Jacques Arnaud, développeur Python spécialisé en backend et intelligence artificielle.",
            accent_color="#7c3aed",
        ))

        for order, (name, category, proficiency, icon) in enumerate(SKILLS, 1):
            session.add(Skill(name=name, category=category, proficiency=proficiency, icon=icon, display_order=order))

        for data in PROJECTS:
            session.add(Project(**data))

        session.add(Education(
            institution="Université Virtuelle de Côte d'Ivoire (UVCI)",
            title="Licence en Informatique et Sciences du Numérique — Réseaux et Sécurité Informatique",
            description="Diplôme obtenu en 2026. Formation en réseaux, sécurité informatique, systèmes et développement logiciel.",
            start_date=date(2022, 1, 1), end_date=date(2026, 1, 1), display_order=1,
        ))
        session.add(Education(
            institution="Nan Académique",
            title="Formation Développeur Python — Intelligence Artificielle",
            description="Formation en développement Python et intelligence artificielle, du 2 février au 16 novembre 2026.",
            start_date=date(2026, 2, 2), end_date=date(2026, 11, 16), display_order=2,
        ))
        session.add(Education(
            institution="Certification professionnelle",
            title="Certification en E-banking",
            description="Certification obtenue en 2026.",
            start_date=date(2026, 1, 1), end_date=date(2026, 1, 1), is_certification=True, display_order=3,
        ))
        session.add(Education(
            institution="Udemy · Jonathan Roux",
            title="Certificat Développeur Python",
            description="Formation orientée programmation et développement Python.",
            display_order=4,
        ))

        await session.commit()
        print("Données professionnelles de Boua Bi Irie Jacques Arnaud insérées avec succès.")


if __name__ == "__main__":
    asyncio.run(seed())
