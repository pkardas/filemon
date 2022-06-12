import os
from datetime import (
    date,
    timedelta,
)
from functools import partial

from sqlmodel import (
    Session,
    create_engine,
)

from src.models.db import (
    ListeningHistory,
    partition_name,
    table_name,
)
from src.models.spotify import (
    RecentlyPlayedItem,
    User,
)

DATABASE_URL = os.environ.get("DATABASE_URL")


def default_session():
    return Session(create_engine(DATABASE_URL, echo=True))


class ListeningHistoryRepository:
    table_name = table_name(ListeningHistory)
    partition_name = partial(partition_name, ListeningHistory)

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, user: User, played_item: RecentlyPlayedItem) -> None:
        self._session.execute(
            f"""
                INSERT INTO {self.partition_name(played_item.played_at.date())} (user_id, track_uri, played_at)
                VALUES (:user_id, :track_uri, :played_at)
                ON CONFLICT DO NOTHING;
            """,  # type: ignore
            {"user_id": user.id, "track_uri": played_item.track.uri, "played_at": played_item.played_at}
        )

    def create_partition(self, day: date) -> None:
        self._session.execute(
            f"""
                CREATE TABLE IF NOT EXISTS {self.partition_name(day)} PARTITION OF {self.table_name}
                FOR VALUES FROM (:start) TO (:end);
            """,  # type: ignore
            {"start": day, "end": day + timedelta(days=1)}
        )

    def commit(self) -> None:
        self._session.commit()
        self._session.close()
