from datetime import date

import pytest

from src.models.db import (
    CollaborativePlaylist,
    ListeningHistory,
    User,
    get_partition_name,
    get_table_name,
)


@pytest.mark.parametrize("table, expected_result", [
    # @formatter:off
    (ListeningHistory,      "listening_history"),
    (User,                  "users"),
    (CollaborativePlaylist, "collaborative_playlists"),
    # @formatter:on
])
def test_table_name(table, expected_result):
    assert get_table_name(table) == expected_result


@pytest.mark.parametrize("table, day, expected_result", [
    # @formatter:off
    (ListeningHistory, date(2022, 6, 1),  "listening_history_2022_06_01"),
    (ListeningHistory, date(2022, 6, 13), "listening_history_2022_06_13"),
    # @formatter:on
])
def test_partition_name(table, day, expected_result):
    assert get_partition_name(table, day) == expected_result
