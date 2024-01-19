import logging.config
from dict_config import dict_config

logging.config.dictConfig(dict_config)
submodule_logger = logging.getLogger("module_logger.submodule_logger")
submodule_logger.setLevel("DEBUG")

def main():
    submodule_logger.debug("Hi there!")

if __name__ == "__main__":
    main()