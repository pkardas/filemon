from pydantic import BaseModel


class SpotifyAuthResponse(BaseModel):
    url: str
