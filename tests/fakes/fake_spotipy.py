from fakes.fake_models import (
    FakeCreatedPlaylist,
    FakeLovedTracks,
    FakeSpotifyUser,
)


class FakeSpotipy:
    # noinspection PyMethodMayBeStatic
    def me(self, **kwargs):
        return FakeSpotifyUser().dict()

    # noinspection PyMethodMayBeStatic
    def user_playlist_create(self, **kwargs):
        return FakeCreatedPlaylist().dict()

    # noinspection PyMethodMayBeStatic
    def current_user_recently_played(self, **kwargs):
        return {}

    # noinspection PyMethodMayBeStatic
    def current_user_saved_tracks(self, **kwargs):
        return FakeLovedTracks().dict()
