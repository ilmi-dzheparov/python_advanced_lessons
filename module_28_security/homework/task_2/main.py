from flask import Flask, request, Response
app = Flask(__name__)

# Шаблоны страниц
page_header = """
<!doctype html>
<html>
  <head>
    <!-- Internal game scripts/styles, mostly boring stuff -->
    <script src="/static/game-frame.js"></script>
    <link rel="stylesheet" href="/static/game-frame-styles.css" />
  </head>
  <body id="level1">
    <img src="/static/logos/level1.png">
    <div>
"""

page_footer = """
    </div>
  </body>
</html>
"""

main_page_markup = """
<form action="" method="GET">
  <input id="query" name="query" value="Enter query here..." onfocus="this.value=''">
  <input id="button" type="submit" value="Search">
</form>
"""


@app.route('/', methods=['GET'])
def main_page():
    # Установка CSP заголовка
    response = Response()
    # response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self';"

    # Установка заголовка X-XSS-Protection
    # response.headers['X-XSS-Protection'] = '1; mode=block'
    # response.headers['X-XSS-Protection'] = '0'

    query = request.args.get('query', None)
    if query is None:
        # Показ главной страницы поиска
        response.set_data(page_header + main_page_markup + page_footer)
    else:
        # Обработка запроса поиска
        sanitized_query = escape(query)
        message = f"Sorry, no results were found for <b>{query}</b>."
        message += " <a href='?'>Try again</a>."
        response.set_data(page_header + message + page_footer)

    return response


def escape(s):
    """Функция для экранирования пользовательского ввода."""
    return s.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')


if __name__ == '__main__':
    app.run(port=8080, debug=True)
