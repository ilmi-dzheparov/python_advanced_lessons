"""
Довольно неудобно использовать встроенный валидатор NumberRange для ограничения числа по его длине.
Создадим свой для поля phone. Создайте валидатор обоими способами.
Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина,
а также опциональный параметр message (см. рекомендации к предыдущему заданию).
"""
from typing import Optional

from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.validators import ValidationError


def number_length(min: int, max: int, message: Optional[str] = None):
    def _number_length(form: FlaskForm, field: Field):
        if not min <= field.data <= max:
            raise ValidationError(message or f"Number must be between {min} and {max}")

    return _number_length


class NumberLength:
    def __init__(self, min: int, max: int, message: Optional[str] = None):
        self.min_value = min
        self.max_value = max
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        if not self.min_value <= field.data <= self.max_value:
            raise ValidationError(self.message or f"Number must be between {self.min_value} and {self.max_value}")


