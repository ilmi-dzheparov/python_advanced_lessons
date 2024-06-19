import datetime
import sqlite3

check_bird_seen_sql = """
    SELECT EXISTS (
        SELECT 1  
        FROM register_of_birds
        WHERE bird_name=?)
"""

log_bird_sql = """
    INSERT INTO register_of_birds (bird_name, date)
    VALUES (?, ?)
"""

create_table_sql = """
    CREATE TABLE IF NOT EXISTS register_of_birds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bird_name TEXT NOT NULL,
        date TEXT NOT NULL
    )
"""


def create_homework_table(cursor: sqlite3.Cursor) -> None:
    cursor.execute(create_table_sql)


def check_if_such_bird_already_seen(cursor: sqlite3.Cursor, bird_name: str) -> bool:
    cursor.execute(check_bird_seen_sql, (bird_name,))
    if cursor.fetchone()[0] == 1:
        return True
    return False


def log_bird(
    cursor: sqlite3.Cursor,
    bird_name: str,
    date_time: str,
) -> None:
    if not check_if_such_bird_already_seen(cursor, bird_name):
        cursor.execute(log_bird_sql, (bird_name, date_time))
        cursor.connection.commit()


if __name__ == "__main__":
    print("Программа помощи ЮНатам v0.1")
    name: str = input("Пожалуйста введите имя птицы\n> ")
    count_str: str = input("Сколько птиц вы увидели?\n> ")
    count: int = int(count_str)
    right_now: str = datetime.datetime.utcnow().isoformat()

    with sqlite3.connect("../homework.db") as connection:
        cursor: sqlite3.Cursor = connection.cursor()

        create_homework_table(cursor)

        if check_if_such_bird_already_seen(cursor, name):
            print("Такую птицу мы уже наблюдали!")

        log_bird(cursor, name, right_now)
