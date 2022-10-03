import logging
import sys

FORMATTER = "%(asctime)s — %(name)s — %(levelname)s — %(message)s"


class Logger(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        logging.basicConfig(filename="test.log", filemode="w", format=FORMATTER)
        logger = logging.getLogger("kafka")
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self)
        logger.addHandler(logging.StreamHandler(sys.stdout))

    def emit(self, record):
        if "kafka." in record.name:
            if record.levelname == "DEBUG":
                self.debug(record)
            if record.levelname == "INFO":
                self.info(record)
            if record.levelname == "ERROR":
                self.error(record)
            return

    def debug(self, message):
        print("inside debug", message)

    def info(self, message):
        print("inside info", message)

    def error(self, message):
        print("inside error", message)

