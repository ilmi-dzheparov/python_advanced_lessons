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

def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic function
    """
    utils_logger.debug("utils.py: Start working function string_to_operator")
    if not isinstance(value, str):
        print("wrong operator type", value)
        utils_logger.error("utils.py: Wrong operator type")
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        print("wrong operator value", value)
        utils_logger.error("utils.py: Wrong operator type")
        raise ValueError("wrong operator value")

    utils_logger.debug("utils.py: Function string_to_operator is successfully ended")
    return OPERATORS[value]
