"""
Added 'tracks' table

Revision ID: fbed923d0bd4
Revises: 942985f3779a
Create Date: 2022-07-16 08:00:07.027090

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

revision = "fbed923d0bd4"
down_revision = "942985f3779a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tracks",
        sa.Column("track_uri", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("album_uri", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("track_uri", "album_uri")
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_tracks_track_uri"), table_name="tracks")
    op.drop_index(op.f("ix_tracks_album_uri"), table_name="tracks")
    op.drop_table("tracks")
