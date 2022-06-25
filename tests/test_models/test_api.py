from contextlib import nullcontext as does_not_raise

import pytest
from pydantic import ValidationError

from src.models.api import CreatePlaylistRequest


@pytest.mark.parametrize("users, expected_result", [
    # @formatter:off
    ([],               pytest.raises(ValidationError)),
    (["user"],         does_not_raise()),
    (["user", "user"], does_not_raise()),
    # @formatter:on
])
def test_must_contain_at_least_one_user(users, expected_result):
    with expected_result:
        CreatePlaylistRequest(users=users)
