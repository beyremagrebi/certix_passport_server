"""add student profile fields

Revision ID: a1b2c3d4e5f6
Revises: 0175c26f816b
Create Date: 2026-10-22

"""
from alembic import op
import sqlalchemy as sa


revision = "a1b2c3d4e5f6"
down_revision = "0175c26f816b"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("bio", sa.String(length=300), nullable=True))
        batch_op.add_column(
            sa.Column("study_program", sa.String(length=100), nullable=True)
        )
        batch_op.add_column(sa.Column("level", sa.String(length=50), nullable=True))
        batch_op.add_column(
            sa.Column("linkedin_url", sa.String(length=255), nullable=True)
        )
        batch_op.add_column(
            sa.Column("github_url", sa.String(length=255), nullable=True)
        )


def downgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("github_url")
        batch_op.drop_column("linkedin_url")
        batch_op.drop_column("level")
        batch_op.drop_column("study_program")
        batch_op.drop_column("bio")
