"""add public slug and public link flag to users

Revision ID: 8c4e1f7a2b90
Revises: a1b2c3d4e5f6
Create Date: 2026-10-24

"""
import re
import secrets
import unicodedata

from alembic import op
import sqlalchemy as sa


revision = "8c4e1f7a2b90"
down_revision = "a1b2c3d4e5f6"
branch_labels = None
depends_on = None


# Frozen copy of app.utils.slug. Migrations must never import application
# code: that code changes over time, while a migration must stay identical.
_NON_ALPHANUMERIC = re.compile(r"[^a-z0-9]+")


def _generate_slug(first_name, last_name):
    name = unicodedata.normalize("NFKD", f"{first_name} {last_name}")
    name = name.encode("ascii", "ignore").decode("ascii").lower()
    base = _NON_ALPHANUMERIC.sub("-", name).strip("-")[:60].strip("-")
    return f"{base or 'member'}-{secrets.randbelow(10**6):06d}"


def _backfill_public_slugs():
    """Give a slug to the users that existed before this migration."""
    bind = op.get_bind()
    rows = bind.execute(
        sa.text("SELECT id, first_name, last_name FROM users")
    ).fetchall()

    used = set()
    for user_id, first_name, last_name in rows:
        slug = _generate_slug(first_name, last_name)
        while slug in used:
            slug = _generate_slug(first_name, last_name)
        used.add(slug)

        bind.execute(
            sa.text("UPDATE users SET public_slug = :slug WHERE id = :id"),
            {"slug": slug, "id": user_id},
        )


def upgrade():
    # 1. Add the columns. The slug is nullable only until the backfill ran.
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("public_slug", sa.String(length=80), nullable=True)
        )
        batch_op.add_column(
            sa.Column(
                "public_link_active",
                sa.Boolean(),
                server_default=sa.true(),
                nullable=False,
            )
        )

    # 2. Fill the slug of existing users.
    _backfill_public_slugs()

    # 3. Enforce the final constraints.
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.alter_column(
            "public_slug",
            existing_type=sa.String(length=80),
            nullable=False,
        )
        batch_op.create_index(
            batch_op.f("ix_users_public_slug"), ["public_slug"], unique=True
        )


def downgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_users_public_slug"))
        batch_op.drop_column("public_link_active")
        batch_op.drop_column("public_slug")
