"""
С помощью команды ps можно посмотреть список запущенных процессов.
С флагами aux эта команда выведет информацию обо всех процессах, запущенных в системе.

Запустите эту команду и сохраните выданный результат в файл:

$ ps aux > output_file.txt

Столбец RSS показывает информацию о потребляемой памяти в байтах.

Напишите функцию get_summary_rss, которая на вход принимает путь до файла с результатом выполнения команды ps aux,
а возвращает суммарный объём потребляемой памяти в человекочитаемом формате.
Это означает, что ответ надо перевести в байты, килобайты, мегабайты и так далее.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, 'output_file.txt')

with open(OUTPUT_FILE) as file:
    aux_file_lines = file.readlines()[1:]


def get_summary_rss(ps_output_file_path: str) -> str:
    with open(ps_output_file_path) as file:
        aux_file_lines = file.readlines()[1:]
    size = 0
    for line in aux_file_lines:
        size += int(line.split()[5])
    size_bytes = size
    units = ["б", "Кб", "Мб", "Гб"]
    unit_index = 0
    while size >= 1024 and unit_index <= len(units) - 1:
        size /= 1024
        unit_index += 1
    f_size = "{:.2f}".format(size)
    return f'Суммарный объем потребляемой памяти: {size_bytes} {units[0]} или {f_size} {units[unit_index]}'





if __name__ == '__main__':
    path: str = OUTPUT_FILE
    summary_rss: str = get_summary_rss(path)
    print(summary_rss)
