from datetime import (
    date,
    datetime,
    timedelta,
)
from functools import partial

from src.models.db import (
    ListeningHistory,
    get_partition_name,
    get_table_name,
)
from src.repositories.repository import Repository


class ListeningHistoryRepository(Repository):
    table_name = get_table_name(ListeningHistory)
    partition_name = partial(get_partition_name, ListeningHistory)

    def add(self, user_id: str, track_uri: str, played_at: datetime) -> None:
        self.session.execute(
            f"""
                INSERT INTO {self.partition_name(played_at.date())} (user_id, track_uri, played_at)
                VALUES (:user_id, :track_uri, :played_at)
                ON CONFLICT DO NOTHING;
            """,  # type: ignore
            {"user_id": user_id, "track_uri": track_uri, "played_at": played_at}
        )

    def create_partition(self, day: date) -> None:
        self.session.execute(
            f"""
                CREATE TABLE IF NOT EXISTS {self.partition_name(day)} PARTITION OF {self.table_name}
                FOR VALUES FROM (:start) TO (:end);
            """,  # type: ignore
            {"start": day, "end": day + timedelta(days=1)}
        )
