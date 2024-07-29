import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

DATA = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 1},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 2},
    {'id': 3, 'title': 'War and Peace', 'author': 3},
]

DATA_AUTHOR = [
    {'id': 0, 'first_name': 'C. H.', 'second_name': 'Swaroop', 'middle_name': None},
    {'id': 1, 'first_name': 'Herman', 'second_name': 'Melville', 'middle_name': None},
    {'id': 3, 'first_name': 'Leo', 'second_name': 'Tolstoy', 'middle_name': 'Nikolaevich'},
]



DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHORS_TABLE_NAME = 'authors'


@dataclass
class Book:
    title: str
    author: "Author"
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)

@dataclass
class Author:
    first_name: str
    second_name: str
    middle_name: Optional[str] = None
    id: Optional[int] = None
    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


def init_db(initial_records_authors: List[Dict], initial_records: List[Dict]) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(
            f"""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='{AUTHORS_TABLE_NAME}';
            """
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.executescript(
                f"""
                CREATE TABLE `{AUTHORS_TABLE_NAME}`(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    first_name TEXT,
                    second_name TEXT,
                    middle_name TEXT
                );
                """
            )
            cursor.executemany(
                f"""
                INSERT INTO `{AUTHORS_TABLE_NAME}`
                (first_name, second_name, middle_name) VALUES (?, ?, ?)
                """,
                [
                    (item['first_name'], item['second_name'], item['middle_name'])
                    for item in initial_records_authors
                ]
            )
        cursor.execute(
            f"""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='{BOOKS_TABLE_NAME}';
            """
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.executescript(
                f"""
                CREATE TABLE `{BOOKS_TABLE_NAME}`(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT,
                    author INTEGER NOT NULL REFERENCES {AUTHORS_TABLE_NAME}(id) ON DELETE CASCADE
            
                );
                """
            )
            cursor.executemany(
            f"""
                INSERT INTO `{BOOKS_TABLE_NAME}`
                (title, author) VALUES (?, ?)
                """,
            [
                (item['title'], item['author'])
                for item in initial_records
            ]
            )


def _get_book_obj_from_row(row: tuple):
    author = get_author_by_id(row[2])
    return Book(id=row[0], title=row[1], author=author)


def _get_author_obj_from_row(row: tuple) -> Author:
    return Author(id=row[0], first_name=row[1], second_name=row[2], middle_name=row[3])


def get_all_books() -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{BOOKS_TABLE_NAME}`')
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]


def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{BOOKS_TABLE_NAME}` 
            (title, author) VALUES (?, ?)
            """,
            (book.title, book.author)
        )
        book.id = cursor.lastrowid
        return book


def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE id = ?
            """,
            (book_id,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def update_book_by_id(book: Book) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE {BOOKS_TABLE_NAME}
            SET title = ?, author = ?
            WHERE id = ?
            """,
            (book.title, book.author, book.id)
        )
        conn.commit()


def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {BOOKS_TABLE_NAME}
            WHERE id = ?
            """,
            (book_id,)
        )
        conn.commit()


def get_book_by_title(book_title: str, book_id: Optional[int]) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        if book_id is None:
            cursor.execute(
                f"""
                SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE title = ?
                """,
                (book_title,)
            )
        else:
            cursor.execute(
                f"""
                SELECT * FROM `{BOOKS_TABLE_NAME}` 
                WHERE title = ? AND id != ?
                """,
                (book_title, book_id)
            )

        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def get_author_by_id(author_id: int) -> Author:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{AUTHORS_TABLE_NAME}` WHERE id=?
            """, (author_id, )
        )
        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)


def get_author_by_fullname(first_name: str, second_name: str) -> Optional[Author]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{AUTHORS_TABLE_NAME}` 
            WHERE first_name = ? AND second_name = ?
            """, (first_name, second_name)
        )
        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)


def get_books_by_author_id(author_id: int) -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE author = ?
            """, (author_id,)
        )
        books = cursor.fetchall()
        print(books)
        if books:
            print([_get_book_obj_from_row(row) for row in books])
            return [_get_book_obj_from_row(row) for row in books]


def get_all_authors():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{AUTHORS_TABLE_NAME}` 
            """
        )
        authors = cursor.fetchall()
        return [_get_author_obj_from_row(row) for row in authors]


def add_author(author: Author) -> Author:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{AUTHORS_TABLE_NAME}` 
            (first_name, second_name, middle_name) VALUES (?, ?, ?)
            """,
            (author.first_name, author.second_name, author.middle_name)
        )
        author.id = cursor.lastrowid
        return author


def delete_author_by_id(author_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(
            f"""
            DELETE FROM {AUTHORS_TABLE_NAME}
            WHERE id = ?
            """,
            (author_id,)
        )
        conn.commit()

def update_author_by_id(middle_name: str, book_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE {AUTHORS_TABLE_NAME}
            SET middle_name = ?
            WHERE id = ?
            """,
            (middle_name, book_id)
        )
        conn.commit()