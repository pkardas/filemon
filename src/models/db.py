from datetime import datetime

from sqlalchemy import UniqueConstraint
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
