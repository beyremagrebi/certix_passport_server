"""merge profile photo and user role migrations

Revision ID: 0175c26f816b
Revises: 7f8c2d9a4b11, e9001f9ca92e
Create Date: 2026-10-22 13:50:55.475994

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0175c26f816b'
down_revision = ('7f8c2d9a4b11', 'e9001f9ca92e')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
