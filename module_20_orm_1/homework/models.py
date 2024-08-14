import datetime
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
