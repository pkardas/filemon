from datetime import (
    date,
    datetime,
)

import pytest

from worker import get_days


@pytest.mark.parametrize("start, end, expected_range", [
    # @formatter:off
    (datetime(2022, 1, 1, 1), datetime(2022, 1, 1, 1),     [date(2022, 1, 1)]),
    (datetime(2022, 1, 1, 1), datetime(2022, 1, 1, 17, 0), [date(2022, 1, 1)]),
    (datetime(2022, 1, 1, 1), datetime(2022, 1, 2, 17, 0), [date(2022, 1, 1), date(2022, 1, 2)])
    # @formatter:off
])
def test_get_days(start, end, expected_range):
    assert get_days(start, end) == expected_range
