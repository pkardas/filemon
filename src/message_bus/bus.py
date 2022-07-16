import logging
from typing import (
    Callable,
    Dict,
    List,
    Type,
)

from src.message_bus.handlers import (
    add_playlist,
    add_user,
    fetch_listening_history,
    update_partitions,
    user_played_music,
    update_playlists,
    update_playlist,
    add_user_token,
    get_user_token,
)
from src.models.messages import (
    AddPlaylist,
    AddUser,
    Command,
    Event,
    FetchListeningHistory,
    Message,
    UpdatePartitions,
    UserPlayedMusic,
    UpdatePlaylists,
    UpdatePlaylist,
    AddUserToken,
    GetUserToken,
)
from src.repositories.unit_of_work import AbstractUnitOfWork

COMMAND_HANDLERS: Dict[Type[Command], Callable] = {
    AddUser: add_user,
    AddPlaylist: add_playlist,
    AddUserToken: add_user_token,
    GetUserToken: get_user_token,
    UpdatePlaylist: update_playlist,
    UpdatePlaylists: update_playlists,
    UpdatePartitions: update_partitions,
    FetchListeningHistory: fetch_listening_history,
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
        response = None

        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, Command):
                handler_response = self._handle_command(message)
            elif isinstance(message, Event):
                handler_response = self._handle_event(message)
            else:
                raise Exception(f"{message} was not an Event or Command")

            # 'handler' is allowed to return one, and only one response from the first internal handler:
            response = handler_response if not response else response

        return response

    def _handle_command(self, command: Command):
        try:
            handler = COMMAND_HANDLERS[type(command)]
            response = handler(command, self.uow)
            self.queue.extend(self.uow.collect_new_messages())
        except Exception:
            logger.exception(f"Exception handling command {command}")
            raise
        return response

    def _handle_event(self, event: Event):
        try:
            handler = EVENT_HANDLERS[type(event)]
            response = handler(event, self.uow)
            self.queue.extend(self.uow.collect_new_messages())
        except Exception:
            logger.exception(f"Exception handling event {event}")
            raise
        return response
