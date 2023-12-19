"""
Напишите GET-эндпоинт /uptime, который в ответ на запрос будет выводить строку вида f"Current uptime is {UPTIME}",
где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).

Сделать это можно с помощью команды uptime.
"""
import subprocess

from flask import Flask

app = Flask(__name__)


@app.route("/uptime", methods=['GET'])
def uptime() -> str:
    result = subprocess.check_output(['uptime', '-p']).decode('utf-8')

    return f"<pre>Uptime information:\n{result[3:]}<pre>"


if __name__ == '__main__':
    app.run(debug=True)
