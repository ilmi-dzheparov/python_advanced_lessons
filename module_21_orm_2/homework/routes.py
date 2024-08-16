import csv

from sqlalchemy import func, extract

from models import Book, Base, engine, session, ReceivingBook, Student, Author, insert_data, give_me_book

from flask import jsonify, abort, request, Blueprint
from datetime import datetime
import io


routes = Blueprint('routes', __name__)


@routes.before_request
def before_request_func():
    Base.metadata.create_all(bind=engine)
    check_exist = session.query(Author).all()

    if not check_exist:
        insert_data()
        give_me_book()


@routes.route("/books", methods=["GET"])
def get_all_books():
    """Получение всех книг в библиотеке"""
    books = session.query(Book).all()
    books_list = []
    for book in books:
        books_list.append(book.to_json())
    return jsonify(books_list=books_list), 200


@routes.route("/debtors", methods=["GET"])
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


@routes.route("/book/issue", methods=['POST'])
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


@routes.route("/book/return", methods=['POST'])
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
    received_book.date_of_return = datetime.now()
    book.count += 1
    session.commit()
    return jsonify({"message": "Book returned successfully"}), 200


@routes.route('/books/search', methods=['GET'])
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


@routes.route("/books/author/<int:id>", methods=["GET"])
def get_books_by_author(id: int):
    """Получить кол-во оставшихся в библиотеке книг по автору"""
    author = session.query(Author).filter(Author.id == id).one_or_none()
    if author is None:
        abort(404, description=f"Author with id={id} does not exist")
    count = session.query(func.sum(Book.count)).filter_by(author_id=id).scalar()
    return jsonify({"author_id": id, "total_books": count})


@routes.route("/books/student/<int:id>", methods=["GET"])
def get_books_by_student(id: int):
    """Получение книг в библиотеке, которые студенты не брал еще"""
    books_read_ids = session.query(ReceivingBook.book_id).filter_by(student_id=id).subquery()
    books_not_read = session.query(Book).filter(Book.id.notin_(books_read_ids)).all()
    student_books_list = []
    for book in books_not_read:
        student_books_list.append(book.to_json())
    return jsonify(books_list=student_books_list), 200


@routes.route("/books/avg", methods=["GET"])
def get_avg_count_of_books_taken():
    """Получить среднее кол-во книг, которые студенты брали в этом месяце"""
    count_students = session.query(func.count(func.distinct(ReceivingBook.student_id))).filter(
        extract('month', ReceivingBook.date_of_issue) == datetime.now().month
    ).scalar()
    if count_students == 0:
        abort(404, description="At this month no one has taken any book")
    count_books = session.query(func.count(ReceivingBook.date_of_issue)).filter(
        extract('month', ReceivingBook.date_of_issue) == datetime.now().month
    ).scalar()

    average_books_taken = count_books / count_students
    return jsonify({"Average count of taken books": average_books_taken}), 200


@routes.route("/book/popular", methods=["GET"])
def get_most_popular_book():
    """Получить самую популярную книгу среди студентов, у которых средний балл больше 4.0"""
    students_score_four = session.query(Student.id).filter(Student.average_score >= 4).subquery()
    book_counts = session.query(
        ReceivingBook.book_id, func.count(ReceivingBook.book_id).label('count')) \
        .filter(ReceivingBook.student_id.in_(students_score_four)) \
        .group_by(ReceivingBook.book_id) \
        .order_by(func.count(ReceivingBook.book_id).desc()).first()
    if not book_counts:
        return jsonify({"message": "No popular books found"}), 404
    most_popular_book_id = book_counts.book_id
    book_name = session.query(Book.name).filter_by(id=most_popular_book_id).scalar()
    return jsonify({"Most popular book": book_name, "book_id": most_popular_book_id}), 200


@routes.route("/students/top", methods=["GET"])
def get_most_readable_students():
    """Получить ТОП-10 самых читающих студентов в этом году"""
    students = session.query(ReceivingBook.student_id, func.count(ReceivingBook.student_id).label("count")) \
        .filter(extract('year', ReceivingBook.date_of_issue) == datetime.now().year) \
        .group_by(ReceivingBook.student_id).order_by(func.count(ReceivingBook.student_id).desc()).limit(10).all()

    student_list = []
    for student in students:
        student_list.append({"student_id": student.student_id, "count": student.count})

    return jsonify(top_students=student_list)


@routes.route("/students/upload", methods=["POST"])
def upload_students():
    """Принимает csv-файл с данными по студентам (разделитель ;)."""
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and file.filename.endswith(".csv"):
        # Чтение файла в формате StringIO
        file_stream = io.StringIO(file.stream.read().decode("UTF-8"), newline=None)

        # Чтение CSV с использованием csv.DictReader
        reader = csv.DictReader(file_stream, delimiter=";")

        data = []
        data = list(reader)
        for row in data:
            if row["scholarship"].lower() == 'true':
                row["scholarship"] = True
            else:
                row["scholarship"] = False
            row["average_score"] = float(row["average_score"])
        session.bulk_insert_mappings(Student, data)
        session.commit()
        return jsonify(new_students=data), 200