import operator
from enum import Enum

from flask import Flask
from flask_jsonrpc import JSONRPC



app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)


@jsonrpc.method('calc.add')
def add(a: float, b: float) -> float:
    """
    Пример запроса:

    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
        -d '{
            "jsonrpc": "2.0",
            "method": "calc.add",
            "params": {"a": 7.8, "b": 5.3},
            "id": "1"
        }' http://localhost:5000/api

    Пример ответа:

    HTTP/1.1 200 OK
    Server: Werkzeug/3.0.1 Python/3.10.12
    Date: Fri, 09 Dec 2022 19:00:09 GMT
    Content-Type: application/json
    Content-Length: 53
    Connection: close

    {
      "id": "1",
      "jsonrpc": "2.0",
      "result": 13.1
    }
    """
    return operator.add(a, b)


@jsonrpc.method('calc.sub')
def subtraction(a: float, b: float) -> float:
    """
    Пример запроса:

    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
        -d '{
            "jsonrpc": "2.0",
            "method": "calc.sub",
            "params": {"a": 7.8, "b": 5.3},
            "id": "1"
        }' http://localhost:5000/api

    Пример ответа:

    HTTP/1.1 200 OK
    Server: Werkzeug/3.0.1 Python/3.10.12
    Date: Fri, 09 Dec 2022 19:00:09 GMT
    Content-Type: application/json
    Content-Length: 53
    Connection: close

    {
      "id": "1",
      "jsonrpc": "2.0",
      "result": 2.5
    }
    """
    return operator.sub(a, b)


@jsonrpc.method('calc.mult')
def multiplication(a: float, b: float) -> float:
    """
    Пример запроса:

    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
        -d '{
            "jsonrpc": "2.0",
            "method": "calc.mult",
            "params": {"a": 7.8, "b": 5.3},
            "id": "1"
        }' http://localhost:5000/api

    Пример ответа:

    HTTP/1.1 200 OK
    Server: Werkzeug/3.0.1 Python/3.10.12
    Date: Fri, 09 Dec 2022 19:00:09 GMT
    Content-Type: application/json
    Content-Length: 53
    Connection: close

    {
      "id": "1",
      "jsonrpc": "2.0",
      "result": 41.34
    }
    """
    return operator.mul(a, b)


@jsonrpc.method('calc.div')
def division(a: float, b: float) -> float:
    """
    Пример запроса:

    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
        -d '{
            "jsonrpc": "2.0",
            "method": "calc.div",
            "params": {"a": 7.8, "b": 3.0},
            "id": "1"
        }' http://localhost:5000/api

    Пример ответа:

    HTTP/1.1 200 OK
    Server: Werkzeug/3.0.1 Python/3.10.12
    Date: Fri, 09 Dec 2022 19:00:09 GMT
    Content-Type: application/json
    Content-Length: 53
    Connection: close

    {
      "id": "1",
      "jsonrpc": "2.0",
      "result": 2.6
    }
    """
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return operator.truediv(a, b)


class Operation(str, Enum):
    ADD = "add"
    SUBSTRACTION = "sub"
    MULTIPLICATION = "mul"
    DIVISION = "div"


@jsonrpc.method('calc')
def operation(op: str, a: float, b: float) -> float:
    """
    Пример запроса:

    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
        -d '{
            "jsonrpc": "2.0",
            "method": "calc",
            "params": {"op": "div", "a": 7.8, "b": 3.0},
            "id": "1"
        }' http://localhost:5000/api

    Пример ответа:

    HTTP/1.1 200 OK
    Server: Werkzeug/3.0.1 Python/3.10.12
    Date: Fri, 09 Dec 2022 19:00:09 GMT
    Content-Type: application/json
    Content-Length: 53
    Connection: close

    {
      "id": "1",
      "jsonrpc": "2.0",
      "result": 2.6
    }
    """
    try:
        op_enum = Operation(op)
    except ValueError:
        raise ValueError("Invalid operation")
    operations = {
        Operation.ADD: operator.add,
        Operation.SUBSTRACTION: operator.sub,
        Operation.MULTIPLICATION: operator.mul,
        Operation.DIVISION: operator.truediv
    }

    if op == Operation.DIVISION and b == 0:
        raise ValueError("Division by zero is not allowed")
    return operations[op_enum](a, b)


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
