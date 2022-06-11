import os

from gateways.auth import AUTH_URL
from gateways.spotify import PersonalSpotify

print(AUTH_URL)
us = PersonalSpotify(os.getenv("SPOTIFY_RESPONSE"))
print(us.get_loved_tracks())
