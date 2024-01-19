import logging


class CustomFilter(logging.Filter):
    def filter(self, record):

        return record.msg.isascii()

# logging.basicConfig(level="DEBUG")
# logger = logging.getLogger(__name__)
# logger.addFilter(CustomFilter())
#
# logger.debug("This will not be ~йй logged")
# logger.info("This will be logged")
