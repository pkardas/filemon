from gateways.auth import get_spotify


class PersonalSpotify:
    def __init__(self, spotify_response: str):
        self._spotify = get_spotify(spotify_response)

    def get_recently_played(self) -> ...:
        return self._spotify.current_user_recently_played()

    def get_loved_tracks(self) -> ...:
        return self._spotify.current_user_saved_tracks()
