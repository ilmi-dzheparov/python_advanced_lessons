import random
import sqlite3
import datetime


number_of_people = 366

hobbies_by_day_dict = {
    "Monday": "футбол",
    "Tuesday": "хоккей",
    "Wednesday": "шахматы",
    "Thursday": "SUP сёрфинг",
    "Friday": "бокс",
    "Saturday": "Dota2",
    "Sunday": "шах-бокс",
}


def get_list_of_workers_having_sport_by_day(cursor: sqlite3.Cursor, date: str):
    date_object = datetime.datetime.strptime(date, "%Y-%m-%d")
    day_of_week = date_object.strftime("%A")
    worker_ids = []
    sport = hobbies_by_day_dict[day_of_week]
    cursor.execute(
        """
        SELECT id 
        FROM table_friendship_employees
        WHERE preferable_sport = ?
    """,
        (sport,),
    )
    worker_ids = [row[0] for row in cursor.fetchall()]
    return worker_ids


def get_list_of_workers_from_schedule_by_date(cursor: sqlite3.Cursor, date: str):
    worker_ids = []
    cursor.execute(
        """
        SELECT employee_id 
        FROM table_friendship_schedule
        WHERE date = ?
    """,
        (date,),
    )
    worker_ids = [row[0] for row in cursor.fetchall()]
    return worker_ids


update_table_friendship_schedule_sql = """
        UPDATE table_friendship_schedule
        SET employee_id = ?
        WHERE employee_id = ? AND date = ?
        """


def update_work_schedule(cursor: sqlite3.Cursor) -> None:
    date = datetime.datetime(year=2020, month=1, day=1)
    end_date = datetime.datetime(year=2020, month=12, day=31)

    while date <= end_date:
        work_date = date.strftime("%Y-%m-%d")
        workers_having_sport = get_list_of_workers_having_sport_by_day(
            cursor, work_date
        )
        workers_by_date = get_list_of_workers_from_schedule_by_date(cursor, work_date)
        workers_by_date_check = get_list_of_workers_from_schedule_by_date(cursor, work_date)
        for worker_id in workers_by_date:
            if worker_id in workers_having_sport:
                while True:
                    new_worker_id = random.randint(1, number_of_people)
                    if (
                        new_worker_id not in workers_having_sport
                        and new_worker_id not in workers_by_date_check
                    ):
                        workers_by_date_check.append(new_worker_id)
                        break
                cursor.execute(
                    update_table_friendship_schedule_sql, (new_worker_id, worker_id, work_date)
                )
        date += datetime.timedelta(days=1)

if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        update_work_schedule(cursor)
        conn.commit()
