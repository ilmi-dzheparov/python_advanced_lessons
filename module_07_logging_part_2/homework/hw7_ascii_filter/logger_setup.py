from logger_helper import LevelFileHandler
from filter_setup import CustomFilter
import sys

dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s",
        },
    },
    "handlers": {
        "screen": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
            "stream": sys.stdout,
            "filters": ["my_filter"],
        },
        "file": {
            "()": LevelFileHandler,
            "level": "DEBUG",
            "formatter": "base",
            "file_name_debug_info": "call_debug.log",
            "file_name_error": "call_error.log",
            "mode": "a",
            "filters": ["my_filter"],
            },
    },
    "loggers": {
        "logger": {
            "level": "DEBUG",
            "handlers": ["screen", "file"],
        },
    },
    "filters": {
        'my_filter': {
            '()': CustomFilter,
        }
    }
}