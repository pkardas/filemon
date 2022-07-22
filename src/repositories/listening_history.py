from datetime import (
    date,
    datetime,
    timedelta,
)
from functools import partial
from typing import List

from src.models.db import (
    ListeningHistory,
    get_partition_name,
    get_table_name,
    TopTrack,
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

    def top_played_tracks(self, user_id: str) -> List[TopTrack]:
        return [
            TopTrack(*row)
            for row in self.session.execute(
                # Get top played tracks for a user, max 2 tracks from one album:
                f"""
                    WITH top_tracks AS (
                        SELECT
                            listening_history.track_uri,
                            tracks.album_uri,
                            COUNT(*) AS frequency,
                            ROW_NUMBER() OVER(
                                PARTITION BY tracks.album_uri
                                ORDER BY COUNT(listening_history.track_uri) DESC
                            ) AS rank
                        FROM listening_history
                        LEFT OUTER JOIN tracks ON listening_history.track_uri = tracks.track_uri
                        WHERE user_id = :user_id AND played_at >= :played_at
                        GROUP BY listening_history.track_uri, tracks.album_uri
                    )
                    SELECT
                        track_uri,
                        frequency
                    FROM top_tracks
                    WHERE rank <= 2
                    ORDER BY frequency DESC
                    LIMIT 15;
                """,  # type: ignore
                {"user_id": user_id, "played_at": datetime.now() - timedelta(days=3)}
            ).all()
        ]

    def create_partition(self, day: date) -> None:
        self.session.execute(
            f"""
                CREATE TABLE IF NOT EXISTS {self.partition_name(day)} PARTITION OF {self.table_name}
                FOR VALUES FROM (:start) TO (:end);
            """,  # type: ignore
            {"start": day, "end": day + timedelta(days=1)}
        )
