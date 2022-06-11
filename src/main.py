import os

# from db.orm import get_session
from gateways.spotify import Spotify
from respository import (
    ListeningHistoryRepository,
    default_session,
)

us = Spotify(os.getenv("SPOTIFY_CODE"))
# for item in us.recently_played().items:
#     print(item.track.name, item.played_at)

repo = ListeningHistoryRepository(default_session())
print(repo.last_played_at(us.user))
