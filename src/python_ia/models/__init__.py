"""Modèles SQLModel persistés en base."""

from python_ia.models.admin import AdminUser
from python_ia.models.contact import ContactMessage
from python_ia.models.education import Education
from python_ia.models.experience import Experience
from python_ia.models.profile import Profile
from python_ia.models.project import Project, ProjectImage
from python_ia.models.site import SiteSettings
from python_ia.models.skill import Skill

__all__ = [
    "AdminUser",
    "ContactMessage",
    "Education",
    "Experience",
    "Profile",
    "Project",
    "ProjectImage",
    "SiteSettings",
    "Skill",
]
