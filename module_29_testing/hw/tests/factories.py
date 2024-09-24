import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import factory
import factory.fuzzy as fuzzy
import random

from hw.main.app import db
from hw.main.models import Client, Parking, ClientParking


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    # credit_card = credit_card = factory.LazyAttribute(
    # lambda _: random.choice([factory.Faker('credit_card_number').evaluate(None, None, None), None]))  # factory.Faker('credit_card_number')  # fuzzy.FuzzyText(prefix="Card ")
    car_number = fuzzy.FuzzyText(prefix="Num ")   # factory.Faker('license_plate')  #
    # credit_card = factory.Faker('credit_card_number')

    @factory.lazy_attribute
    def credit_card(self):
        if random.choice([True, False]):
            return None
        return factory.Faker('credit_card_number')

class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker('address')
    count_places = factory.LazyAttribute(lambda x: random.randint(5, 15))
    count_available_places = factory.LazyAttribute(lambda obj: random.randint(0, obj.count_places))  # factory.SelfAttribute(count_places)
    opened = factory.LazyAttribute(lambda b: random.choice([True, False]))



class ClientParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ClientParking
        sqlalchemy_session = db.session

    client_id = factory.SubFactory(ClientFactory)
    parking_id = factory.SubFactory(ParkingFactory)
    time_in = factory.Faker('date_time_this_year', before_now=True, after_now=False)  # Случайная дата в этом году
    time_out = None  # Можно оставить None или задать позже
