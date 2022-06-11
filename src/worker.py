import calendar
import os
from datetime import (
    date,
    datetime,
    timedelta,
)
from typing import List

from gateways.spotify import Spotify
from respository import (
    ListeningHistoryRepository,
    default_session,
)


def get_days(start: datetime, end: datetime) -> List[date]:
    assert end >= start, "Start has to be before End"
    return [(start + timedelta(days=i)).date() for i in range((end - start).days + 1)]


def main():
    repository = ListeningHistoryRepository(session=default_session())
    spotify = Spotify(os.getenv("SPOTIFY_CODE"))

    for day in get_days(start=repository.last_played_at(spotify.user), end=datetime.now()):
        repository.create_partition(day)

        timestamp = calendar.timegm(repository.last_played_at(spotify.user).utctimetuple())

        for item in spotify.recently_played(after=timestamp).items:
            repository.add(spotify.user, item)

    repository.commit()


if __name__ == '__main__':
    main()
