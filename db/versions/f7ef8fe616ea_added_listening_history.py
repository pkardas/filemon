"""
Added 'listening_history' table.

Revision ID: f7ef8fe616ea
Revises:
Create Date: 2022-06-11 17:38:55.706755

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

revision = "f7ef8fe616ea"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "listening_history",
        sa.Column("user_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("track_uri", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("played_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("user_id", "track_uri", "played_at"),
        postgresql_partition_by="RANGE(played_at)"
    )
    op.create_index(op.f("ix_listening_history_played_at"), "listening_history", ["played_at"], unique=False)
    op.create_index(op.f("ix_listening_history_user_id"), "listening_history", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_listening_history_user_id"), table_name="listening_history")
    op.drop_index(op.f("ix_listening_history_played_at"), table_name="listening_history")
    op.drop_table("listening_history")
