import os
from datetime import date
from typing import Set

from src.gateways.spotify import Spotify
from src.respository import (
    ListeningHistoryRepository,
    default_session,
)
from src.models.spotify import RecentlyPlayed


def get_days(recently_played: RecentlyPlayed) -> Set[date]:
    return {item.played_at.date() for item in recently_played.items}


def main():
    repository = ListeningHistoryRepository(session=default_session())
    spotify = Spotify(os.getenv("SPOTIFY_CODE"))
    recently_played = spotify.recently_played()

    for day in get_days(recently_played):
        repository.create_partition(day)

    for item in recently_played.items:
        repository.add(spotify.user, item)

    repository.commit()


if __name__ == '__main__':
    main()
