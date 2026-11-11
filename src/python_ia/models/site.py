"""Paramètres globaux du site."""


from sqlmodel import Field, SQLModel


class SiteSettings(SQLModel, table=True):
    __tablename__ = "site_settings"

    id: int | None = Field(default=1, primary_key=True)
    site_name: str = Field(default="Portfolio professionnel", max_length=150)
    meta_description: str = Field(default="", max_length=320)
    accent_color: str = Field(default="#2563eb", max_length=20)
    contact_enabled: bool = Field(default=True)
