from datetime import (
    datetime,
    timedelta,
)

from src.message_bus.bus import MessageBus
from src.models.bus import (
    FetchListeningHistory,
    UpdatePartitions,
)
from src.repositories.unit_of_work import UnitOfWork


def run(bus=MessageBus(uow=UnitOfWork())):
    today = datetime.now().date()
    for i in range(7):
        bus.handle(UpdatePartitions(day=today - timedelta(days=i)))

    bus.handle(FetchListeningHistory())


if __name__ == '__main__':
    run()
