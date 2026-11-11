"""Schémas d'entrée et de sortie des API CRUD."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ProfileUpdate(SchemaBase):
    full_name: str = Field(max_length=150)
    headline: str = Field(max_length=200)
    biography: str
    email: str = Field(default="", max_length=255)
    phone: str = Field(default="", max_length=50)
    location: str = Field(default="", max_length=150)
    avatar_url: str = Field(default="", max_length=500)
    cv_url: str = Field(default="", max_length=500)
    github_url: str = Field(default="", max_length=500)
    linkedin_url: str = Field(default="", max_length=500)
    website_url: str = Field(default="", max_length=500)
    is_published: bool = True


class ProfileRead(ProfileUpdate):
    id: int


class SkillCreate(SchemaBase):
    name: str = Field(max_length=100)
    category: str = Field(default="", max_length=100)
    proficiency: int | None = Field(default=None, ge=0, le=100)
    icon: str = Field(default="", max_length=100)
    display_order: int = 0
    is_published: bool = True


class SkillRead(SkillCreate):
    id: int


class ProjectCreate(SchemaBase):
    title: str = Field(max_length=180)
    slug: str = Field(max_length=200)
    short_description: str = Field(default="", max_length=500)
    description: str = ""
    technologies: str = Field(default="", max_length=500)
    repository_url: str = Field(default="", max_length=500)
    live_url: str = Field(default="", max_length=500)
    cover_image_url: str = Field(default="", max_length=500)
    display_order: int = 0
    is_featured: bool = False
    is_published: bool = True


class ProjectRead(ProjectCreate):
    id: int
    created_at: datetime
    updated_at: datetime


class ProjectImageCreate(SchemaBase):
    image_url: str = Field(max_length=500)
    alt_text: str = Field(default="", max_length=200)
    display_order: int = 0


class ProjectImageRead(ProjectImageCreate):
    id: int
    project_id: int


class ExperienceCreate(SchemaBase):
    company: str = Field(max_length=180)
    position: str = Field(max_length=180)
    location: str = Field(default="", max_length=150)
    description: str = ""
    start_date: date
    end_date: date | None = None
    is_current: bool = False
    display_order: int = 0
    is_published: bool = True


class ExperienceRead(ExperienceCreate):
    id: int


class EducationCreate(SchemaBase):
    institution: str = Field(max_length=180)
    title: str = Field(max_length=180)
    description: str = ""
    start_date: date | None = None
    end_date: date | None = None
    credential_url: str = Field(default="", max_length=500)
    is_certification: bool = False
    display_order: int = 0
    is_published: bool = True


class EducationRead(EducationCreate):
    id: int


class ContactMessageCreate(SchemaBase):
    sender_name: str = Field(min_length=2, max_length=150)
    sender_email: str = Field(max_length=255)
    subject: str = Field(default="", max_length=200)
    body: str = Field(min_length=1)


class ContactMessageRead(ContactMessageCreate):
    id: int
    is_read: bool
    created_at: datetime
