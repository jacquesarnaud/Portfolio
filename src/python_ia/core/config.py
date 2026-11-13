"""Configuration centralisée, chargée depuis l'environnement."""

from functools import lru_cache
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Portfolio professionnel"
    debug: bool = False
    secret_key: str = "change-me-in-production"
    database_url: str = "sqlite+aiosqlite:///./portfolio.db"
    admin_username: str = "admin"
    admin_password: str = "change-me"
    jwt_secret_key: str = "change-jwt-secret-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 480
    uploads_dir: str = "uploads"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def async_database_url(self) -> str:
        """Retourne une URL compatible avec le moteur asyncpg.

        Cette conversion permet d'utiliser aussi bien l'URL Neon classique
        (`postgresql://`) que l'URL SQLAlchemy asynchrone.
        """
        # Nettoie les espaces accidentels souvent ajoutés lors d'un copier-coller.
        url = self.database_url.strip().replace("postgresql + async://", "postgresql+asyncpg://")
        url = url.replace("postgresql+async://", "postgresql+asyncpg://")

        # Les URLs SQLite utilisent trois slash après le schéma. Les traiter
        # avec urlsplit/urlunsplit les réduirait à un seul slash et rendrait
        # l'URL invalide (notamment pour la valeur par défaut locale).
        if url.startswith("sqlite"):
            return url

        if url.startswith("postgresql://"):
            url = "postgresql+asyncpg://" + url.removeprefix("postgresql://")
        elif url.startswith("postgres://"):
            url = "postgresql+asyncpg://" + url.removeprefix("postgres://")

        # asyncpg utilise `ssl=require`, alors que Neon fournit parfois
        # `sslmode=require` dans les URLs destinées au pilote psycopg.
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        if query.pop("sslmode", None) == "require":
            query["ssl"] = "require"
        if parts.hostname and parts.hostname.endswith("neon.tech") and "ssl" not in query:
            query["ssl"] = "require"
        return urlunsplit(parts._replace(query=urlencode(query)))


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
