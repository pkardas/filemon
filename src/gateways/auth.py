from typing import List

from spotipy import (
    Spotify,
    SpotifyOAuth,
    SpotifyStateError,
)

SCOPE = ["user-library-read", "user-read-recently-played", "playlist-modify-private"]


class FilemonSpotifyOAuth(SpotifyOAuth):
    def __init__(self, scope: List[str], spotify_response: str):
        self._spotify_response = spotify_response
        super().__init__(scope=scope, open_browser=False)

    def _get_auth_response_interactive(self, open_browser=False):
        """
        Override 'SpotifyOAuth._get_auth_response_interactive' in order to disable 'input' prompt,
        which is not need in the backend application.
        """
        state, code = SpotifyOAuth.parse_auth_response_url(self._spotify_response)
        if self.state is not None and self.state != state:
            raise SpotifyStateError(self.state, state)
        return code


def get_spotify(spotify_code: str) -> Spotify:
    auth = FilemonSpotifyOAuth(scope=SCOPE, spotify_response=spotify_code)
    return Spotify(auth_manager=auth)
