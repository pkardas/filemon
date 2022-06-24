from datetime import (
    date,
    datetime,
)
from typing import (
    Type,
    cast,
)

from sqlmodel import (
    Field,
    SQLModel,
)


class ListeningHistory(SQLModel, table=True):
    __tablename__ = "listening_history"
    __table_args__ = (
        {"postgresql_partition_by": "RANGE(played_at)"},
    )

    user_id: str = Field(primary_key=True, index=True)
    track_uri: str = Field(primary_key=True)
    played_at: datetime = Field(primary_key=True, index=True)


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(primary_key=True, index=True)
    spotify_code: str


def get_table_name(table: Type[SQLModel]) -> str:
    return cast(str, table.__tablename__)


def get_partition_name(table: Type[SQLModel], day: date) -> str:
    return f"{get_table_name(table)}_{day.isoformat().replace('-', '_')}"
