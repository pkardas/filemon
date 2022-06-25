from functools import cached_property

from src.gateways.auth import get_spotify
from src.models.spotify import (
    CreatedPlaylist,
    LovedTracks,
    RecentlyPlayed,
    SpotifyUser,
)


class Spotify:
    def __init__(self, spotify_code: str):
        self._spotify = get_spotify(spotify_code)

    @cached_property
    def user(self) -> SpotifyUser:
        return SpotifyUser(**self._spotify.me())

    def create_playlist(self, playlist_name: str) -> CreatedPlaylist:
        return CreatedPlaylist(**self._spotify.user_playlist_create(user=self.user.id, name=playlist_name, public=False, collaborative=True))

    def recently_played(self) -> RecentlyPlayed:
        return RecentlyPlayed(**self._spotify.current_user_recently_played())

    def loved_tracks(self, limit: int = 20, offset: int = 0) -> LovedTracks:
        return LovedTracks(**self._spotify.current_user_saved_tracks(limit=limit, offset=offset))
