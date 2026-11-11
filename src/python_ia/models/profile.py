"""Informations publiques du propriétaire du portfolio."""


from sqlmodel import Field, SQLModel


class Profile(SQLModel, table=True):
    """Profil principal ; la première version n'autorise qu'un profil."""

    __tablename__ = "profiles"

    id: int | None = Field(default=1, primary_key=True)
    full_name: str = Field(default="", max_length=150)
    headline: str = Field(default="", max_length=200)
    biography: str = Field(default="")
    email: str = Field(default="", max_length=255)
    phone: str = Field(default="", max_length=50)
    location: str = Field(default="", max_length=150)
    avatar_url: str = Field(default="", max_length=500)
    cv_url: str = Field(default="", max_length=500)
    github_url: str = Field(default="", max_length=500)
    linkedin_url: str = Field(default="", max_length=500)
    website_url: str = Field(default="", max_length=500)
    is_published: bool = Field(default=True)
