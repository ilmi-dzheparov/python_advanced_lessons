import logging
import sys


class LevelFileHandler(logging.Handler):
    def __init__(self, file_name_debug_info, file_name_error, mode="a"):
        super().__init__()
        self.file_name_debug_info = file_name_debug_info
        self.file_name_error = file_name_error
        self.mode = mode
    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        log_level = message.split()[0]
        if log_level in ["DEBUG", "INFO"]:
            with open(self.file_name_debug_info, self.mode) as f:
                f.write(message + '\n')
        if log_level == "ERROR":
            with open(self.file_name_error, self.mode) as f:
                f.write(message + '\n')


def get_logger(name):
    ...
    return logger

