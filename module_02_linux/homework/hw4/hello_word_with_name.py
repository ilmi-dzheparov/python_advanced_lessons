"""
Реализуйте endpoint /hello-world/<имя>, который возвращает строку «Привет, <имя>. Хорошей пятницы!».
Вместо хорошей пятницы endpoint должен уметь желать хорошего дня недели в целом, на русском языке.

Пример запроса, сделанного в субботу:

/hello-world/Саша  →  Привет, Саша. Хорошей субботы!
"""
from datetime import datetime
import sys

from flask import Flask


app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)





