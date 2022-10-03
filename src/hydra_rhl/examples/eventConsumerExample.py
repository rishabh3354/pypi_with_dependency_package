from ..infra.events.consumer import EventConsumer
from ..settings.config import KafkaConfig, CONSUMER_CONFIG, ENV
from ..core.logger import Logger

log = Logger()


def foo(message):
    log.info("{}".format(message.value))
    # log.info("Foo: This function call is not part of consumer logic.")


def main():
    log.info("Main Process Started")
    config = KafkaConfig(CONSUMER_CONFIG, ENV)
    ticketBookedConsumer = EventConsumer(
        config=config,
        eventName="ticket_booked",
        groupName="notification_group_1",
        concurrency=3,
        callBack=foo,
    )
    ticketBookedConsumer.run()
    # foo()


main()
