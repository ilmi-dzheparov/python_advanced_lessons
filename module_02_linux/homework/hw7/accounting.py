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

from flask import Flask

app = Flask(__name__)

storage = {}


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int):
    year = date[:4]
    month = date[4:6]
    day = date[-2:]
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

@app.route("/calculate/<year>")
def calculate_year(year: str):
    expense = storage.setdefault(year, {'total': 0})['total']
    print(storage)
    return f'Сумма трат за год {year} равна {expense}'



@app.route("/calculate/<year>/<month>")
def calculate_month(year: str, month: str):
    expense_for_year = storage.setdefault(year, {'total': 0})['total']
    expense_for_month = storage[year].setdefault(month, {'total': 0})['total']
    return (f'Сумма трат за год {year} равна {expense_for_year}<br>'
            f'Сумма трат за месяц {month} равна {expense_for_month}')


if __name__ == "__main__":
    app.run(debug=True)
