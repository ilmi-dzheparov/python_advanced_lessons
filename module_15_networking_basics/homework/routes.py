from decimal import Decimal

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DecimalField
from wtforms.validators import InputRequired
from models import add_room, init_db, get_rooms, Hotel, book_room
from flask import Flask, jsonify, render_template, request, redirect


app: Flask = Flask(__name__)
app.secret_key = "qwerty"


class AddRoomForm(FlaskForm):
    floor = IntegerField("Floor number", validators=[InputRequired()])
    beds = IntegerField("Beds number", validators=[InputRequired()])
    guestNum = IntegerField("Room number", validators=[InputRequired()])
    price = IntegerField("Price", validators=[InputRequired()])
    submit = SubmitField("Submit")


# @app.route("/add-room", methods=["GET", "POST"])
# def add_room_form() -> str:
#     form = AddRoomForm()
#     if request.method == "GET":
#         return render_template("add_room.html", form=form)
#     if request.method == "POST" and form.validate_on_submit():
#         # floor = form.floor.data
#         # beds = form.beds.data
#         # guestNum = form.guestNum.data
#         # price = Decimal(form.price.data)
#         # floor = request.form["floor"]
#         # beds = request.form["beds"]
#         # guestNum = request.form["guestNum"]
#         # price = request.form["price"]
#         print(price)
#         add_room(floor, beds, guestNum, price)
#         # add_room(request.form["floor"], request.form["beds"], request.form["guestNum"], request.form["price"])
#         # return redirect("/add-")
#         # return render_template("rooms_list.html", rooms=get_rooms()), 200
#         return jsonify({"floor": floor, "beds": beds, "guestNum": guestNum, "price": price}), 200
#     return render_template("add_room.html", form=form)


@app.route("/add-room", methods=["POST"])
def add_room_route():
    data = request.get_json()  # Получаем JSON данные из тела запроса
    floor = data.get("floor")
    beds = data.get("beds")
    guestNum = data.get("guestNum")
    price = data.get("price")
    print(price)
    add_room(floor, beds, guestNum, price)
    return (
        jsonify({"floor": floor, "beds": beds, "guestNum": guestNum, "price": price}),
        200,
    )


@app.route("/room")
def get_room():
    # return render_template("rooms_list.html", rooms=get_rooms()), 200
    guestsNum = request.args.get("guestsNum")
    rooms = [
        {
            "roomId": room.id,
            "floor": room.floor,
            "beds": room.beds,
            "guestNum": room.guest_num,
            "price": room.price,
        }
        for room in get_rooms()
    ]
    if guestsNum:
        rooms = [room for room in rooms if room["guestNum"] == int(guestsNum)]
    return jsonify({"rooms": rooms})


@app.route("/booking", methods=["POST"])
def booking():
    data = request.get_json()
    roomId = data.get("roomId")
    checkIn = data.get("bookingDates").get("checkIn")
    checkOut = data.get("bookingDates").get("checkOut")
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    if roomId:
        response = book_room(roomId, firstName, lastName, checkIn, checkOut)
        return response


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
