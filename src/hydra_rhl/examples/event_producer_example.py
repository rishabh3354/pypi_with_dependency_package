from ..core.container import bootstrap
from dependency_injector.wiring import inject


def foo(message):
    print("{}".format(message.value))
    # log.info("Foo: This function call is not part of consumer logic.")


@inject
def main(container):
    event_producer = container.event_producer()
    event_producer.produce(
        event_name=f"test_topic",
        message={"domains": ["carbonconsole.com", "matrixcastle.com"]},
    )


if __name__ == "__main__":
    hydraConfig = {
        "aws": {
            "access_key_id": "KEY",
            "secret_access_key": "SECRET",
        },
        "bootstrap_servers": "localhost:9092",
        "env": "local_akhil",
    }

    bootstrap(hydraConfig, main)
