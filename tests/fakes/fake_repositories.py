from datetime import datetime
from typing import List

from src.models.db import (
    CollaborativePlaylist,
    ListeningHistory,
    User,
)
from src.repositories.collaborative_playlists import CollaborativePlaylistsRepository
from src.repositories.listening_history import ListeningHistoryRepository
from src.repositories.users import UsersRepository


class FakeUsersRepository(UsersRepository):
    def __init__(self):
        self._users = []
        super().__init__(session=...)

    @property
    def all_users(self) -> List[User]:
        return self._users

    def add(self, user_id: str, user_name: str, spotify_code: str) -> None:
        self._users.append(User(id=user_id, name=user_name, spotify_code=spotify_code))


class FakeListeningHistoryRepository(ListeningHistoryRepository):
    def __init__(self):
        self._listening_history = []
        super().__init__(session=...)

    def add(self, user_id: str, track_uri: str, played_at: datetime) -> None:
        self._listening_history.append(ListeningHistory(user_id=user_id, track_uri=track_uri, played_at=played_at))


class FakeCollaborativePlaylistsRepository(CollaborativePlaylistsRepository):
    def __init__(self):
        self._collaborative_playlists = []
        super().__init__(session=...)

    def add(self, users: List[str], playlist_id: str) -> None:
        self._collaborative_playlists.append(CollaborativePlaylist(playlist_id=playlist_id, users=users))
