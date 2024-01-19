import json
from flask import Flask, request


app = Flask(__name__)


def save_logs(pathfile: str, data: str) -> None:
    with open(pathfile, 'a') as f:
        f.write(data + '\n')


@app.route('/log', methods=['POST'])
def log():
    """
    Записываем полученные логи которые пришли к нам на сервер
    return: текстовое сообщение об успешной записи, статус код успешной работы

    """
    data = request.get_data(as_text=True)
    log_data = json.dumps(data)
    save_logs("received_logs.log", log_data)
    print(f"Received log: {log_data}")
    return "Logs received successfully", 200


@app.route('/logs', methods=['GET'])
def logs():
    """
    Рендерим список полученных логов
    return: список логов обернутый в тег HTML <pre></pre>
    """
    log_data = request.args.lists()
    for data in log_data:
        log_data = json.dumps(json.loads(data[0]))
    save_logs("received_logs.log", log_data)
    print(f"Received log: {log_data}")
    return "Logs received successfully", 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)