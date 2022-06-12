import logging
from typing import (
    Callable,
    Dict,
    List,
    Type,
)

from src.message_bus import handlers
from src.message_bus.handlers import (
    fetch_listening_history,
    update_partitions,
    user_played_music,
)
from src.models.bus import (
    AddUser,
    Command,
    Event,
    FetchListeningHistory,
    Message,
    UpdatePartitions,
    UserPlayedMusic,
)
from src.repositories.unit_of_work import AbstractUnitOfWork

COMMAND_HANDLERS: Dict[Type[Command], Callable] = {
    AddUser: handlers.add_user,
    UpdatePartitions: update_partitions,
    FetchListeningHistory: fetch_listening_history
}

EVENT_HANDLERS: Dict[Type[Event], Callable] = {
    UserPlayedMusic: user_played_music
}

logger = logging.getLogger(__name__)


class MessageBus:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow
        self.queue: List[Message] = []

    def handle(self, message: Message):
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, Command):
                self._handle_command(message)
            elif isinstance(message, Event):
                self._handle_event(message)
            else:
                raise Exception(f"{message} was not an Event or Command")

    def _handle_command(self, command: Command):
        try:
            handler = COMMAND_HANDLERS[type(command)]
            handler(command, self.uow)
            self.queue.extend(self.uow.collect_new_messages())
        except Exception:
            logger.exception(f"Exception handling command {command}")
            raise

    def _handle_event(self, event: Event):
        try:
            handler = EVENT_HANDLERS[type(event)]
            handler(event, self.uow)
            self.queue.extend(self.uow.collect_new_messages())
        except Exception:
            logger.exception(f"Exception handling event {event}")
            raise
