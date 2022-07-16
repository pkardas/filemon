"""
Added 'active' column in 'collaborative_playlists'

Revision ID: 942985f3779a
Revises: 530651ef694d
Create Date: 2022-07-16 07:23:41.644269

"""
import sqlalchemy as sa
from alembic import op

revision = "942985f3779a"
down_revision = "530651ef694d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("collaborative_playlists", sa.Column("active", sa.Boolean(), nullable=True))
    op.execute("UPDATE collaborative_playlists SET active = TRUE")
    op.alter_column("collaborative_playlists", "active", nullable=False)


def downgrade() -> None:
    op.drop_column("collaborative_playlists", "active")
