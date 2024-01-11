"""
Ваш коллега, применив JsonAdapter из предыдущей задачи, сохранил логи работы его сайта за сутки
в файле skillbox_json_messages.log. Помогите ему собрать следующие данные:

1. Сколько было сообщений каждого уровня за сутки.
2. В какой час было больше всего логов.
3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
4. Сколько сообщений содержит слово dog.
5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
"""
import json
import subprocess
from typing import Dict
from collections import Counter


def task1() -> Dict[str, int]:
    """
    1. Сколько было сообщений каждого уровня за сутки.
    @return: словарь вида {уровень: количество}
    """
    level_count = {
        "DEBUG": 0,
        "INFO": 0,
        "ERROR": 0,
        "CRITICAL": 0
    }
    for key in level_count.keys():
        command = 'grep -c ' + "'" + '"level"' + ": " + f'"{key}"' + "'" + ' skillbox_json_messages.log'
        res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        level_count[key] = int(res.stdout)

    return level_count


def task2() -> int:
    """
    2. В какой час было больше всего логов.
    @return: час
    """
    hours_logs = []
    count = 0
    hour_max = 0
    for hour in range(0, 24):
        if hour < 10:
            key_h = "0" + str(hour)
        else:
            key_h = str(hour)
        command = 'grep ' + "'" + '"time"' + ": " + f'"{key_h}' + "'" + ' skillbox_json_messages.log'
        res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        lines = res.stdout.splitlines()
        if count < len(lines):
            count = len(lines)
            hour_max = hour

    return hour_max


def task3() -> int:
    """
    3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
    @return: количество логов
    """
    count = 0
    str_to_find = '"level"' + ": " + '"CRITICAL"'
    for key_h in ("05:0", "05:1"):
        command = 'grep ' + "'" + '"time"' + ": " + f'"{key_h}' + "'" + ' skillbox_json_messages.log'
        res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        count += res.stdout.count(str_to_find)

    return count


def task4() -> int:
    """
    4. Сколько сообщений содержат слово dog.
    @return: количество сообщений
    """
    command = 'grep -c ' + "'" + 'dog' + "'" + ' skillbox_json_messages.log'
    res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    return int(res.stdout)


def task5() -> str:
    """
    5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
    @return: слово
    """
    words = []
    command = 'grep ' + "'" + '"level"' + ": " + f'"WARNING"' + "'" + ' skillbox_json_messages.log'
    res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    lines = res.stdout.splitlines()
    for line in lines:
        line_json = json.loads(line)
        words.extend(line_json["message"].lower().split())
    counter = Counter(words)
    most_common_word = max(counter, key=counter.get)
    return(most_common_word)






if __name__ == '__main__':
    tasks = (task1, task2, task3, task4, task5)
    for i, task_fun in enumerate(tasks, 1):
        task_answer = task_fun()
        print(f'{i}. {task_answer}')
