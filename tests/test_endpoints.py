import os
from unittest import mock

from tests.fakes.fake_spotipy import FakeSpotipy
from tests.fakes.fake_unit_of_work import FakeUnitOfWork

from src.message_bus.bus import MessageBus


def test_spotify(api_test_client):
    result = api_test_client.get("/spotify")

    assert result.url.startswith("https://accounts.spotify.com/authorize?client_id=")

    assert len(result.history) == 1
    assert result.history[0].status_code == 307


@mock.patch("src.gateways.spotify.get_spotipy", lambda spotify_code: FakeSpotipy())
def test_spotify_callback(api_test_client):
    fake_uow = FakeUnitOfWork()

    with mock.patch("src.endpoints.bus", MessageBus(uow=fake_uow)):
        api_test_client.get("/spotify/callback?code=123456789")

    assert len(fake_uow.users.all_users) == 1
    assert fake_uow.users.all_users[0].spotify_code == f"{os.getenv('SPOTIPY_REDIRECT_URI')}?code=123456789"
