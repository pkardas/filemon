from dataclasses import dataclass
from datetime import date

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
class UpdatePartitions(Command):
    day: date


class FetchListeningHistory(Command):
    pass


@dataclass
class UserPlayedMusic(Event):
    user: SpotifyUser
    recently_played: RecentlyPlayedItem
