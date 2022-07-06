from src.message_bus.bus import MessageBus
from src.models.bus import UpdatePlaylists
from src.repositories.unit_of_work import UnitOfWork


def run(bus=MessageBus(uow=UnitOfWork())):
    bus.handle(UpdatePlaylists())


if __name__ == '__main__':
    run()
