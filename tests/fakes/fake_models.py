from factory import (
    Factory,
    Faker,
)

from src.models.spotify import (
    CreatedPlaylist,
    LovedTracks,
    SpotifyUser,
)


class FakeSpotifyUser(Factory):
    class Meta:
        model = SpotifyUser

    id = Faker("uuid4")
    display_name = Faker("name")
    uri = Faker("uuid4")


class FakeCreatedPlaylist(Factory):
    class Meta:
        model = CreatedPlaylist

    id = Faker("uuid4")


class FakeLovedTracks(Factory):
    class Meta:
        model = LovedTracks

    total = 15
    items = []  # type: ignore
    limit = 20
    offset: int
    next = None
