from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class BookForm(FlaskForm):
    book_title = StringField('Book Title', validators=[InputRequired()])
    author_name = StringField('Author name', validators=[InputRequired()])
    submit = SubmitField('Submit')