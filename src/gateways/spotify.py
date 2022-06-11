from functools import cached_property
from typing import Optional

from gateways.auth import get_spotify
from models.spotify import (
    LovedTracks,
    RecentlyPlayed,
    User,
)


class Spotify:
    def __init__(self, spotify_code: str):
        self._spotify = get_spotify(spotify_code)

    @cached_property
    def user(self) -> User:
        return User(**self._spotify.me())

    def create_playlist(self, playlist_name: str) -> None:
        self._spotify.user_playlist_create(user=self.user.id, name=playlist_name, public=False, collaborative=True)

    def recently_played(self, after: Optional[int] = None, before: Optional[int] = None) -> RecentlyPlayed:
        return RecentlyPlayed(**self._spotify.current_user_recently_played(after=after, before=before))

    def loved_tracks(self, limit: int = 20, offset: int = 0) -> LovedTracks:
        return LovedTracks(**self._spotify.current_user_saved_tracks(limit=limit, offset=offset))
