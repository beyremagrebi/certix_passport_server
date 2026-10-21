"""add profile photo reference

Revision ID: 7f8c2d9a4b11
Revises: 3481ba87b175
Create Date: 2026-10-21 11:16:21

"""
from alembic import op
import sqlalchemy as sa


revision = "7f8c2d9a4b11"
down_revision = "3481ba87b175"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users",
        sa.Column("profile_photo_ref", sa.String(length=255), nullable=True),
    )


def downgrade():
    op.drop_column("users", "profile_photo_ref")
