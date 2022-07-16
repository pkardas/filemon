from __future__ import annotations

import os
from abc import (
    ABC,
    abstractmethod,
)
from typing import Optional

from sqlmodel import (
    Session,
    create_engine,
)

from repositories.tracks import TracksRepository
from src.repositories.collaborative_playlists import CollaborativePlaylistsRepository
from src.repositories.listening_history import ListeningHistoryRepository
from src.repositories.users import UsersRepository

DATABASE_URL = os.environ.get("DATABASE_URL")


def default_session():
    return Session(create_engine(DATABASE_URL, echo=True))


class AbstractUnitOfWork(ABC):
    listening_history: ListeningHistoryRepository
    users: UsersRepository
    collaborative_playlists: CollaborativePlaylistsRepository
    tracks: TracksRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def collect_new_messages(self):
        for item in self.listening_history.queue:
            yield item
        self.listening_history.queue = []

        for item in self.users.queue:
            yield item
        self.users.queue = []

        for item in self.collaborative_playlists.queue:
            yield item
        self.collaborative_playlists.queue = []

        for item in self.tracks.queue:
            yield item
        self.tracks.queue = []

    def commit(self):
        self._commit()

    def rollback(self):
        self._rollback()

    @abstractmethod
    def _rollback(self):
        raise NotImplementedError

    @abstractmethod
    def _commit(self):
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session: Optional[Session] = None):
        # 'default_session()' can not be in the '__init__' because it would be evaluated only once:
        self.session = session if session else default_session()

    def __enter__(self):
        self.listening_history = ListeningHistoryRepository(self.session)
        self.users = UsersRepository(self.session)
        self.collaborative_playlists = CollaborativePlaylistsRepository(self.session)
        self.tracks = TracksRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _rollback(self):
        self.session.rollback()

    def _commit(self):
        self.session.commit()
