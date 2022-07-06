from random import shuffle

from src.gateways.spotify import Spotify
from src.models.bus import (
    AddPlaylist,
    AddUser,
    FetchListeningHistory,
    UpdatePartitions,
    UserPlayedMusic,
    UpdatePlaylists,
    UpdatePlaylist,
)
from src.models.errors import UserDoesNotExists
from src.repositories.unit_of_work import AbstractUnitOfWork


def add_user(command: AddUser, uow: AbstractUnitOfWork):
    # No 'user_id' yet:
    spotify = Spotify(spotify_code=command.spotify_code, user_id=None)

    with uow:
        uow.users.add(spotify.user.id, command.spotify_code)
        uow.commit()

    # 'user_id' known, update database:
    spotify.cache_handler.save_token_to_db(spotify.user.id)


def add_playlist(command: AddPlaylist, uow: AbstractUnitOfWork):
    with uow:
        if any(not uow.users.exists(user) for user in command.users):
            raise UserDoesNotExists("User does not exist")

        spotify = uow.users.get_spotify(command.first_user)
        response = spotify.create_playlist(command.playlist_name)

        uow.collaborative_playlists.add(command.users, response.id)
        uow.commit()


def update_partitions(command: UpdatePartitions, uow: AbstractUnitOfWork):
    with uow:
        uow.listening_history.create_partition(command.day)
        uow.commit()


def fetch_listening_history(command: FetchListeningHistory, uow: AbstractUnitOfWork):
    for user in uow.users.all_users:
        spotify = uow.users.get_spotify(user.id)
        recently_played = spotify.recently_played()

        uow.listening_history.queue.extend([
            UserPlayedMusic(
                user=spotify.user,
                recently_played=item
            )
            for item in recently_played.items
        ])


def update_playlists(command: UpdatePlaylists, uow: AbstractUnitOfWork):
    with uow:
        for playlist in uow.collaborative_playlists.get_all():
            uow.collaborative_playlists.queue.append(
                UpdatePlaylist(
                    playlist_id=playlist.playlist_id,
                    users=playlist.users
                )
            )
        uow.commit()


def update_playlist(command: UpdatePlaylist, uow: AbstractUnitOfWork):
    with uow:
        owner = uow.users.get_spotify(command.first_user)

        top_tracks = [
            track.track_uri
            for user_id in command.users
            for track in uow.listening_history.top_played_tracks(user_id)
        ]
        shuffle(top_tracks)

        owner.add_tracks(playlist_id=command.playlist_id, track_uris=top_tracks)

        uow.commit()


def user_played_music(event: UserPlayedMusic, uow: AbstractUnitOfWork):
    with uow:
        uow.listening_history.add(user_id=event.user.id, track_uri=event.recently_played.track.uri, played_at=event.recently_played.played_at)
        uow.commit()
