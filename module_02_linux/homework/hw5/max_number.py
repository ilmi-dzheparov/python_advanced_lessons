"""
Реализуйте endpoint, начинающийся с /max_number, в который можно передать список чисел, разделённых слешем /.
Endpoint должен вернуть текст «Максимальное переданное число {number}»,
где number — выделенное курсивом наибольшее из переданных чисел.

Примеры:

/max_number/10/2/9/1
Максимальное число: 10

/max_number/1/1/1/1/1/1/1/2
Максимальное число: 2

"""

from flask import Flask

app = Flask(__name__)


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


@app.route("/max_number/<path:numbers>")
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


if __name__ == "__main__":
    app.run(debug=True)
