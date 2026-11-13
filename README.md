# Portfolio professionnel

Application web de portfolio construite avec FastAPI, Jinja2, HTMX, SQLModel,
PostgreSQL (Neon) et Alembic.

## Architecture

```text
src/python_ia/
├── api/          # routeurs HTTP et dépendances web
├── core/         # configuration et base de données
├── models/       # modèles SQLModel
├── schemas/      # schémas de validation Pydantic
├── services/     # logique métier et cas d'utilisation
└── web/          # ancien rendu serveur conservé pour référence
migrations/      # versions Alembic
```

## Démarrage local

```bash
cp .env.example .env
uv sync
uv run alembic upgrade head
uv run python-ia
```

`DATABASE_URL` doit pointer vers Neon en production. La valeur par défaut
utilise SQLite asynchrone afin de démarrer l'application sans service externe ;
la migration Alembic doit être appliquée avant le premier démarrage. SQLite ne
remplace pas PostgreSQL dans l'environnement cible.

## Démarrage avec Docker

Le fichier `.env` est transmis au conteneur par Docker Compose. Il n'est pas
copié dans l'image et reste ignoré par Git.

```bash
docker compose up --build
```

L'application est disponible sur `http://localhost:8000` et sa documentation
sur `http://localhost:8000/docs`. FastAPI rend les templates Jinja2 et sert les
fichiers statiques ; HTMX est disponible pour les interactions dynamiques.
