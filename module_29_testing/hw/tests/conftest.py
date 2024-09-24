import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from datetime import datetime

import pytest
from flask import template_rendered
from hw.main.app import create_app, db as _db
from hw.main.models import Client, Parking, ClientParking


@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()
        test_client = Client(
            name="name",
            surname="surname",
            credit_card='credit_card',
            car_number='car_number')
        test_parking_1 = Parking(
            address="address_2",
            opened=True,
            count_places=4,
            count_available_places=4)
        test_parking_2 = Parking(
            address="address",
            opened=True,
            count_places=4,
            count_available_places=4)
        # Лог с фиксацией времени въезда и выезда
        test_client_parking = ClientParking(
            client_id=1,
            parking_id=1,
            time_in=datetime(2024, 9, 22, 10, 0, 0),
            time_out=None #datetime(2024, 9, 22, 12, 0, 0)
        )

        _db.session.add(test_client)
        _db.session.add(test_parking_1)
        _db.session.add(test_parking_2)
        _db.session.add(test_client_parking)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


# @pytest.fixture
# def captured_templates(app):
#     recorded = []
#
#     def record(sender, template, context, **extra):
#         recorded.append((template, context))
#
#     template_rendered.connect(record, app)
#     try:
#         yield recorded
#     finally:
#         template_rendered.disconnect(record, app)


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
