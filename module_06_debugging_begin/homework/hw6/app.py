"""
Заменим сообщение "The requested URL was not found on the server" на что-то более информативное.
Например, выведем список всех доступных страниц с возможностью перехода по ним.

Создайте Flask Error Handler, который при отсутствии запрашиваемой страницы будет выводить
список всех доступных страниц на сайте с возможностью перехода на них.
"""

from flask import Flask, url_for
from werkzeug.exceptions import InternalServerError

app = Flask(__name__)


registered_endpoints_links = []

def register_of_endpoints(endpoint: str) -> None:
    def decorator(func):
        registered_endpoints_links.append(f'<a href="{endpoint}">{endpoint}</a>')
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator


# @app.errorhandler(404)
# def handle_exception(e: InternalServerError):
#     def has_no_empty_params(rule):
#         defaults = rule.defaults if rule.defaults is not None else ()
#         arguments = rule.arguments if rule.arguments is not None else ()
#         return len(defaults) >= len(arguments)
#
#     links = []
#     for rule in app.url_map.iter_rules():
#         # Filter out rules we can't navigate to in a browser
#         # and rules that require parameters
#         if "GET" in rule.methods and has_no_empty_params(rule):
#             url = url_for(rule.endpoint, **(rule.defaults or {}))
#             links.append((url, rule.endpoint))
#     return links


@app.errorhandler(404)
def handle_exception(e: InternalServerError):

    links = '\n; '.join(registered_endpoints_links[i] for i in range(0, len(registered_endpoints_links)))
    return (f'Доступные ссылки: {links}')


@register_of_endpoints('/dogs')
@app.route('/dogs')
def dogs():
    return 'Страница с пёсиками'


@register_of_endpoints('/cats')
@app.route('/cats')
def cats():
    return 'Страница с котиками'


@register_of_endpoints('/cats/<int:cat_id>')
@app.route('/cats/<int:cat_id>')
def cat_page(cat_id: int):
    return f'Страница с котиком {cat_id}'


@register_of_endpoints('/index')
@app.route('/index')
def index():
    return 'Главная страница'


if __name__ == '__main__':
    app.run(debug=True)
