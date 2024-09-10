from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
       <meta charset="UTF-8">
       <title>Title</title>
    </head>
    <body>
       <h1>Hello, World!</h1>
       <script>
         alert("Hacked!!!");
       </script>
    </body>
    </html>
    """
    response = Response(html_content)
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self';"
    # response.headers['X-XSS-Protection'] = '1; mode=block'
    # response.headers['X-XSS-Protection'] = '0'
    return response

if __name__ == '__main__':
    app.run(port=8080, debug=True)
