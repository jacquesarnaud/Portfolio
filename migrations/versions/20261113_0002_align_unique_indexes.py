"""align unique indexes with SQLModel metadata

Revision ID: 20261113_0002
Revises: 20261111_0001
Create Date: 2026-11-13
"""

from alembic import op


revision = "20261113_0002"
down_revision = "20261111_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Replace redundant non-unique indexes with the declared unique ones."""
    op.drop_index("ix_admin_users_username", table_name="admin_users")
    op.create_index("ix_admin_users_username", "admin_users", ["username"], unique=True)
    op.drop_index("ix_projects_slug", table_name="projects")
    op.create_index("ix_projects_slug", "projects", ["slug"], unique=True)


def downgrade() -> None:
    """Restore the indexes created by the initial schema revision."""
    op.drop_index("ix_projects_slug", table_name="projects")
    op.create_index("ix_projects_slug", "projects", ["slug"], unique=False)
    op.drop_index("ix_admin_users_username", table_name="admin_users")
    op.create_index("ix_admin_users_username", "admin_users", ["username"], unique=False)
