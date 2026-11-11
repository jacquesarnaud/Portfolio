"""Expériences professionnelles."""

from datetime import date

from sqlmodel import Field, SQLModel


class Experience(SQLModel, table=True):
    __tablename__ = "experiences"

    id: int | None = Field(default=None, primary_key=True)
    company: str = Field(max_length=180)
    position: str = Field(max_length=180)
    location: str = Field(default="", max_length=150)
    description: str = Field(default="")
    start_date: date
    end_date: date | None = None
    is_current: bool = Field(default=False)
    display_order: int = Field(default=0, index=True)
    is_published: bool = Field(default=True, index=True)
