"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""
import shlex
import subprocess
from time import time

from flask import Flask, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, NumberRange

app = Flask(__name__)


class CodeForm(FlaskForm):
    code = StringField(validators=[InputRequired()])
    timeout = IntegerField(validators=[InputRequired(), NumberRange(min=1, max=30)])


def run_python_code_in_subproccess(code: str, timeout: int):
    # command = []
    try:
        # code = f'"{code}"'
        # command = ['python', '-c', code]
        # print(command)prlimit --nproc=1:1 --nofile=1024
        command = f'prlimit --nproc=1:1 python -c "{code}"'
        res = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            stdout, stderr = res.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            res.terminate()
            return {'stdout': '', 'stderr': 'Timeout is expired'}

        return {'stdout': stdout, 'stderr': stderr}
    except subprocess.CalledProcessError as e:
        print(f'Процесс завершился с ошибкой. Код возврата: {e.returncode}')

    print(res)

@app.route('/run_code', methods=['POST'])
def run_code():
    form = CodeForm()
    if form.validate_on_submit():
        code, timeout = form.code.data, form.timeout.data
        print(code, timeout)
        result = run_python_code_in_subproccess(code, timeout)
        return jsonify(result)
    else:
        return jsonify({'error': f'Invalid input, {form.errors}'}), 400
        # return f"Invalid input, {form.errors}"



if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
