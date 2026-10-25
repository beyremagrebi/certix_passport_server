"""add is_active flag to users

Revision ID: 3d7a9b2c5f18
Revises: 8c4e1f7a2b90
Create Date: 2026-10-24

"""
from alembic import op
import sqlalchemy as sa


revision = "3d7a9b2c5f18"
down_revision = "8c4e1f7a2b90"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "is_active",
                sa.Boolean(),
                server_default=sa.true(),
                nullable=False,
            )
        )


def downgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("is_active")