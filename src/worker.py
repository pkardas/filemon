from datetime import (
    datetime,
)

from src.message_bus.bus import MessageBus
from src.models.bus import (
    FetchListeningHistory,
    UpdatePartitions,
)
from src.repositories.unit_of_work import UnitOfWork

bus = MessageBus(uow=UnitOfWork())


def main():
    bus.handle(UpdatePartitions(day=datetime.now().date()))
    bus.handle(FetchListeningHistory())


if __name__ == '__main__':
    main()
