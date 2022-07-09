"""
Add 'name' column to 'users'

Revision ID: 530651ef694d
Revises: d3c5fdb096ad
Create Date: 2022-07-09 12:31:07.528409

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

revision = "530651ef694d"
down_revision = "d3c5fdb096ad"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.create_index(op.f("ix_users_name"), "users", ["name"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_users_name"), table_name="users")
    op.drop_column("users", "name")
