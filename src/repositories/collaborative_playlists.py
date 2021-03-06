from typing import List

from sqlmodel import select

from src.models.db import (
    CollaborativePlaylist,
    get_table_name,
)
from src.repositories.repository import Repository


class CollaborativePlaylistsRepository(Repository):
    table_name = get_table_name(CollaborativePlaylist)

    def add(self, users: List[str], playlist_id: str) -> None:
        self.session.execute(
            f"""
                INSERT INTO {self.table_name} (playlist_id, users, active)
                VALUES (:playlist_id, :users, TRUE);
            """,  # type: ignore
            {"playlist_id": playlist_id, "users": users}
        )

    def get_all(self) -> List[CollaborativePlaylist]:
        return self.session.exec(select(CollaborativePlaylist).where(CollaborativePlaylist.active == True)).all()  # noqa: E712, ORM does not work with '... is True'
