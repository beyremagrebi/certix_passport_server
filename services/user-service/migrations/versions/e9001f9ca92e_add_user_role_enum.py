"""Add user role enum

Revision ID: e9001f9ca92e
Revises: 3481ba87b175
Create Date: 2026-10-21 13:13:59.804197
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "e9001f9ca92e"
down_revision = "3481ba87b175"
branch_labels = None
depends_on = None


def upgrade():
    # Create PostgreSQL enum type before using it.
    role_enum = postgresql.ENUM(
        "student",
        "admin",
        name="user_role",
    )
    role_enum.create(op.get_bind(), checkfirst=True)

    # Add role column to users.
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "role",
                postgresql.ENUM(
                    "student",
                    "admin",
                    name="user_role",
                    create_type=False,
                ),
                server_default=sa.text("'student'"),
                nullable=False,
            )
        )


def downgrade():
    # Drop role column first, then its enum type.
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("role")

    postgresql.ENUM(
        "student",
        "admin",
        name="user_role",
    ).drop(op.get_bind(), checkfirst=True)
