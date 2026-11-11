"""Compétences techniques affichées sur le portfolio."""


from sqlmodel import Field, SQLModel


class Skill(SQLModel, table=True):
    __tablename__ = "skills"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    category: str = Field(default="", max_length=100)
    proficiency: int | None = Field(default=None, ge=0, le=100)
    icon: str = Field(default="", max_length=100)
    display_order: int = Field(default=0, index=True)
    is_published: bool = Field(default=True, index=True)
