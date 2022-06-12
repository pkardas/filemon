from src.models import commands

from src.message_bus import handlers

COMMAND_HANDLERS = {
    commands.AddUser: handlers.add_user
}


class MessageBus:
    pass
