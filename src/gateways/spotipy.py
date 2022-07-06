from typing import (
    List,
    Dict,
    Optional,
)

from spotipy import (
    Spotify,
    SpotifyOAuth,
    SpotifyStateError,
    CacheHandler,
)

SCOPE = ["playlist-modify-private", "user-library-read", "user-read-recently-played"]


class DbCacheHandler(CacheHandler):
    def __init__(self, user_id: Optional[str]) -> None:
        self.token_info = None
        self._user_id = user_id

    def get_cached_token(self) -> Optional[Dict[str, str]]:
        if self.token_info:
            return self.token_info

        if not self._user_id:
            return None

        from src.repositories.unit_of_work import default_session
        from src.repositories.users import UsersRepository

        with default_session() as session:
            return UsersRepository(session).get_token(self._user_id)

    def save_token_to_cache(self, token_info: Dict[str, str]) -> None:
        self.token_info = token_info  # type: ignore

        if self._user_id:
            self.save_token_to_db(self._user_id)

    def save_token_to_db(self, user_id: str) -> None:
        if not self.token_info:
            return

        with self._session as session:
            self._users_repo(session).add_token(user_id, self.token_info)
            session.commit()

    @property
    def _session(self):
        from src.repositories.unit_of_work import default_session
        return default_session()

    @property
    def _users_repo(self):
        from src.repositories.users import UsersRepository
        return UsersRepository


class FilemonSpotifyOAuth(SpotifyOAuth):
    def __init__(self, scope: List[str], spotify_response: str, user_id: Optional[str]):
        self._spotify_response = spotify_response
        super().__init__(scope=scope, open_browser=False, cache_handler=DbCacheHandler(user_id=user_id))

    def _get_auth_response_interactive(self, open_browser=False):
        """
        Override 'SpotifyOAuth._get_auth_response_interactive' in order to disable 'input' prompt,
        which is not need in the backend application.
        """
        state, code = SpotifyOAuth.parse_auth_response_url(self._spotify_response)
        if self.state is not None and self.state != state:
            raise SpotifyStateError(self.state, state)
        return code


def get_spotipy(spotify_code: str, user_id: Optional[str]) -> Spotify:
    auth = FilemonSpotifyOAuth(scope=SCOPE, spotify_response=spotify_code, user_id=user_id)
    return Spotify(auth_manager=auth)
