from typing import List

from sqlmodel import select

from src.models.db import (
    User,
    get_table_name,
)
from src.models.spotify import SpotifyUser
from src.repositories.repository import Repository


class UsersRepository(Repository):
    table_name = get_table_name(User)

    def add(self, user: SpotifyUser, spotify_code: str) -> None:
        self.session.execute(
            """
                INSERT INTO users (id, spotify_code)
                VALUES (:user_id, :spotify_code)
                ON CONFLICT (id) DO
                    UPDATE SET spotify_code = :spotify_code
            """,  # type: ignore
            {"user_id": user.id, "spotify_code": spotify_code}
        )

    @property
    def all_users(self) -> List[User]:
        return self.session.exec(select(User)).all()
