from flask import Flask, render_template, request, redirect
from typing import List

from models import (
    init_db,
    get_all_books,
    DATA,
    add_book,
    get_books_by_author,
    get_book_by_id,
    increase_count_views_all_books,
    increase_count_views_of_book_by_id,
)
from forms import BookForm


app: Flask = Flask(__name__)
app.secret_key = "qwerty"


def _get_html_table_for_books(books: List[dict]) -> str:
    table = """
<table>
    <thead>
    <tr>
        <th>ID</th>
        <th>Title</th>
        <th>Author</th>
        <th>Views</th>
    </tr>
    </thead>
    <tbody>
        {books_rows}
    </tbody>
</table>
"""
    rows: str = ""
    for book in books:
        rows += "<tr><td>{id}</td><td>{title}</td><td>{author}</td><td>{views}</td></tr>".format(
            id=book["id"],
            title=book["title"],
            author=book["author"],
            views=book["count_of_views"],
        )
    return table.format(books_rows=rows)


@app.route("/books")
def all_books() -> str:
    increase_count_views_all_books()
    return render_template(
        "index.html",
        books=get_all_books(),
    )


@app.route("/books/form", methods=["GET", "POST"])
def get_books_form() -> str:
    form = BookForm()
    if request.method == "GET":
        return render_template("add_book.html", form=form)
    if request.method == "POST":
        add_book(request.form["book_title"], request.form["author_name"])
        return redirect("/books")
    return render_template("add_book.html", form=form)


@app.route("/books/author")
def books_by_author():
    author_name = request.args.get("author_name")
    if author_name:
        books = get_books_by_author(author_name)
        return render_template("books_by_author.html", books=books, author=author_name)
    return "Error: Author name not provided", 400


@app.route("/books/<int:id>")
def books_detail(id):
    book = get_book_by_id(id)
    increase_count_views_of_book_by_id(id)
    return render_template("book_by_id.html", book=book, id=id)


if __name__ == "__main__":
    init_db(DATA)
    app.run(debug=True)
