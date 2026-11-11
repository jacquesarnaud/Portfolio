"""Messages reçus depuis le formulaire de contact."""

from datetime import datetime

from sqlmodel import Field, SQLModel

from python_ia.models.base import utc_now


class ContactMessage(SQLModel, table=True):
    __tablename__ = "contact_messages"

    id: int | None = Field(default=None, primary_key=True)
    sender_name: str = Field(max_length=150)
    sender_email: str = Field(index=True, max_length=255)
    subject: str = Field(default="", max_length=200)
    body: str = Field()
    is_read: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=utc_now, index=True)
