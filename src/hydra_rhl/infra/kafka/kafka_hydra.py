import json
from kafka import KafkaConsumer, ConsumerRebalanceListener
from ...infra.events.utils import get_topic


# this class provides observability around consumer assignment
class _ConsumerListener(ConsumerRebalanceListener):
    def on_partitions_revoked(self, revoked):
        print("on_partitions_revoked called")
        print(revoked)

    def on_partitions_assigned(self, assigned):
        print("on_partitions_assigned called")
        print(assigned)


class MyKafkaConsumer:
    def __init__(
        self,
        env,
        bootstrap_servers,
        auto_offset_reset,
        enable_auto_commit,
        eventName,
        groupName,
        callBack,
        concurrency=1,
    ):
        self.env = env
        self.eventName = eventName
        self.groupName = groupName
        self.callBack = callBack
        self.concurrency = concurrency
        self.consumer = KafkaConsumer(
            bootstrap_servers=[bootstrap_servers],
            auto_offset_reset=auto_offset_reset,  # question this
            enable_auto_commit=enable_auto_commit,  # question this
            group_id=self.getGroupId(),
            value_deserializer=lambda m: json.loads(m.decode("ascii")),
        )

    def getGroupId(self):
        return self.groupName + "_" + self.env

    def run(self):
        try:
            self.consumer.subscribe(
                topics=get_topic(self.eventName, self.env), listener=_ConsumerListener()
            )
            for message in self.consumer:
                self.callBack(message)
        except Exception as e:
            print(e)
