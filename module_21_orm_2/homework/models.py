import re
from datetime import datetime, date
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
    ForeignKey,
    DateTime, event,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,
    relationship,
    backref,
    validates,
)

engine = create_engine("sqlite:///python.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    author = relationship(
        "Author", backref=backref("books", cascade="all, delete-orphan", lazy="select")
    )
    students = relationship("ReceivingBook", back_populates="book")

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
    books = relationship("ReceivingBook", back_populates="student")

    def __repr__(self):
        return f"Student {self.name} {self.surname}"

    # @validates("phone")
    # def validate_phone(self, key, phone):
    #     """Проверяет, что номер телефона соответствует формату +7(9**) -*** - ** - **"""
    #     if not re.match(r"^\+7\(9\d{2}\)-\d{3}-\d{2}-\d{2}$", phone):
    #         raise ValueError(
    #             "Invalid phone number format. It should be +7(9**) -*** - ** - **"
    #         )
    #     return phone

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
    # id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
    date_of_issue = Column(DateTime, default=datetime.now)
    date_of_return = Column(DateTime, nullable=True)
    student = relationship("Student", back_populates="books")
    book = relationship("Book", back_populates="students")

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


def insert_data():
    authors = [
        Author(name="Александр", surname="Пушкин"),
        Author(name="Лев", surname="Толстой"),
        Author(name="Михаил", surname="Булгаков"),
    ]
    authors[0].books.extend(
        [
            Book(name="Капитанская дочка", count=5, release_date=date(1836, 1, 1)),
            Book(name="Евгений Онегин", count=3, release_date=date(1838, 1, 1)),
        ]
    )
    authors[1].books.extend(
        [
            Book(name="Война и мир", count=10, release_date=date(1867, 1, 1)),
            Book(name="Анна Каренина", count=7, release_date=date(1877, 1, 1)),
        ]
    )
    authors[2].books.extend(
        [
            Book(name="Морфий", count=5, release_date=date(1926, 1, 1)),
            Book(name="Собачье сердце", count=3, release_date=date(1925, 1, 1)),
        ]
    )
    students = [
        Student(
            name="Nik",
            surname="Ivanov",
            phone="111",
            email="nik@",
            average_score=4,
            scholarship=True,
        ),
        Student(
            name="Vlad",
            surname="Petrov",
            phone="222",
            email="vlad@",
            average_score=4.6,
            scholarship=True,
        ),
    ]
    session.add_all(authors)
    session.add_all(students)
    session.commit()


def give_me_book():
    nikita = session.query(Student).filter(Student.name == "Nik").first()
    vlad = session.query(Student).filter(Student.name == "Vlad").first()
    books_to_nik = (
        session.query(Book)
        .filter(Author.surname == "Толстой", Author.id == Book.author_id)
        .all()
    )
    books_to_vlad = session.query(Book).filter(Book.id.in_([1, 3, 4])).all()
    for book in books_to_nik:
        receiving_book = ReceivingBook()
        receiving_book.book = book
        receiving_book.student = nikita
        session.add(receiving_book)
    for book in books_to_vlad:
        receiving_book = ReceivingBook()
        receiving_book.book = book
        receiving_book.student = vlad
        session.add(receiving_book)

    session.commit()


@event.listens_for(Student, "before_insert")
def validate_phone_format(mapper, connection, target):
    if not re.match(r"^\+7\(9\d{2}\)-\d{3}-\d{2}-\d{2}$", target.phone):
        raise ValueError(
            "Invalid phone number format. It should be +7(9**) -*** - ** - **"
        )
