from functools import cached_property
from typing import (
    Optional,
    List,
)

from src.gateways.spotipy import (
    get_spotipy,
    DbCacheHandler,
)
from src.models.spotify import (
    CreatedPlaylist,
    LovedTracks,
    RecentlyPlayed,
    SpotifyUser,
)


class Spotify:
    def __init__(self, spotify_code: str, user_id: Optional[str]):
        self._spotify = get_spotipy(spotify_code, user_id)

    @property
    def cache_handler(self) -> DbCacheHandler:
        return self._spotify.auth_manager.cache_handler

    @cached_property
    def user(self) -> SpotifyUser:
        return SpotifyUser(**self._spotify.me())

    def create_playlist(self, playlist_name: str) -> CreatedPlaylist:
        return CreatedPlaylist(**self._spotify.user_playlist_create(user=self.user.id, name=playlist_name, public=False, collaborative=True))

    def recently_played(self) -> RecentlyPlayed:
        return RecentlyPlayed(**self._spotify.current_user_recently_played())

    def loved_tracks(self, limit: int = 20, offset: int = 0) -> LovedTracks:
        return LovedTracks(**self._spotify.current_user_saved_tracks(limit=limit, offset=offset))

    def add_tracks(self, playlist_id: str, track_uris: List[str]) -> None:
        return self._spotify.playlist_add_items(playlist_id=playlist_id, items=track_uris)

    def get_playlist_tracks(self, playlist_id) -> LovedTracks:
        return LovedTracks(**self._spotify.playlist_items(playlist_id=playlist_id))

    def clear_playlist(self, playlist_id: str) -> None:
        while True:
            tracks = self.get_playlist_tracks(playlist_id)

            if not tracks.items:
                return

            self._spotify.playlist_remove_all_occurrences_of_items(
                playlist_id=playlist_id,
                items=[track.track.uri for track in tracks.items]
            )
