"""Projets et médias associés."""

from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, Relationship, SQLModel

from python_ia.models.base import utc_now


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=180)
    slug: str = Field(index=True, unique=True, max_length=200)
    short_description: str = Field(default="", max_length=500)
    description: str = Field(default="")
    technologies: str = Field(default="", max_length=500)
    repository_url: str = Field(default="", max_length=500)
    live_url: str = Field(default="", max_length=500)
    cover_image_url: str = Field(default="", max_length=500)
    display_order: int = Field(default=0, index=True)
    is_featured: bool = Field(default=False, index=True)
    is_published: bool = Field(default=True, index=True)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    images: list["ProjectImage"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class ProjectImage(SQLModel, table=True):
    __tablename__ = "project_images"

    id: int | None = Field(default=None, primary_key=True)
    project_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("projects.id", ondelete="CASCADE"),
            index=True,
            nullable=False,
        )
    )
    image_url: str = Field(max_length=500)
    alt_text: str = Field(default="", max_length=200)
    display_order: int = Field(default=0)

    project: Project | None = Relationship(back_populates="images")
