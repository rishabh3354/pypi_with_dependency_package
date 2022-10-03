import json
from ...infra.events.utils import get_topic


class EventProducer:
    # create separate common function for event_name in producer and consumer
    def __init__(self, bootstrap_servers, env, producer, logger):
        self.env = env
        self.producer = producer(
            bootstrap_servers=[bootstrap_servers],
            value_serializer=lambda m: json.dumps(m).encode("ascii"),
        )
        self.logger = logger()

    def on_send_success(self, record_metadata):
        message = f"on_send_success triggered!! {record_metadata.topic}, record_metadata.offset"
        self.logger.info(message)

    def on_send_error(self, excp):
        message = f"on_send_error triggered!!\n{excp}"
        self.logger.error(message)

    def produce(self, event_name, message):
        try:
            event_name = get_topic(event_name, self.env)
            self.producer.send(topic=event_name, value=message).add_callback(
                self.on_send_success
            ).add_errback(self.on_send_error)
            self.producer.flush()

        except Exception as e:
            self.on_send_error(repr(e))
