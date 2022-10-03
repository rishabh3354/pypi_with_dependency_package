from .logger import Logger
from ..infra.events.consumer import EventConsumer
from ..infra.events.producer import EventProducer
from ..infra.kafka.kafka_hydra import MyKafkaConsumer
from dependency_injector import containers, providers
from kafka import KafkaProducer


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    kafka_consumer = providers.Factory(
        kafka_consumer=MyKafkaConsumer,
        bootstrap_servers=config.bootstrap_servers,
        auto_offset_reset=True,
        env=config.env,
    )

    event_consumer = providers.Factory(
        EventConsumer,
        kafka_consumer=kafka_consumer,
        config=config,
    )

    event_producer = providers.Singleton(
        EventProducer,
        bootstrap_servers=config.bootstrap_servers,
        env=config.env,
        producer=KafkaProducer,
        logger=Logger,
    )


def bootstrap(hydraConfig, callback):
    container = Container()
    container.config.from_dict(hydraConfig)
    container.wire(modules=[__name__])
    callback(container)
