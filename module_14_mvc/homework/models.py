import sqlite3
from typing import Any, Optional, List

DATA: List[dict] = [
    {"id": 0, "title": "A Byte of Python", "author": "Swaroop C. H.", "count_of_views": 0},
    {"id": 1, "title": "Moby-Dick; or, The Whale", "author": "Herman Melville", "count_of_views": 0},
    {"id": 3, "title": "War and Peace", "author": "Leo Tolstoy", "count_of_views": 0},
]


class Book:

    def __init__(self, id: int, title: str, author: str, count_of_views: int) -> None:
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.count_of_views: int = count_of_views

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


def init_db(initial_records: List[dict]) -> None:
    with sqlite3.connect("table_books.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_books'; 
            """
        )
        exists: Optional[tuple[str,]] = cursor.fetchone()
        # now in `exist` we have tuple with table name if table really exists in DB
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `table_books` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT, 
                    author TEXT,
                    count_of_views INTEGER DEFAULT 0
                    )
                """
            )
            cursor.executemany(
                """
                INSERT INTO `table_books`
                (title, author, count_of_views) VALUES (?, ?, ?)
                """,
                [(item["title"], item["author"], item["count_of_views"]) for item in initial_records],
            )


def increase_count_views_all_books():
    with sqlite3.connect("table_books.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE `table_books`
            SET count_of_views = count_of_views+1
            """
        )


def increase_count_views_of_book_by_id(id: int):
    with sqlite3.connect("table_books.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE `table_books`
            SET count_of_views = count_of_views+1
            WHERE id = ?
            """, (id,)
        )

def get_all_books() -> List[Book]:
    with sqlite3.connect("table_books.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * from `table_books`
            """
        )
        return [Book(*row) for row in cursor.fetchall()]


def add_book(title: str, author: str):
    with sqlite3.connect("table_books.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
                INSERT INTO `table_books`
                (title, author) VALUES (?, ?)
                """,
            (title, author),
        )


def get_books_by_author(author: str) -> List[Book]:
    with sqlite3.connect("table_books.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * from `table_books`
            WHERE author = ?
            """,
            (author,),
        )
        return [Book(*row) for row in cursor.fetchall()]


def get_book_by_id(id: int) -> Book:
    with sqlite3.connect("table_books.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * from `table_books`
            WHERE id = ?
            """,
            (id,),
        )
        row = cursor.fetchone()
        print(row)
        if row:
            return Book(*row)
        else:
            return None