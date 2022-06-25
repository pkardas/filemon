from dataclasses import dataclass
from datetime import date
from typing import List

from src.models.spotify import (
    RecentlyPlayedItem,
    SpotifyUser,
)


class Message:
    pass


class Command(Message):
    pass


class Event(Message):
    pass


@dataclass
class AddUser(Command):
    spotify_code: str


@dataclass
class AddPlaylist(Command):
    users: List[str]
    playlist_name: str


@dataclass
class UpdatePartitions(Command):
    day: date


class FetchListeningHistory(Command):
    pass


@dataclass
class UserPlayedMusic(Event):
    user: SpotifyUser
    recently_played: RecentlyPlayedItem
