from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import APISpec, Swagger
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

class BookListResource(Resource):
    def get(self) -> tuple[list[dict], int]:
        """
        This is an endpoint for obtaining the books list
        ---
        tags:
          - books
        responses:
          200:
            description: Books data
            schema:
              type: array
              items:
                $ref: '#/definitions/Book'
        :return:
        """
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200


    def post(self) -> tuple[dict, int]:
        """
        This is an endpoint for book creation
        ---
        tags:
         - books
        parameters:
         - in: body
           name: new books parameters
           schema:
             $ref: '#/definitions/Book'
        responses:
         201:
           description: The book has been created
           schema:
             $ref: '#/definitions/Book'

        :return:
        """
        data = request.json
        book_schema = BookSchema(context={"id": None})

        try:
            book = book_schema.load(data)
            print(book)
            author_data = book["author"]
            print(f'ssss {author_data}')

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
    def get(self, book_id: int) -> tuple[dict, int]:
        """
        This is an endpoint for obtaining the book by id
        ---
        tags:
         - books
        parameters:
         - in: path
           name: book_id
           required: true
           description: ID of the book to update
           type: integer
           format: int64
        responses:
          200:
            description: Books data
            schema:
              type: array
              items:
                $ref: '#/definitions/Book'
        :return:
        """
        schema = BookSchema()
        return schema.dump(get_book_by_id(book_id)), 200


    def put(self, book_id: int) -> tuple[dict, int]:
        """
        This is an endpoint for book updating
        ---
        tags:
         - books
        parameters:
         - in: path
           name: book_id
           required: true
           description: ID of the book to update
           type: integer
           format: int64
         - in: body
           name: new books parameters
           schema:
             $ref: '#/definitions/Book'
        responses:
         201:
           description: The book has been updated
           schema:
             $ref: '#/definitions/Book'

        :return:
        """
        data = request.json
        print(data)
        book_schema = BookSchema(context={"id": book_id})
        try:
            book = book_schema.load(data)
            author_data = book["author"]
            print(f'ssss {author_data}')
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


    def delete(self, book_id: int) -> tuple[list[dict], int]:
        """
        This is an endpoint for deleting the book by id
        ---
        tags:
         - books
        parameters:
         - in: path
           name: book_id
           required: true
           description: ID of the book to delete
           type: integer
           format: int64
        responses:
          200:
            description: Books data
            schema:
              type: array
              items:
                $ref: '#/definitions/Book'
        :return:
        """
        delete_book_by_id(book_id)
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200


class AuthorListResource(Resource):
    def post(self) -> tuple[dict, int]:
        """
        This is an endpoint for author creation
        ---
        tags:
         - authors
        parameters:
         - in: body
           name: new author parameters
           schema:
             $ref: '#/definitions/Author'
        responses:
         201:
           description: The author has been created
           schema:
             $ref: '#/definitions/Author'

        :return:
        """
        data = request.json
        schema = AuthorSchema(context={"is_create": True})
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        author = add_author(author)
        return schema.dump(author), 201

    def get(self) -> tuple[list[dict], int]:
        """
        This is an endpoint for obtaining list of authors
        ---
        tags:
         - authors
        responses:
         200:
           description: The list of  authors
           schema:
             $ref: '#/definitions/Author'

        :return:
        """
        schema = AuthorSchema()
        return schema.dump(get_all_authors(), many=True), 200


class AuthorResource(Resource):
    def get(self, author_id: int) -> tuple[dict, int]:
        """
        This is an endpoint for obtaining list of authors by author id
        ---
        tags:
         - authors
        parameters:
         - in: path
           name: author_id
           required: true
           description: ID of the author to get list of books
           type: integer
           format: int64
        responses:
         200:
           description: The list of  authors by author_id
           schema:
             $ref: '#/definitions/Author'

        :return:
        """
        schema = BookSchema()
        return schema.dump(get_books_by_author_id(author_id), many=True), 200


    def delete(self, author_id: int) -> tuple[list[dict], int]:
        """
        This is an endpoint for deleting the author by id
        ---
        tags:
         - authors
        parameters:
         - in: path
           name: author_id
           required: true
           description: ID of the author to delete
           type: integer
           format: int64
        responses:
          200:
            description: Books data
            schema:
              type: array
              items:
                $ref: '#/definitions/Book'
        :return:
        """
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
api.add_resource(AuthorResource,"/api/authors/<int:author_id>")


if __name__ == "__main__":
    init_db(initial_records_authors=DATA_AUTHOR, initial_records=DATA)
    app.run(debug=True)
