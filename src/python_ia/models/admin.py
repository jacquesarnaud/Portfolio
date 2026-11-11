"""Compte administrateur unique."""

from datetime import datetime

from sqlmodel import Field, SQLModel

from python_ia.models.base import utc_now


class AdminUser(SQLModel, table=True):
    __tablename__ = "admin_users"

    id: int | None = Field(default=1, primary_key=True)
    username: str = Field(unique=True, index=True, max_length=100)
    password_hash: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    last_login_at: datetime | None = None
    created_at: datetime = Field(default_factory=utc_now)
