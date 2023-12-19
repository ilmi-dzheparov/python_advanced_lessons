import json
from urllib.parse import unquote_plus
from flask import Flask, request

app = Flask(__name__)

@app.route("/sum", methods=["POST"])
def _sum():
    array1 = request.form.getlist("array1", type=int)
    array2 = request.form.getlist("array2", type=int)
    result = ",".join(str(a1 + a2) for a1, a2 in zip(array1, array2))
    return f"Array of sums is [{result}]"

@app.route("/sum2", methods=["POST"])
def _sum2():
    arrays = {}
    form_data = request.get_data(as_text=True)
    request_data = unquote_plus(form_data)
    print(f"request_data={request_data}")
    for encoded_chunk in request_data.split("&"):
        print(encoded_chunk)
        k, v = encoded_chunk.split("=")
        print(k, v)
        arrays[k] = [int(it) for it in v.split(",")]
    result_str = ",".join(
        str(a1 + a2) for a1, a2 in zip(arrays['array1'], arrays['array2'])
    )

    return f"Array of sums is [{result_str}]"

@app.route("/sum3", methods=["POST"])
def _sum3():
    form_data = request.get_data(as_text=True)
    data_object = json.loads(form_data)
    print(f"request_data={form_data}")
    result_str = ",".join(
        str(a1 + a2) for a1, a2 in zip(data_object['array1'], data_object['array2'])
    )

    return f"Array of sums is [{result_str}]"

@app.route("/sum4", methods=["POST"])
def _sum4():
    array = []
    form_data = request.get_data(as_text=True)
    data_object = json.loads(form_data)
    print(f"request_data={form_data}")
    for i in range(0, len(data_object['array'])-1):
        print(data_object['array'][i])
        if data_object['array'][i+1] < data_object['array'][i]:
            array = data_object['array'][i+1:] + data_object['array'][:i+1]
            return f"Array is {array}"

    array = data_object['array']
    return f"Array is {array}"


if __name__ == "__main__":
    app.run(debug=True)