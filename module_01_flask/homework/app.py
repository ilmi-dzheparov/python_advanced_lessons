import datetime
import os
import random
import re

from flask import Flask

app = Flask(__name__)


@app.route('/hello_world')
def hello_world():
    return 'Привет, мир!'


cars_list =['Chevrolet', 'Renault', 'Ford', 'Lada']
@app.route('/cars')
def cars_print():
    return ', '.join(cars_list)


cats_list = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']
@app.route('/cats')
def cats_choice():
    return random.choice(cats_list)



@app.route('/get_time/now')
def get_time_now():
    current_time = datetime.datetime.now().time()
    return f"Точное время {current_time}"



@app.route('/get_time/future')
def get_time_en_hour():
    current_time_after_hour = (datetime.datetime.now() + datetime.timedelta(hours=1)).time()
    return f'Точное время через час будет {current_time_after_hour}'


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')

with open(BOOK_FILE) as book:
    book_content = book.read()

book_content_words = re.findall(r'\w+', book_content)

@app.route('/get_random_word')
def random_word():
    return random.choice(book_content_words)


count = 0
@app.route('/counter')
def counter_function():
    global count
    count += 1
    return f'Страница открылась {count} раз'


if __name__ == '__main__':
    app.run(debug=True)
