"""create portfolio models

Revision ID: 20261111_0001
Revises:
Create Date: 2026-11-11
"""

import sqlalchemy as sa
from alembic import op

revision = "20261111_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("full_name", sa.String(length=150), nullable=False),
        sa.Column("headline", sa.String(length=200), nullable=False),
        sa.Column("biography", sa.Text(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=50), nullable=False),
        sa.Column("location", sa.String(length=150), nullable=False),
        sa.Column("avatar_url", sa.String(length=500), nullable=False),
        sa.Column("cv_url", sa.String(length=500), nullable=False),
        sa.Column("github_url", sa.String(length=500), nullable=False),
        sa.Column("linkedin_url", sa.String(length=500), nullable=False),
        sa.Column("website_url", sa.String(length=500), nullable=False),
        sa.Column("is_published", sa.Boolean(), nullable=False),
    )
    op.create_table(
        "skills",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("proficiency", sa.Integer(), nullable=True),
        sa.Column("icon", sa.String(length=100), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("is_published", sa.Boolean(), nullable=False),
    )
    op.create_index("ix_skills_name", "skills", ["name"])
    op.create_index("ix_skills_display_order", "skills", ["display_order"])
    op.create_index("ix_skills_is_published", "skills", ["is_published"])
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=180), nullable=False),
        sa.Column("slug", sa.String(length=200), nullable=False, unique=True),
        sa.Column("short_description", sa.String(length=500), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("technologies", sa.String(length=500), nullable=False),
        sa.Column("repository_url", sa.String(length=500), nullable=False),
        sa.Column("live_url", sa.String(length=500), nullable=False),
        sa.Column("cover_image_url", sa.String(length=500), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("is_featured", sa.Boolean(), nullable=False),
        sa.Column("is_published", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_projects_slug", "projects", ["slug"])
    op.create_index("ix_projects_display_order", "projects", ["display_order"])
    op.create_index("ix_projects_is_featured", "projects", ["is_featured"])
    op.create_index("ix_projects_is_published", "projects", ["is_published"])
    op.create_table(
        "project_images",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("image_url", sa.String(length=500), nullable=False),
        sa.Column("alt_text", sa.String(length=200), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
    )
    op.create_index("ix_project_images_project_id", "project_images", ["project_id"])
    op.create_table(
        "experiences",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company", sa.String(length=180), nullable=False),
        sa.Column("position", sa.String(length=180), nullable=False),
        sa.Column("location", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("is_current", sa.Boolean(), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("is_published", sa.Boolean(), nullable=False),
    )
    op.create_index("ix_experiences_display_order", "experiences", ["display_order"])
    op.create_index("ix_experiences_is_published", "experiences", ["is_published"])
    op.create_table(
        "educations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("institution", sa.String(length=180), nullable=False),
        sa.Column("title", sa.String(length=180), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("credential_url", sa.String(length=500), nullable=False),
        sa.Column("is_certification", sa.Boolean(), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("is_published", sa.Boolean(), nullable=False),
    )
    op.create_index("ix_educations_is_certification", "educations", ["is_certification"])
    op.create_index("ix_educations_display_order", "educations", ["display_order"])
    op.create_index("ix_educations_is_published", "educations", ["is_published"])
    op.create_table(
        "contact_messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("sender_name", sa.String(length=150), nullable=False),
        sa.Column("sender_email", sa.String(length=255), nullable=False),
        sa.Column("subject", sa.String(length=200), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("is_read", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_contact_messages_sender_email", "contact_messages", ["sender_email"])
    op.create_index("ix_contact_messages_is_read", "contact_messages", ["is_read"])
    op.create_index("ix_contact_messages_created_at", "contact_messages", ["created_at"])
    op.create_table(
        "admin_users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(length=100), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_admin_users_username", "admin_users", ["username"])
    op.create_table(
        "site_settings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("site_name", sa.String(length=150), nullable=False),
        sa.Column("meta_description", sa.String(length=320), nullable=False),
        sa.Column("accent_color", sa.String(length=20), nullable=False),
        sa.Column("contact_enabled", sa.Boolean(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("site_settings")
    op.drop_index("ix_admin_users_username", table_name="admin_users")
    op.drop_table("admin_users")
    op.drop_index("ix_contact_messages_created_at", table_name="contact_messages")
    op.drop_index("ix_contact_messages_is_read", table_name="contact_messages")
    op.drop_index("ix_contact_messages_sender_email", table_name="contact_messages")
    op.drop_table("contact_messages")
    op.drop_index("ix_educations_is_published", table_name="educations")
    op.drop_index("ix_educations_display_order", table_name="educations")
    op.drop_index("ix_educations_is_certification", table_name="educations")
    op.drop_table("educations")
    op.drop_index("ix_experiences_is_published", table_name="experiences")
    op.drop_index("ix_experiences_display_order", table_name="experiences")
    op.drop_table("experiences")
    op.drop_index("ix_project_images_project_id", table_name="project_images")
    op.drop_table("project_images")
    op.drop_index("ix_projects_is_published", table_name="projects")
    op.drop_index("ix_projects_is_featured", table_name="projects")
    op.drop_index("ix_projects_display_order", table_name="projects")
    op.drop_index("ix_projects_slug", table_name="projects")
    op.drop_table("projects")
    op.drop_index("ix_skills_is_published", table_name="skills")
    op.drop_index("ix_skills_display_order", table_name="skills")
    op.drop_index("ix_skills_name", table_name="skills")
    op.drop_table("skills")
    op.drop_table("profiles")
