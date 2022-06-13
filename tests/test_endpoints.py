from src.gateways.auth import SCOPE
from src.models.api import SpotifyAuthResponse


def test_spotify(api_test_client):
    response = SpotifyAuthResponse(**api_test_client.get("/spotify").json())

    assert "https://accounts.spotify.com/authorize?client_id=" in response.url
    assert '+'.join(SCOPE) in response.url
