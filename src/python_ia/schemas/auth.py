"""Schémas de l'authentification API."""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Identifiants envoyés par l'administrateur."""

    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=255)


class TokenResponse(BaseModel):
    """Jeton retourné après une authentification réussie."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
