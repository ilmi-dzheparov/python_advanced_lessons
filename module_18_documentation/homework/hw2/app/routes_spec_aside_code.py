import json

from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import APISpec, Swagger
from flasgger.utils import swag_from
from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from models import (
    DATA,
    DATA_AUTHOR,
    get_all_books,
    init_db,
    add_book,
    update_book_by_id,
    delete_book_by_id,
    get_book_by_id,
    get_author_by_id,
    get_books_by_author_id,
    add_author,
    get_all_authors,
    delete_author_by_id,
    get_author_by_fullname,
    update_author_by_id,
)
from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)
spec = APISpec(
    title='BookList',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
    ],
)


with open('../swagger.json', 'r', encoding='utf-8') as f:
    swagger_dict = json.load(f)


class BookListResource(Resource):
    @swag_from('../swagger_get_all_books.yml')
    def get(self) -> tuple[list[dict], int]:

        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200


    @swag_from('../swagger_post_book.yml')
    def post(self) -> tuple[dict, int]:

        data = request.json
        book_schema = BookSchema(context={"id": None})

        try:
            book = book_schema.load(data)
            author_data = book["author"]

        except ValidationError as exc:
            return exc.messages, 400

        first_name = author_data.first_name
        second_name = author_data.second_name
        existing_author = get_author_by_fullname(first_name, second_name)
        if existing_author is not None:
            book.author = existing_author.id
            existing_author.middle_name = author_data.middle_name
        else:
            author = add_author(author_data)
            book.author = author.id

        book = add_book(book)
        return book_schema.dump(get_book_by_id(book.id)), 201


class BookResource(Resource):
    @swag_from('../swagger_get_book_by_id.yml')
    def get(self, book_id: int) -> tuple[dict, int]:
        schema = BookSchema()
        return schema.dump(get_book_by_id(book_id)), 200

    @swag_from('../swagger_update_book_by_id.yml')
    def put(self, book_id: int) -> tuple[dict, int]:
        data = request.json
        book_schema = BookSchema(context={"id": book_id})
        try:
            book = book_schema.load(data)
            author_data = book["author"]
        except ValidationError as exc:
            return exc.messages, 400

        book.id = book_id
        first_name = author_data.first_name
        second_name = author_data.second_name
        existing_author = get_author_by_fullname(first_name, second_name)
        if existing_author is not None:
            book.author = existing_author.id
            update_author_by_id(author_data.middle_name, existing_author.id)
        else:
            author = add_author(author_data)
            book.author = author.id
        update_book_by_id(book)
        return book_schema.dump(get_book_by_id(book_id)), 201

    @swag_from('../swagger_delete_book_by_id.yml')
    def delete(self, book_id: int) -> tuple[list[dict], int]:

        delete_book_by_id(book_id)
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200


class AuthorListResource(Resource):
    @swag_from(swagger_dict['paths']['/api/authors']['post'])
    def post(self) -> tuple[dict, int]:

        data = request.json
        schema = AuthorSchema(context={"is_create": True})
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        author = add_author(author)
        return schema.dump(author), 201

    @swag_from(swagger_dict['paths']['/api/authors']['get'])
    def get(self) -> tuple[list[dict], int]:

        schema = AuthorSchema()
        return schema.dump(get_all_authors(), many=True), 200


class AuthorResource(Resource):
    @swag_from(swagger_dict['paths']['/api/authors/{id}']['get'])
    def get(self, author_id: int) -> tuple[dict, int]:
        schema = BookSchema()
        return schema.dump(get_books_by_author_id(author_id), many=True), 200

    @swag_from(swagger_dict['paths']['/api/authors/{id}']['delete'])
    def delete(self, author_id: int) -> tuple[list[dict], int]:
        delete_author_by_id(author_id)
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200


template = spec.to_flasgger(
    app,
    definitions=[BookSchema],
)
swagger = Swagger(app, template=template)

api.add_resource(BookListResource, "/api/books")
api.add_resource(BookResource, "/api/books/<int:book_id>")
api.add_resource(AuthorListResource, "/api/authors")
api.add_resource(AuthorResource, "/api/authors/<int:author_id>")

if __name__ == "__main__":
    init_db(initial_records_authors=DATA_AUTHOR, initial_records=DATA)
    app.run(debug=True)
