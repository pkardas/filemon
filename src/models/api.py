from typing import (
    List,
    Optional,
)

from pydantic import (
    BaseModel,
    validator,
)


class CreatePlaylistRequest(BaseModel):
    users: List[str]
    playlist_name: Optional[str] = "Blend by Filemon"

    @validator("users")
    def name_must_contain_at_least_one_user(cls, users):
        if len(users) == 0:
            raise ValueError("Must contain at least one user")
        return users
