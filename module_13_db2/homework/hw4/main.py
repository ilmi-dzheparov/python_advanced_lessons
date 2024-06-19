import sqlite3


EFFECTIVE_MANAGER_SALARY = 100000

get_salary_sql = """
    SELECT salary
    FROM table_effective_manager
    WHERE name = ?
"""

delete_worker_sql = """
    DELETE FROM table_effective_manager
    WHERE name = ?
"""

update_worker_salary = """
    UPDATE table_effective_manager
    SET salary = ?
    WHERE name = ?
"""

def ivan_sovin_the_most_effective(
        cursor: sqlite3.Cursor,
        name: str,
) -> None:
    cursor.execute(get_salary_sql, (name,))
    worker_old_salary = cursor.fetchone()[0]
    worker_new_salary = worker_old_salary * 1.1
    if worker_new_salary < EFFECTIVE_MANAGER_SALARY:
        cursor.execute(update_worker_salary, (worker_new_salary, name))
    elif name != 'Иван Совин':
        cursor.execute(delete_worker_sql, (name,))

if __name__ == '__main__':
    name: str = input('Введите имя сотрудника: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        ivan_sovin_the_most_effective(cursor, name)
        conn.commit()
