from fakes.fake_repositories import (
    FakeCollaborativePlaylistsRepository,
    FakeListeningHistoryRepository,
    FakeUsersRepository,
)
from src.repositories.unit_of_work import AbstractUnitOfWork


class FakeUnitOfWork(AbstractUnitOfWork):
    def __enter__(self):
        self.listening_history = FakeListeningHistoryRepository()
        self.users = FakeUsersRepository()
        self.collaborative_playlists = FakeCollaborativePlaylistsRepository()
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)

    def _rollback(self):
        pass

    def _commit(self):
        pass
