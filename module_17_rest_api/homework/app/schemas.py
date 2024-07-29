from marshmallow import Schema, fields, validates, ValidationError, post_load, EXCLUDE, validates_schema

from models import get_book_by_title, Book, get_author_by_id, get_author_by_fullname, Author


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    second_name = fields.Str(required=True)
    middle_name = fields.Str(missing=None)

    @validates_schema
    def validate_fullname(self, data, **kwargs):
        if self.context.get("is_create", False):  # Default to True if not provided
            first_name = data.get("first_name")
            second_name = data.get("second_name")
            print(f"Validating fullnmae with data: {data}")
            if get_author_by_fullname(first_name, second_name) is not None:
                raise ValidationError(
                    'Author {first_name} {second_name} already exists, '
                    'please use a different author.'.format(first_name=first_name, second_name=second_name)
                )

    @post_load
    def create_author(self, data, **kwargs):
        return Author(**data)


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Nested(AuthorSchema(), required=True)

    @validates('title')
    def validate_title(self, title: str) -> None:
        book_id = self.context.get('id')
        print(f"Validating book with data: {title}")
        if get_book_by_title(title, book_id) is not None:
            raise ValidationError(
                'Book with title "{title}" already exists, '
                'please use a different title.'.format(title=title)
            )

    # @validates('author')
    # def validate_author(self, author: int) -> None:
    #     print(f"Validating author with data: {author}")
    #     if get_author_by_id(author) is None:
    #         raise ValidationError(
    #             'Author {author} does not exist, '
    #             'please use a different author.'.format(author=author)
    #         )

    @post_load
    def create_book(self, data: dict, **kwargs) -> Book:
        return Book(
            title=data.get('title'),
            author=data.get('author'),
            id=data.get('id')
        )
