"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""
import subprocess
import shlex
from typing import List

from flask import Flask, request

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps() -> str:
    args: List[str] = request.args.getlist('arg')
    quoted_command_list = ["ps",] + [shlex.quote(param) for param in args]
    print(quoted_command_list)
    result = subprocess.check_output(quoted_command_list).decode('utf-8')

    return f"<pre>Your result:\n{result}<pre>"


if __name__ == "__main__":
    app.run(debug=True)
