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

from src.repositories.listening_history import ListeningHistoryRepository

DATABASE_URL = os.environ.get("DATABASE_URL")


def default_session():
    return Session(create_engine(DATABASE_URL, echo=True))


class AbstractUnitOfWork(ABC):
    listening_history: ListeningHistoryRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def collect_new_messages(self):
        for item in self.listening_history.queue:
            yield item
        self.listening_history.queue = []

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
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _rollback(self):
        self.session.rollback()

    def _commit(self):
        self.session.commit()
