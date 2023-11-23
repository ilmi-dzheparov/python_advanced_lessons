"""
Удобно направлять результат выполнения команды напрямую в программу с помощью конвейера (pipe):

$ ls -l | python3 get_mean_size.py

Напишите функцию get_mean_size, которая на вход принимает результат выполнения команды ls -l,
а возвращает средний размер файла в каталоге.
"""

import sys


def get_mean_size(data_list: list[str]):
    total_size = 0
    count = 0
    if data_list:
        for line in data_list:
            if line[0] != 'd':
                columns = line.split()
                total_size += int(columns[4])
                count += 1
    else:
        print(f'В папке отсутствуют файлы')
        return None
    mean_size = total_size / count
    mean_size_format = "{:.2f}".format(mean_size)
    return mean_size_format


if __name__ == '__main__':
    data_list: list[str] = sys.stdin.readlines()[1:]
    mean_size = get_mean_size(data_list)
    print(mean_size)
