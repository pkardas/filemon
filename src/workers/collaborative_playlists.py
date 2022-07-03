from src.message_bus.bus import MessageBus
from src.repositories.unit_of_work import UnitOfWork


def run(bus=MessageBus(uow=UnitOfWork())):
    pass


if __name__ == '__main__':
    run()
