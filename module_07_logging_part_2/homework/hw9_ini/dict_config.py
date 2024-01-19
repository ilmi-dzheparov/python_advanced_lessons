import sys

dict_config = {
    "loggers": {
        "root": {
            "level": "DEBUG",
            "handlers": ["consoleHandler"],
        },
        "applogger": {
            "level": "DEBUG",
            "handlers": ["consoleHandler", "fileHandler"],
            "qualname": "appLogger",
            "propagate": 0,
        }
    },
    "handlers": {
        "consoleHandler": {
            "class": "StreamHandler",
            "level": "WARNING",
            "formatter": "consoleFormatter",
            "args": [sys.stdout,]
        },
        "fileHandler": {
            "class": "FileHandler",
            "level": "DEBUG",
            "formatter": "fileFormatter",
            "args": ['logfile.log',]
        },
    },
    "formatters": {
        "fileFormatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%Z",
        },
        "consoleFormatter": {
            "format": "%(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%Z"
        },
    },
 }