import logging
import sys


class CustomStreamHandler(logging.Handler):
    def __init__(self, stream_name=sys.stderr):
        super().__init__()
        self.stream_name = stream_name
    def emit(self, record):
        message = self.format(record)
