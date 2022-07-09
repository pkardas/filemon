def test_spotify(api_test_client):
    result = api_test_client.get("/spotify")

    assert result.url.startswith("https://accounts.spotify.com/authorize?client_id=")

    assert len(result.history) == 1
    assert result.history[0].status_code == 307
