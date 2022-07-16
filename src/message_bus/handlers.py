import itertools
from typing import Dict

from src.gateways.spotify import Spotify
from src.models.errors import UserDoesNotExists
from src.models.messages import (
    AddPlaylist,
    AddUser,
    FetchListeningHistory,
    UpdatePartitions,
    UserPlayedMusic,
    UpdatePlaylists,
    UpdatePlaylist,
    AddUserToken,
    GetUserToken,
)
from src.repositories.unit_of_work import AbstractUnitOfWork


def add_user(command: AddUser, uow: AbstractUnitOfWork):
    # No 'user_id' yet:
    spotify = Spotify(spotify_code=command.spotify_code, user_id=None)

    with uow:
        uow.users.add(spotify.user.id, spotify.user.display_name, command.spotify_code)
        uow.commit()

    # 'user_id' known, update database:
    uow.users.queue.append(
        AddUserToken(
            user_id=spotify.user.id,
            token_info=spotify.token_info
        )
    )


def add_user_token(command: AddUserToken, uow: AbstractUnitOfWork):
    with uow:
        uow.users.add_token(command.user_id, command.token_info)
        uow.commit()


def get_user_token(command: GetUserToken, uow: AbstractUnitOfWork) -> Dict[str, str]:
    with uow:
        return uow.users.get_token(command.user_id)


def add_playlist(command: AddPlaylist, uow: AbstractUnitOfWork):
    with uow:
        if any(not uow.users.exists(user) for user in command.users):
            raise UserDoesNotExists("User does not exist")

        spotify = uow.users.get_spotify(user_id=uow.users.get_user_id(command.first_user))
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
        user_id = uow.users.get_user_id(command.first_user)
        owner = uow.users.get_spotify(user_id=user_id)

        users_top_tracks = [
            (track.track_uri for track in uow.listening_history.top_played_tracks(uow.users.get_user_id(user_name)))
            for user_name in command.users
        ]

        owner.clear_playlist(command.playlist_id)
        owner.add_tracks(
            playlist_id=command.playlist_id,
            # Overlap songs:
            track_uris=list(itertools.chain(*zip(*users_top_tracks)))
        )

        uow.commit()


def user_played_music(event: UserPlayedMusic, uow: AbstractUnitOfWork):
    with uow:
        uow.listening_history.add(user_id=event.user.id, track_uri=event.recently_played.track.uri, played_at=event.recently_played.played_at)
        uow.tracks.add(track_uri=event.recently_played.track.uri, album_uri=event.recently_played.track.album.uri)

        uow.commit()
