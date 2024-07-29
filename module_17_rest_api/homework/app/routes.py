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


class BookListResource(Resource):
    def get(self) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200


    # def post(self) -> tuple[dict, int]:
    #     data = request.json
    #     schema = BookSchema(context={"id": None})
    #     try:
    #         book = schema.load(data)
    #     except ValidationError as exc:
    #         return exc.messages, 400
    #
    #     book = add_book(book)
    #     return schema.dump(book), 201


    def post(self) -> tuple[dict, int]:
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
        schema = BookSchema()
        return schema.dump(get_book_by_id(book_id)), 200


    def put(self, book_id: int) -> tuple[dict, int]:
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

    # def patch(self, book_id: int) -> tuple[dict, int]:
    #     data = request.json
    #     schema = BookSchema(partial=True, context={"id": book_id})
    #     try:
    #         book = schema.load(data)
    #         print(book)
    #         book.id = book_id
    #     except ValidationError as exc:
    #         return exc.messages, 400
    #     existing_book = get_book_by_id(book_id)
    #     if not existing_book:
    #         return {"message": "Book not found"}, 400
    #     if not book.title:
    #         book.title = existing_book.title
    #     if not book.author:
    #         book.author = existing_book.author
    #         update_book_by_id(book)
    #     return schema.dump(book), 201

    def delete(self, book_id: int) -> tuple[list[dict], int]:
        delete_book_by_id(book_id)
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200


class AuthorListResource(Resource):
    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = AuthorSchema(context={"is_create": True})
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        author = add_author(author)
        return schema.dump(author), 201

    def get(self) -> tuple[list[dict], int]:
        schema = AuthorSchema()
        return schema.dump(get_all_authors(), many=True), 200


class AuthorResource(Resource):
    def get(self, author_id: int) -> tuple[dict, int]:
        schema = BookSchema()
        return schema.dump(get_books_by_author_id(author_id), many=True), 200


    def delete(self, author_id: int) -> tuple[list[dict], int]:
        delete_author_by_id(author_id)
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200



api.add_resource(BookListResource, "/api/books")
api.add_resource(BookResource, "/api/books/<int:book_id>")
api.add_resource(AuthorListResource, "/api/authors")
api.add_resource(AuthorResource,"/api/authors/<int:author_id>")


if __name__ == "__main__":
    init_db(initial_records_authors=DATA_AUTHOR, initial_records=DATA)
    app.run(debug=True)
