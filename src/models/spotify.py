from datetime import datetime
from typing import (
    List,
    Optional,
)

from pydantic import BaseModel


class Image(BaseModel):
    height: int
    width: int
    url: str


class Album(BaseModel):
    name: str
    uri: str
    images: List[Image]


class Artist(BaseModel):
    name: str
    uri: str


class Track(BaseModel):
    id: str
    album: Album
    artists: List[Artist]
    name: str
    uri: str


class Cursor(BaseModel):
    before: str
    after: str


class RecentlyPlayedItem(BaseModel):
    track: Track
    played_at: datetime


class LovedTracksItem(BaseModel):
    track: Track
    added_at: datetime


class RecentlyPlayed(BaseModel):
    items: List[RecentlyPlayedItem]
    cursors: Optional[Cursor]
    limit: int
    next: Optional[str]


class LovedTracks(BaseModel):
    total: int
    items: List[LovedTracksItem]
    limit: int
    offset: int
    next: Optional[str]


class CreatePlaylist(BaseModel):
    name: str
    description: str
    public: bool

class CreatedPlaylist(BaseModel):
    id: str

class SpotifyUser(BaseModel):
    id: str
    display_name: str
    uri: str


