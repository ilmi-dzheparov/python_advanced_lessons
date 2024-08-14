from models import Book, Base, engine, session, ReceivingBook, Student

from flask import jsonify, abort, request, Blueprint


routes = Blueprint('routes', __name__)


@routes.before_request
def before_request_func():
    Base.metadata.create_all(bind=engine)


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
    session.delete(received_book)
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
