"""
Реализуйте приложение для учёта финансов, умеющее запоминать, сколько денег было потрачено за день,
а также показывать затраты за отдельный месяц и за целый год.

В программе должно быть три endpoints:

/add/<date>/<int:number> — сохранение информации о совершённой в рублях трате за какой-то день;
/calculate/<int:year> — получение суммарных трат за указанный год;
/calculate/<int:year>/<int:month> — получение суммарных трат за указанные год и месяц.

Дата для /add/ передаётся в формате YYYYMMDD, где YYYY — год, MM — месяц (от 1 до 12), DD — число (от 01 до 31).
Гарантируется, что переданная дата имеет такой формат и она корректна (никаких 31 февраля).
"""

from flask import Flask, abort
from datetime import  datetime

app = Flask(__name__)

storage = {}


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int):
    date_format = "%Y%m%d"
    parsed_date = datetime.strptime(date, date_format)
    if parsed_date:
        year = parsed_date.year
        month = parsed_date.month
        day = parsed_date.day
    # else:
    #     return ValueError
    if storage.setdefault(year, {'total': 0}).setdefault(month, {'total': 0}).get(day):
        storage[year][month][day] += number
        storage[year][month]['total'] += number
        storage[year]['total'] += number
    else:
        storage.setdefault(year, {'total': 0}).setdefault(month, {'total': 0})[day] = number
        storage[year][month]['total'] += number
        storage[year]['total'] += number
    print(storage)
    return f'Год {year} месяц {month} день {day}. Сумма трат: {number}'

@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    print(storage)
    expense = storage.setdefault(year, {'total': 0})['total']
    print(storage)
    return f'Сумма трат за год {year} равна {expense}'



@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    if 1 <= int(month) <= 12:
        expense_for_year = storage.setdefault(year, {'total': 0})['total']
        expense_for_month = storage[year].setdefault(month, {'total': 0})['total']
    else:
        abort(404)

    return (f'Сумма трат за год {year} равна {expense_for_year}<br>'
            f'Сумма трат за месяц {month} равна {expense_for_month}')

# @app.errorhandler(404)
# def page_not_found(error):
#     return f'Такого месяца не существует. Введите новый запрос.'


if __name__ == "__main__":
    app.run(debug=True)


