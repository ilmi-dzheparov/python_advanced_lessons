from flask import Flask, Response, render_template_string
import os
import base64

app = Flask(__name__)

def generate_nonce():
    return base64.b64encode(os.urandom(16)).decode('utf-8')

@app.route('/')
def index():
    nonce = generate_nonce()
    html_content = f"""
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
    response.headers['Content-Security-Policy'] = f"default-src 'self'; script-src 'self' 'nonce-{nonce}';"
    return response

if __name__ == '__main__':
    app.run(port=8080, debug=True)
