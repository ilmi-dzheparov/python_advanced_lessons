import logging
from typing import Union, Callable
from operator import sub, mul, truediv, add


OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}

Numeric = Union[int, float]

utils_logger = logging.getLogger("utils")
utils_handler = logging.handlers.TimedRotatingFileHandler("call_utils.log", when='H', interval=10, backupCount=10)
formatter = logging.Formatter(
    "%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s"
)
utils_handler.setFormatter(formatter)
utils_logger.setLevel("INFO")
utils_logger.addHandler(utils_handler)

def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic function
    """
    utils_logger.info("utils.py: Start working function string_to_operator")
    if not isinstance(value, str):
        print("wrong operator type", value)
        utils_logger.error("utils.py: Wrong operator type")
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        print("wrong operator value", value)
        utils_logger.error("utils.py: Wrong operator type")
        raise ValueError("wrong operator value")

    utils_logger.info("utils.py: Function string_to_operator is successfully ended")
    return OPERATORS[value]
