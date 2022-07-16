from src.models.db import (
    get_table_name,
    Track,
)
from src.repositories.repository import Repository


class TracksRepository(Repository):
    table_name = get_table_name(Track)

    def add(self, track_uri: str, album_uri: str) -> None:
        self.session.execute(
            f"""
                INSERT INTO {self.table_name} (track_uri, album_uri)
                VALUES (:track_uri, :album_uri)
                ON CONFLICT DO NOTHING;
            """,  # type: ignore
            {"track_uri": track_uri, "album_uri": album_uri}
        )
