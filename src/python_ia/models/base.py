"""Types partagés par les modèles persistants."""

from datetime import UTC, datetime


def utc_now() -> datetime:
    """Retourne une date UTC naïve compatible avec les colonnes PostgreSQL.

    Les colonnes actuelles sont des ``TIMESTAMP WITHOUT TIME ZONE``. La valeur
    reste UTC, mais sans ``tzinfo`` afin d'éviter les erreurs asyncpg lors de
    l'insertion.
    """
    return datetime.now(UTC).replace(tzinfo=None)
