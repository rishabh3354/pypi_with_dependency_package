import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=f'{os.environ["HOME"]}/hydra/.env')

PRODUCER_CONFIG = {"bootstrap_servers": os.getenv("HOST")}

CONSUMER_CONFIG = {
    "bootstrap_servers": os.getenv("HOST"),
    "enable_auto_commit": False,
    "auto_offset_reset": "smallest",
}

ENV = os.getenv("ENV")


class KafkaConfig:
    def __init__(self, config, env):
        self.config = config
        self.env = env
