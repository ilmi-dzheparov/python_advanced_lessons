import datetime
from flask import Flask

app = Flask(__name__)


@app.route('/test')
def test_function():
    now = datetime.datetime.now().utcnow()
    return f'Это тестовая страничка, ответ сгенерирован в {now}'


@app.route('/hello')
def hell0_world():
    return 'Hello World!'


count = 0
@app.route('/count')
def counter():
    global count
    count += 1
    return f'Это тестовая страничка, ответ сгенерирован {count}'