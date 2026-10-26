"""add email confirmation fields and tokens

Revision ID: 4f2c8a9e1b30
Revises: 3d7a9b2c5f18
"""

from alembic import op
import sqlalchemy as sa


revision = "4f2c8a9e1b30"
down_revision = "3d7a9b2c5f18"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "email_confirmed",
                sa.Boolean(),
                server_default=sa.true(),
                nullable=False,
            )
        )

    op.create_table(
        "email_confirmation_tokens",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token_hash"),
    )
    op.create_index(
        "ix_email_confirmation_tokens_user_id",
        "email_confirmation_tokens",
        ["user_id"],
    )
    op.create_index(
        "ix_email_confirmation_tokens_token_hash",
        "email_confirmation_tokens",
        ["token_hash"],
    )
    op.create_index(
        "ix_email_confirmation_tokens_expires_at",
        "email_confirmation_tokens",
        ["expires_at"],
    )


def downgrade():
    op.drop_index(
        "ix_email_confirmation_tokens_expires_at",
        table_name="email_confirmation_tokens",
    )
    op.drop_index(
        "ix_email_confirmation_tokens_token_hash",
        table_name="email_confirmation_tokens",
    )
    op.drop_index(
        "ix_email_confirmation_tokens_user_id",
        table_name="email_confirmation_tokens",
    )
    op.drop_table("email_confirmation_tokens")
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("email_confirmed")
