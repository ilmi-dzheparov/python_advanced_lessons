import sqlite3
import random

generate_table_uefa_commands_sql = """
DROP TABLE IF EXISTS `uefa_commands`;

CREATE TABLE `uefa_commands` (
    command_number INTEGER PRIMARY KEY,
    command_name VARCHAR(255) NOT NULL,
    command_country VARCHAR(255) NOT NULL,
    command_level VARCHAR(255) NOT NULL
);
"""

generate_table_uefa_draw_sql = """
DROP TABLE IF EXISTS `uefa_draw`;

CREATE TABLE `uefa_draw` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    command_number numeric NOT NULL UNIQUE,
    group_number numeric NOT NULL
);
"""

insert_data_in_table_uefa_draw_sql = """
    INSERT INTO `uefa_draw`
    (command_number, group_number) VALUES (?, ?)
"""

insert_data_in_table_uefa_commands_sql = """
    INSERT INTO `uefa_commands`
    (command_number, command_name, command_country, command_level) 
    VALUES (?, ?, ?, ?)
"""

countries = """Австрия, Бельгия, Болгария, Хорватия, Кипр, Чешская Республика, Дания, Эстония, Финляндия, Франция,
Германия, Греция, Венгрия, Ирландия, Италия, Латвия, Литва, Люксембург, Мальта, Нидерланды, Польша, Португалия, Румыния,
Словакия, Словения, Испания, Швеция, Албания, Черногория, Северная Македония, Турция, Сербия
""".split(
    ", "
)

command_names = """Омерзительная семерка, Тупые козырьки, Бесславные улитки, Некрепкие орешки, Халат Лебовски, Мы есть Грут, Йагупоп 77-ой,
Два капитана, Сами знаете кто, Дементоры, Без Тимура, Палата номер 6, горе от ума, Дюжина бровей, Аристократы и дегенераты,
Тупой и еще тупее, Союз спасения, Они сражались за логику, Вассервуман, Я же говорила, Змеиный коллектив, Баба Яга и команда,
Цветущий вулкан, Мы с Тамарой, Отличницы, Девичья фамилия, Косички, В джазе только девушки, Пончики не проигрывают, Весна,
Маленькие леди, Волнушки, Офисные феи, Капибарыня, Ученье Светы, Зато красивые, Брокколи, Второе дыхание, 2х2, Профитроли,
Коллеги, Береста, Моя любимая команда, Котангенс, Борщ, Манул, Ура, Комбо, Фантазеры, Команда Х, Черный ящик, Знак бесконечности,
Формальдегид, Не вопрос, Пять плюс один, Лаванда, Old School, Команда телезрителей, Точка кипения
""".split(
    ", "
)


def insert_command_in_table(cursor: sqlite3.Cursor, command_number: int, level: str):
    command_name = random.choice(command_names)
    command_names.remove(command_name)
    command_country = random.choice(countries)
    cursor.execute(
        insert_data_in_table_uefa_commands_sql,
        (command_number, command_name, command_country, level),
    )


def generate_test_data(cursor: sqlite3.Cursor, number_of_groups: int) -> None:
    group_numbers_list = [i + 1 for i in range(number_of_groups)]

    command_number = 1
    for _ in range(number_of_groups):
        group_number = random.choice(group_numbers_list)
        group_numbers_list.remove(group_number)

        insert_command_in_table(cursor, command_number, "сильная")

        cursor.execute(
            insert_data_in_table_uefa_draw_sql, (command_number, group_number)
        )

        command_number += 1
        insert_command_in_table(cursor, command_number, "средняя")

        cursor.execute(
            insert_data_in_table_uefa_draw_sql, (command_number, group_number)
        )

        command_number += 1
        insert_command_in_table(cursor, command_number, "средняя")

        cursor.execute(
            insert_data_in_table_uefa_draw_sql, (command_number, group_number)
        )

        command_number += 1
        insert_command_in_table(cursor, command_number, "слабая")

        cursor.execute(
            insert_data_in_table_uefa_draw_sql, (command_number, group_number)
        )
        command_number += 1



if __name__ == "__main__":
    number_of_groups: int = int(input("Введите количество групп (от 4 до 16): "))
    with sqlite3.connect("../homework.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.executescript(generate_table_uefa_draw_sql)
        cursor.executescript(generate_table_uefa_commands_sql)
        generate_test_data(cursor, number_of_groups)
        conn.commit()
