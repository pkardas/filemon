import logging
from datetime import (
    datetime,
    timedelta,
)
from threading import Event

from src.message_bus.bus import MessageBus
from src.models.bus import (
    FetchListeningHistory,
    UpdatePartitions,
)
from src.repositories.unit_of_work import UnitOfWork

event = Event()
logger = logging.getLogger("listening_history")


def run(bus=MessageBus(uow=UnitOfWork())):
    today = datetime.now().date()
    for i in range(3):
        bus.handle(UpdatePartitions(day=today - timedelta(days=i)))

    bus.handle(FetchListeningHistory())


def run_loop():
    logger.info("Worker fetching listening history registered.")
    while not event.wait(timeout=60 * 5):
        logger.info("Fetching listening history...")
        run()


if __name__ == '__main__':
    run()
