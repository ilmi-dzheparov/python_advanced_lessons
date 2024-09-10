from flask import Flask, jsonify, request, Response

app = Flask(__name__)


@app.route('/get_example', methods=['GET'])
def handler():
    print(request.headers)
    return jsonify({"Hello": "User"})


@app.route('/post_example', methods=['POST'])
def handler_post():
    data = request.get_json()
    print(request.headers)
    return jsonify({"Received Data": data}), 200


@app.route('/put_example', methods=['PUT'])
def post_example():
    data = {'message': 'This is a PUT request example'}
    return jsonify(data)


@app.after_request
def add_cors(response: Response):
    response.headers['Access-Control-Allow-Origin'] = 'https://www.google.com'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-My-Fancy-Header'
    return response


if __name__ == '__main__':
    app.run(port=8080, debug=True)
