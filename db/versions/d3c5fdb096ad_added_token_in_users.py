"""
Added 'token' column in 'users'

Revision ID: d3c5fdb096ad
Revises: 82b4960c2387
Create Date: 2022-07-06 19:45:45.991705

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "d3c5fdb096ad"
down_revision = "82b4960c2387"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("token", postgresql.JSONB(astext_type=sa.Text()), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "token")
