import datetime

from flask import Flask, jsonify, abort, request
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Date,
    Boolean,
    Float,
    case,
    func,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker, declarative_base

app = Flask(__name__)
engine = create_engine("sqlite:///python.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, default=datetime.date.today, nullable=False)
    author_id = Column(Integer, nullable=False)

    def __repr__(self):
        return f"Book {self.name} -> count: {self.count}"

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)

    def __repr__(self):
        return f"Author {self.name} {self.surname}"


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    phone = Column(String(11), nullable=False)
    email = Column(String(50), nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"Student {self.name} {self.surname}"


    @classmethod
    def get_students_with_scholarship(cls):
        """Возвращает список студентов проживающих в общежитии"""
        return session.query(Student).filter(Student.scholarship == True).all()

    @classmethod
    def get_students_with_average_score(cls, av_s: float):
        """Получение списка студентов, у которых средний балл выше балла, который будет передан входным параметров в функцию"""
        return session.query(Student).filter(Student.average_score > av_s).all()


class ReceivingBook(Base):
    __tablename__ = "receiving_books"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    date_of_issue = Column(Date, nullable=False, default=datetime.date.today())
    date_of_return = Column(Date)

    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return:
            return (self.date_of_return - self.date_of_issue).days
        else:
            return (datetime.date.today() - self.date_of_issue).days

    @count_date_with_book.expression
    def count_date_with_book(cls):
        """Генерирует SQL-выражение для подсчета дней."""
        return case(
            (
                cls.date_of_return != None,
                func.julianday(cls.date_of_return) - func.julianday(cls.date_of_issue),
            ),
            else_=func.julianday(func.current_date())
            - func.julianday(cls.date_of_issue),
        )


@app.before_request
def before_request_func():
    Base.metadata.create_all(bind=engine)


@app.route("/books", methods=["GET"])
def get_all_books():
    """Получение всех книг в библиотеке"""
    books = session.query(Book).all()
    books_list = []
    for book in books:
        books_list.append(book.to_json())
    return jsonify(books_list=books_list), 200


@app.route("/debtors", methods=["GET"])
def get_debtors():
    """Получение списка должников, которые держат книги у себя более 14 дней"""
    debtors = []
    student_ids = (
        session.query(ReceivingBook.student_id)
        .filter(ReceivingBook.count_date_with_book > 14)
        .all()
    )
    for id in student_ids:
        debtors.append(id[0])
    return jsonify(debtors=debtors)


@app.route("/book/issue", methods=['POST'])
def book_issue():
    """Выдать книгу студенту (POST - входные параметры ID книги и ID студента)"""
    book_id = request.form.get('book_id', type = int)
    student_id = request.form.get('student_id', type=int)
    book = session.query(Book).filter(Book.id == book_id).one_or_none()
    if book is None:
        abort(404, description="Book not found")
    if book.count <= 0:
        return jsonify({"message": "No books in stock"}), 400
    student = session.query(Student.id).filter(Student.id == student_id).one_or_none()
    if student is None:
        abort(404, description="Student not found")
    book_for_issue = ReceivingBook(book_id=book_id, student_id=student_id)
    session.add(book_for_issue)
    book.count -= 1
    session.commit()
    return jsonify({"message": "Book issued successfully"}), 200


@app.route("/book/return", methods=['POST'])
def book_return():
    """Сдать книгу в библиотеку (POST - входные параметры ID книги и ID студента)"""
    book_id = request.form.get('book_id', type = int)
    student_id = request.form.get('student_id', type=int)

    book = session.query(Book).filter(Book.id == book_id).one_or_none()
    if book is None:
        abort(404, description="Book not found")

    received_book = session.query(ReceivingBook).filter(
        ReceivingBook.book_id == book_id,
        ReceivingBook.student_id == student_id).first()
    if received_book is None:
        abort(404, description="Book is not received by student")
    session.delete(received_book)
    book.count += 1
    session.commit()
    return jsonify({"message": "Book returned successfully"}), 200


@app.route('/books/search', methods=['GET'])
def search_books():
    """Поиск книги по названию"""
    query = request.args.get('query', '')
    if not query:
        abort(400, description="Query parameter is required")

    books = session.query(Book).filter(Book.name.ilike(f'%{query}%')).all()

    if not books:
        return jsonify({"message": "No books found matching the query"}), 404

    books_list = [book.to_json() for book in books]
    return jsonify(books=books_list), 200


if __name__ == "__main__":
    app.run()
    # print(Student.get_students_with_scholarship())
