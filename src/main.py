import os

from gateways.spotify import Spotify

us = Spotify(os.getenv("SPOTIFY_CODE"))
for item in us.recently_played().items:
    print(item.track.name, item.played_at)
