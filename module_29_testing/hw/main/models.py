from email.policy import default
from enum import unique

from .app import db
from typing import Dict, Any

class Client(db.Model):
    __tablename__ = "clients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50), default=None)
    car_number = db.Column(db.String(10))

    def __repr__(self):
        return f"Клиент {self.name} {self.surname}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Parking(db.Model):
    __tablename__ = "parkings"
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean, default=True)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Парковка {self.id} Количество мест: {self.count_places}, \
        количество свободных мест: {self.count_available_places}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ClientParking(db.Model):
    __tablename__ = "client_parkings"
    id = db.Column(db.Integer, primary_key=True)
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime, default=None)
    __table_args__ = (
        db.UniqueConstraint('client_id', 'parking_id', name='unique_client_parking'),
    )
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    client = db.relationship("Client", backref="client_parkings")
    parking_id = db.Column(db.Integer, db.ForeignKey('parkings.id'))
    parking = db.relationship("Parking", backref="client_parkings")

    # Явный конструктор
    def __init__(self, client_id, parking_id, time_in, time_out=None):
        self.client_id = client_id
        self.parking_id = parking_id
        self.time_in = time_in
        self.time_out = time_out

    # def __repr__(self):
    #     return f"Парковка {self.id} Количество мест: {self.count_places}, \
    #         количество свободных мест: {self.count_available_places}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
