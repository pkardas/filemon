import os

from fastapi import APIRouter
from spotipy import SpotifyOAuth
from starlette.responses import RedirectResponse

from src.gateways.auth import SCOPE
from src.message_bus.bus import MessageBus
from src.models.bus import AddUser
from src.repositories.unit_of_work import UnitOfWork

router = APIRouter()
bus = MessageBus(uow=UnitOfWork())


@router.get("/spotify")
def spotify():
    return RedirectResponse(SpotifyOAuth(scope=SCOPE).get_authorize_url())


@router.get("/spotify/callback/")
def spotify_callback(code: str):
    bus.handle(AddUser(spotify_code=f"{os.getenv('SPOTIPY_REDIRECT_URI')}?code={code}"))
    return RedirectResponse("https://open.spotify.com/")
