import datetime
from zoneinfo import available_timezones

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from typing import List
from datetime import datetime

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parking.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .models import Client, Parking, ClientParking

    @app.before_request
    def before_request_func():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()


    @app.route("/clients", methods=["POST"])
    def create_client_handler():
        """Создание нового клиента"""
        data = request.get_json()
        name = data["name"]
        surname = data["surname"]
        credit_card = data.get("credit_card", None)
        car_number = data["car_number"]
        new_client = Client(name=name,
                            surname=surname,
                            credit_card=credit_card,
                            car_number=car_number)
        db.session.add(new_client)
        db.session.commit()
        client = db.session.query(Client).order_by(Client.id.desc()).first()
        return client.to_json(), 201


    @app.route("/clients", methods=["GET"])
    def get_all_clients_handler():
        """Получение списка всех клиентов"""
        clients = db.session.query(Client).all()
        clients_list = [c.to_json() for c in clients]
        return jsonify(clients_list), 200



    @app.route("/clients/<client_id>", methods=["GET"])
    def get_client_by_id_handler(client_id: int):
        """Получение информации клиента по ID"""
        client = db.session.query(Client).filter(Client.id == client_id).one_or_none()
        if client is not None:
            return jsonify(client.to_json()), 200
        else:
            return jsonify({"Error": f"Client with id: {client_id} does not exist"}), 401


    @app.route("/parkings", methods=["POST"])
    def create_parking_handler():
        """Создание новой парковочной зоны"""
        data = request.get_json()
        address = data["address"]
        count_places = data["count_places"]

        new_parking = Parking(address=address,
                            count_places=count_places,
                            count_available_places=count_places)
        db.session.add(new_parking)
        db.session.commit()
        parking = db.session.query(Parking).order_by(Parking.id.desc()).first()
        return parking.to_json(), 201


    @app.route("/client_parkings", methods=["POST"])
    def create_client_parking_handler():
        """Заезд на парковку"""
        data = request.get_json()
        client_id = data["client_id"]
        parking_id = data["parking_id"]
        client = db.session.query(Client.id).filter(Client.id == client_id).scalar()
        parking = db.session.query(Parking).filter(Parking.id == parking_id).one_or_none()

        if client is None:
            return jsonify({"Error": f"Client with id: {client_id} does not exist"}), 401
        if parking is None:
            return jsonify({"Error": f"Parking with id: {parking_id} does not exist"}), 401

        available_places = parking.count_available_places
        if available_places > 0:
            new_client_parking = ClientParking(client_id=client_id,
                                               parking_id=parking_id,
                                               time_in=datetime.now())
            db.session.add(new_client_parking)
            parking.count_available_places -= 1
            db.session.commit()
            client_parking = db.session.query(ClientParking).order_by(ClientParking.id.desc()).first()
            parking_by_id = db.session.query(Parking).filter(Parking.id == parking_id).first()

            return jsonify([client_parking.to_json(), parking_by_id.to_json()]), 201
        else:
            return jsonify({"Message": f"Parking with id: {parking_id} does not have free places"}), 401

    @app.route("/client_parkings", methods=["DELETE"])
    def delete_client_parking_handler():
        """Выезд с парковки"""
        data = request.get_json()
        client_id = data["client_id"]
        parking_id = data["parking_id"]
        client_parking = db.session.query(ClientParking).filter(
            ClientParking.client_id == client_id,
            ClientParking.parking_id == parking_id).order_by(
            ClientParking.id.desc()).first()
        if client_parking is not None and client_parking.time_out is None:
            client_credit_card = db.session.query(Client.credit_card).filter(Client.id == client_id).scalar()
            print(client_credit_card)
            if client_credit_card is not None:
                client_parking.time_out = datetime.now()
                parking = db.session.query(Parking).filter(Parking.id == parking_id).first()
                parking.count_available_places += 1
                db.session.commit()
                client_parking = db.session.query(ClientParking).order_by(ClientParking.id.desc()).first()
                parking_by_id = db.session.query(Parking).filter(Parking.id == parking_id).first()
                return jsonify([client_parking.to_json(), parking_by_id.to_json()]), 201
            else:
                return jsonify(
                    {"Message": f"Client with id: {client_id} does not have credit card. Please input credit card for payment"}), 401
        else:
            return jsonify({"Message": f"Parking with id: {parking_id} does not have client with id {client_id}"}), 401


    return app
