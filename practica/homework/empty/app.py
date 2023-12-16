from datetime import datetime
import os
import sys


from flask import Flask

app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, 'output_file.txt')

with open(OUTPUT_FILE) as file:
    aux_file_lines = file.readlines()[1:]


@app.route('/get_aux/rss')
def get_summary_rss():
    global aux_file_lines
    size = 0
    for line in aux_file_lines:
        size += int(line.split()[5])
    size_bytes = size
    units = ["б", "Кб", "Мб", "Гб"]
    unit_index = 0
    while size >= 1024 and unit_index <= len(units)-1:
        size /= 1024
        unit_index += 1
    f_size = "{:.2f}".format(size)
    return f'Суммарный объем потребляемой памяти: {size_bytes} {units[0]} или {f_size} {units[unit_index]}'


weekdays_tuple = ('Хорошего понедельника', 'Хорошего вторника', 'Хорошей среды', 'Хорошего четверга', 'Хорошей пятницы', 'Хорошей субботы', 'Хорошего воскркесенья')
# weekdays_list = ['Хорошего понедельника', 'Хорошего вторника', 'Хорошей среды', 'Хорошего четверга', 'Хорошей пятницы', 'Хорошей субботы', 'Хорошего воскркесенья']
# weekdays_dict = {0: 'Хорошего понедельника', 1: 'Хорошего вторника', 2: 'Хорошей среды', 3: 'Хорошего четверга', 4: 'Хорошей пятницы', 5: 'Хорошей субботы', 6:'Хорошего воскркесенья'}
#
# print(sys.getsizeof(weekdays_tuple))
# print(sys.getsizeof(weekdays_list))
# print(sys.getsizeof(weekdays_dict))


@app.route('/hello_world/<username>')
def hell0_world(username:str):
    global weekdays_tuple
    weekday = datetime.today().weekday()
    return f'Привет, {username}! {weekdays_tuple[weekday]}!'


def is_number(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def is_list_of_numbers(num_list):
    for num in num_list:
        if is_number(num) == False:
            return False


@app.route('/max_number/<path:numbers>')
def max_number(numbers):
    if numbers[-1] == '/':
        numbers = numbers[:-1]
    list_of_data = numbers.split('/')
    if is_list_of_numbers(list_of_data) == False:
        return f'Некоторые из переданных данных не являются числами'
    else:
        list_of_numbers = [float(num) for num in list_of_data]

    max_number = max(list_of_numbers)
    return f'Максимальное переданное число <i>{max_number}</i>'


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route('/preview/<int:size>/<path:relative_path>')
def preview(size, relative_path):
    abs_path = os.path.join(BASE_DIR, relative_path)
    with open(abs_path) as file:
        result_text = file.read(size)
    result_size = len(result_text)
    return (f'<b>{abs_path}</b> {result_size}<br>'
            f'{result_text}')




if __name__ == '__main__':
    app.run(debug=True)
