import csv
from typing import Optional

from flask import Flask
from werkzeug.exceptions import InternalServerError

app = Flask(__name__)

@app.route("/bank_api/<branch>/<int:person_id>")
def bank_api(branch: str, person_id: int):
    branch_card_file_name = f"bank_data/{branch}.csv"
    with open(branch_card_file_name, "r") as fi:
        csv_reader = csv.DictReader(fi, delimiter=",")
        for record in csv_reader:
            if int(record['id']) == person_id:
                return record["name"]
        else:
            return "Person not found", 400

@app.errorhandler(InternalServerError)
def handle_exception(e: InternalServerError) -> object:
    original: Optional[Exception] = getattr(e, "original_exception", None)
    if isinstance(original, FileNotFoundError):
        with open("invalid_error.log", "a") as fo:
            fo.write(
                f"Tried to access {original.filename}. Exception info: {original.strerror}\n"
            )
    elif isinstance(original, OSError):
        with open("invalid_error.log", "a") as fo:
            fo.write(
                f"Tried to access a card. Exception info: {original.strerror}\n"
            )
    return "Internal server error", 500


if __name__ == "__main__":
    app.run()
