from dataclasses import dataclass
from datetime import (
    date,
    datetime,
)
from typing import (
    List,
    Type,
    cast,
)

from sqlalchemy import (
    ARRAY,
    Column,
    String,
)
from sqlalchemy.dialects.postgresql import JSONB
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


@dataclass
class TopTrack:
    track_uri: str
    count: int


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(primary_key=True, index=True)
    spotify_code: str
    token: str = Field(sa_column=Column(JSONB), nullable=True)


class CollaborativePlaylist(SQLModel, table=True):
    __tablename__ = "collaborative_playlists"

    playlist_id: str = Field(primary_key=True, index=True)
    users: List[str] = Field(sa_column=Column(ARRAY(String)))


def get_table_name(table: Type[SQLModel]) -> str:
    return cast(str, table.__tablename__)


def get_partition_name(table: Type[SQLModel], day: date) -> str:
    return f"{get_table_name(table)}_{day.isoformat().replace('-', '_')}"
