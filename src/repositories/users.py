import json
from typing import (
    List,
    Dict,
    cast,
)

from sqlmodel import select

from src.gateways.spotify import Spotify
from src.models.db import (
    User,
    get_table_name,
)
from src.repositories.repository import Repository


class UsersRepository(Repository):
    table_name = get_table_name(User)

    @property
    def all_users(self) -> List[User]:
        return self.session.exec(select(User)).all()

    def add(self, user_id: str, user_name: str, spotify_code: str) -> None:
        self.session.execute(
            f"""
                INSERT INTO {self.table_name} (id, name, spotify_code)
                VALUES (:user_id, :name, :spotify_code)
                ON CONFLICT (id) DO
                    UPDATE SET spotify_code = :spotify_code
            """,  # type: ignore
            {"user_id": user_id, "name": user_name, "spotify_code": spotify_code}
        )

    def exists(self, user_id: str) -> bool:
        return any(self.session.exec(select(User).where(User.id == user_id)).all())

    def get_spotify(self, user_id: str) -> Spotify:
        user = self.session.exec(select(User).where(User.id == user_id)).one()
        return Spotify(spotify_code=user.spotify_code, user_id=user_id)

    def add_token(self, user_id: str, token: Dict[str, str]):
        self.session.execute(
            f"""
                UPDATE {self.table_name}
                SET token = :token
                WHERE id = :user_id
            """,  # type: ignore
            {"user_id": user_id, "token": json.dumps(token)}
        )

    def get_token(self, user_id: str) -> Dict[str, str]:
        return cast(Dict[str, str], self.session.exec(select(User.token).where(User.id == user_id)).one())
