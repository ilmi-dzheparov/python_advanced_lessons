import reprlib
from typing import List, Optional
from flask import Flask, request

app = Flask(__name__)

@app.route("/search/", methods=["GET"],)
def search():
    cell_tower_ids: List[int] = request.args.getlist(
        "cell_tower_id", type=int
    )
    if not cell_tower_ids:
        return f"You must specify at least one cell_tower_id", 400

    phone_prefixes: List[str] = request.args.getlist("phone_prefix")

    protocols: List[str] = request.args.getlist("protocol")

    signal_level: Optional[float] = request.args.get(
        "signal_level", type=float, default=None,
    )

    return (
        f"Search for {cell_tower_ids} cell towers. Search criteria.\n"
        f"phone_prefixes={phone_prefixes}\n"
        f"protocols={protocols}\n"
        f"signal_level={signal_level}"
    )

if __name__ == "__main__":
    app.run(debug=True)

#/search/?cell_tower_id=1&cell_tower_id=2&cell_tower_id=3&phone_prefix=999*&phone_prefix=921*&signal_level=-100