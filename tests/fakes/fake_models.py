from factory import (
    Factory,
    Faker,
)

from src.models.spotify import (
    CreatedPlaylist,
    Tracks,
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


class FakeTracks(Factory):
    class Meta:
        model = Tracks

    total = 15
    items = []  # type: ignore
    limit = 20
    offset: int
    next = None
