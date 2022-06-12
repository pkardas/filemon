from dataclasses import dataclass
from datetime import date

from src.models.spotify import (
    RecentlyPlayedItem,
    User,
)


class Message:
    pass


class Command(Message):
    pass


class Event(Message):
    pass


@dataclass
class AddUser(Command):
    spotify_url: str


@dataclass
class UpdatePartitions(Command):
    day: date


class FetchListeningHistory(Command):
    pass


@dataclass
class UserPlayedMusic(Event):
    user: User
    recently_played: RecentlyPlayedItem
