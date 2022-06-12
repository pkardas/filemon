from typing import List

from sqlmodel import Session

from src.models.bus import Message


class Repository:
    def __init__(self, session: Session):
        self.session = session
        self.queue: List[Message] = []
