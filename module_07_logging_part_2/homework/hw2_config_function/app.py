import sys
import logging
from utils import string_to_operator

# logging.basicConfig(level="DEBUG")
logger = logging.getLogger()
logger.setLevel("DEBUG")
app_logger = logging.getLogger("app")
handler = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter(
    "%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def calc(args):
    app_logger.debug("Start working function calc()")
    app_logger.info(f'Arguments: {args}')
    print("Arguments: ", args)

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
        app_logger.info(f'num_1: {num_1}')
    except ValueError as e:
        app_logger.exception(e)
        print("Error while converting number 1")
        print(e)

    try:
        num_2 = float(num_2)
        app_logger.info(f'num_1: {num_2}')
    except ValueError as e:
        app_logger.exception(e)
        print("Error while converting number 2")
        print(e)

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)
    app_logger.debug("Function calc() is successfully ended")
    app_logger.info(f"Result: {result}")
    print("Result: ", result)
    print(f"{num_1} {operator} {num_2} = {result}")


if __name__ == '__main__':
    # calc(sys.argv[1:])
    calc('2+9')
