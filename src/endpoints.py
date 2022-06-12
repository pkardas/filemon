import os

from fastapi import APIRouter
from spotipy import SpotifyOAuth
from src.gateways.spotify import Spotify

from src.gateways.auth import SCOPE
from src.models.api import SpotifyAuthResponse

router = APIRouter()


@router.get("/spotify", response_model=SpotifyAuthResponse)
def spotify():
    return SpotifyAuthResponse(url=SpotifyOAuth(scope=SCOPE).get_authorize_url())


@router.get("/spotify/callback/")
def spotify_callback(code: str):
    us = Spotify(f"{os.getenv('SPOTIPY_REDIRECT_URI')}?code={code}")
    return {"user": us.user.display_name}
