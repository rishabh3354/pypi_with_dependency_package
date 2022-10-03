import concurrent.futures


# todo: add standard logger
# platformSettings = {"brokers": ["localhost:9092"], "environment": "local_akhil"}
# log = Logger()


class EventConsumer:
    def __init__(
        self,
        env,
        bootstrap_servers,
        auto_offset_reset,
        enable_auto_commit,
        kafka_consumer,
        logger,
        eventName,
        groupName,
        callBack,
        concurrency=1,
    ):
        self.env = env
        self.bootstrap_servers = bootstrap_servers
        self.auto_offset_reset = auto_offset_reset
        self.enable_auto_commit = enable_auto_commit
        self.eventName = eventName
        self.groupName = groupName
        self.concurrency = concurrency
        self.callBack = callBack
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=None)
        self.logger = logger
        self.kafka_consumer = kafka_consumer

    def runSingleInstance(self):
        consumer = self.kafka_consumer(
            bootstrap_servers=self.bootstrap_servers,
            auto_offset_reset=self.auto_offset_reset,
            enable_auto_commit=self.enable_auto_commit,
            eventName=self.eventName,
            groupName=self.groupName,
            concurrency=self.concurrency,
            callBack=self.callBack,
        )
        consumer.run()

    def run(self):
        try:
            print(self.concurrency.__class__)
            for i in range(self.concurrency):
                print("Starting Consumer Instance " + str(i))
                self.executor.submit(self.runSingleInstance)
        except Exception as e:
            print(e)


# # @inject
# def main():
#     ticketBookedConsumer = EventConsumer(
#         env=container.config.env,
#         bootstrap_servers=container.config.bootstrap_servers,
#         auto_offset_reset=container.config.auto_offset_reset,
#         enable_auto_commit=container.config.enable_auto_commit,
#         eventName=container.config.eventName,
#         groupName=container.config.groupName,
#         concurrency=container.config.concurrency,
#         callBack=container.config.callBack,
#     )
#     ticketBookedConsumer.run()
#     print(container.config)
#
#
# if __name__ == "__main__":
#     container = Container()
#     # container.init_resources()
#     container.config.bootstrap_servers.from_env("bootstrap_servers", required=True)
#     container.config.auto_offset_reset.from_env("auto_offset_reset", required=True)
#     container.config.enable_auto_commit.from_env("enable_auto_commit", required=True)
#     container.config.eventName.from_env("event_name", required=True)
#     container.config.groupName.from_env("group_name", required=True)
#     container.config.concurrency.from_env("concurrency", required=True)
#     container.config.callBack.from_env("callback", required=True)
#     container.config.env.from_env("env", required=True)
#     container.wire(modules=[__name__])
#     main()  # <-- dependency is injected automatically
