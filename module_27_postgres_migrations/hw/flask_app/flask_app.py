import json

from sqlalchemy import Column, Integer, String, Float, Boolean, Text, \
    create_engine, Sequence, Identity, ForeignKey, delete, func, select, text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from flask import Flask, jsonify, request
from typing import Dict, Any
from sqlalchemy.dialects.postgresql import insert, ARRAY, JSON

app = Flask(__name__)
engine = create_engine('postgresql+psycopg2://admin:admin@postgres/skillbox_db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# СREATE TABLE coffee (
#     id SERIAL NOT NULL,
#     title VARCHAR(200) NOT NULL,
#     origin VARCHAR(200),
#     intensifier VARCHAR(100),
#     notes VARCHAR[],
#     PRIMARY KEY (id)
# )

# CREATE TABLE users (
#     id SERIAL NOT NULL,
#     name VARCHAR(50) NOT NULL,
#     has_sale BOOLEAN,
#     address JSON,
#     coffee_id INTEGER,
#     PRIMARY KEY (id),
#     FOREIGN KEY(coffee_id) REFERENCES coffee (id)
# )


class Coffee(Base):
    __tablename__ = 'coffee'

    id = Column(Integer, Sequence('coffee_id_seq'), primary_key=True)
    title = Column(String(200), nullable=False)
    origin = Column(String(200))
    intensifier = Column(String(100))
    notes = Column(ARRAY(Text))

    # user_id = Column(Integer, ForeignKey('users.id'))
    # user = relationship("User", backref="products")

    def __repr__(self):
        return f"Кофе {self.title}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    has_sale = Column(Boolean, default=False)
    address = Column(JSON)
    coffee_id = Column(Integer, ForeignKey('coffee.id'))
    coffee = relationship("Coffee", backref="users")

    def __repr__(self):
        return f"Пользователь {self.username}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


@app.before_request
def before_first_request():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with open('coffee.json', 'r') as file:
        data_coffee = json.load(file)
    with open('users.json', 'r') as file:
        data_users = json.load(file)

    objects = []
    for data in data_coffee:
        title = data["title"]
        origin = data["origin"]
        intensifier = data["intensifier"]
        notes = data["notes"]
        objects.append(Coffee(title=title,
                              origin=origin,
                              intensifier=intensifier,
                              notes=notes)
                       )
    for data in data_users:
        name = data["name"]
        has_sale = data["has_sale"]
        address = data["address"]
        coffee_id = data["coffee_id"]
        objects.append(User(name=name,
                            has_sale=has_sale,
                            address=address,
                            coffee_id=coffee_id)
                       )

    session.bulk_save_objects(objects)
    session.commit()


# @app.route('/products/<int:id>', methods=['DELETE'])
# def delete_product_handler(id: int):
#     result = delete(Product).returning(Product.id, Product.title). \
#         where(Product.id == id)
#     deleted_row = session.execute(result).fetchone()
#     if deleted_row:
#         deleted_row_json = dict(id=deleted_row[0], title=deleted_row[1])
#         return jsonify(delete_row_attrs=deleted_row_json)


@app.route('/user', methods=['POST'])
def add_user_handler():
    data = request.get_json()
    coffee_id = data["coffee_id"]
    coffee_exists = session.query(Coffee.id).filter_by(id=coffee_id).scalar()
    if not coffee_exists:
        return jsonify({"error": f"Coffee with id: {coffee_id} does not exist in DB"}), 400
    new_user = User(name=data.get("name"),
                    has_sale=data.get("origin", False),
                    address=data.get("address"),
                    coffee_id=data.get("coffee_id")
                    )
    session.add(new_user)
    session.commit()
    last_user = session.query(User).order_by(User.id.desc()).first()
    return last_user.to_json(), 200


@app.route('/search_coffee', methods=['GET'])
def search_coffee_handler():
    query = request.args.get('title', '')
    if not query:
        return jsonify({"error": "No search query provided"}), 400

    # Создаем запрос для полнотекстового поиска
    # search_query = func.plainto_tsquery('english', query)

    # Выполняем запрос с динамическим преобразованием текста
    # results = session.query(Coffee).filter(
    #     func.to_tsvector('english', Coffee.title).op('@@')(search_query)
    # ).all()

    # Выполняем запрос для поиска по названию кофе с использованием полнотекстового поиска
    # results = session.execute(
    #     select(Coffee).where(
    #         Coffee.title.match(query, postgresql_regconfig='english')
    #     )
    # ).scalars().all()

    results = session.execute(
        select(Coffee).where(func.to_tsvector('english', Coffee.title) \
                             .match(query, postgresql_regconfig='english'))
    ).scalars().all()

    # Форматируем результаты
    results_json = [coffee.to_json() for coffee in results]
    return jsonify(results_json), 200


@app.route('/unique_notes', methods=['GET'])
def unique_notes_handler():
    # Получаем все элементы массива `notes` и делаем их уникальными
    unique_notes = session.execute(
        select(func.unnest(Coffee.notes))  # unnest "разворачивает" массив в отдельные строки
        ).scalars().all()

    # Преобразуем в уникальный список
    unique_notes_set = set(unique_notes)

    return jsonify({"unique_notes": list(unique_notes_set)}), 200


@app.route('/users/country', methods=['GET'])
def get_users_by_country_handler():
    country = request.args.get('country', '').lower()
    if not country:
        return jsonify({"error": "No search query provided"}), 400

    users = session.query(User.id, User.name) \
        .filter(func.lower(func.json_extract_path_text(User.address, 'country')) == country).all()
    if not users:
        return jsonify({"error": f"Country {country} does not exist in DB"}), 400

    result = [{"id": user.id, "name": user.name} for user in users]

    return jsonify(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
