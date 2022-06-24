"""
Added 'users' table

Revision ID: 82374bbd5723
Revises: f7ef8fe616ea
Create Date: 2022-06-24 20:11:21.415954

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

revision = "82374bbd5723"
down_revision = "f7ef8fe616ea"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("spotify_code", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
