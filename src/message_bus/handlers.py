from src.gateways.spotify import Spotify
from src.models.bus import (
    AddUser,
    FetchListeningHistory,
    UpdatePartitions,
    UserPlayedMusic,
)
from src.repositories.unit_of_work import AbstractUnitOfWork


def add_user(command: AddUser, uow: AbstractUnitOfWork):
    spotify = Spotify(spotify_code=command.spotify_code)
    with uow:
        uow.users.add(spotify.user, command.spotify_code)
        uow.commit()


def update_partitions(command: UpdatePartitions, uow: AbstractUnitOfWork):
    with uow:
        uow.listening_history.create_partition(command.day)
        uow.commit()


def fetch_listening_history(command: FetchListeningHistory, uow: AbstractUnitOfWork):
    for user in uow.users.all_users:
        spotify = Spotify(spotify_code=user.spotify_code)
        recently_played = spotify.recently_played()

        uow.listening_history.queue.extend([
            UserPlayedMusic(
                user=spotify.user,
                recently_played=item
            )
            for item in recently_played.items
        ])


def user_played_music(event: UserPlayedMusic, uow: AbstractUnitOfWork):
    with uow:
        uow.listening_history.add(user=event.user, played_item=event.recently_played)
        uow.commit()
