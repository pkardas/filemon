from threading import Event

from src.message_bus.bus import MessageBus
from src.models.bus import UpdatePlaylists
from src.repositories.unit_of_work import UnitOfWork

event = Event()


def run(bus=MessageBus(uow=UnitOfWork())):
    bus.handle(UpdatePlaylists())


def run_loop():
    while not event.wait(timeout=60 * 45):
        run()


if __name__ == '__main__':
    run_loop()
