"""Formations et certifications."""

from datetime import date

from sqlmodel import Field, SQLModel


class Education(SQLModel, table=True):
    __tablename__ = "educations"

    id: int | None = Field(default=None, primary_key=True)
    institution: str = Field(max_length=180)
    title: str = Field(max_length=180)
    description: str = Field(default="")
    start_date: date | None = None
    end_date: date | None = None
    credential_url: str = Field(default="", max_length=500)
    is_certification: bool = Field(default=False, index=True)
    display_order: int = Field(default=0, index=True)
    is_published: bool = Field(default=True, index=True)
