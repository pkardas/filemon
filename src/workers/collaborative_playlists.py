import logging
from threading import Event

from src.message_bus.bus import MessageBus
from src.models.messages import UpdatePlaylists
from src.repositories.unit_of_work import UnitOfWork

event = Event()
logger = logging.getLogger("collaborative_playlists")


def run(bus=MessageBus(uow=UnitOfWork())):
    bus.handle(UpdatePlaylists())


def run_loop():
    logger.info("Worker updating playlists registered.")
    while not event.wait(timeout=60 * 60 * 12):
        logger.info("Updating playlists...")
        run()


if __name__ == '__main__':
    run()
