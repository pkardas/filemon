"""
Added 'collaborative_playlists' table

Revision ID: 82b4960c2387
Revises: 82374bbd5723
Create Date: 2022-06-25 10:02:12.598007

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

revision = "82b4960c2387"
down_revision = "82374bbd5723"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "collaborative_playlists",
        sa.Column("users", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("playlist_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("playlist_id")
    )
    op.create_index(op.f("ix_collaborative_playlists_playlist_id"), "collaborative_playlists", ["playlist_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_collaborative_playlists_playlist_id"), table_name="collaborative_playlists")
    op.drop_table("collaborative_playlists")
