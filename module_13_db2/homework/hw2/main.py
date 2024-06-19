import sqlite3
import csv

delete_request = """
    DELETE FROM table_fees
    WHERE timestamp = ? AND truck_number = ?
"""


def delete_wrong_fees(cursor: sqlite3.Cursor, wrong_fees_file: str) -> None:
    with open(wrong_fees_file, newline="") as csvfile:
        fines = csv.DictReader(csvfile, delimiter=",")
        for row in fines:
            cursor.execute(delete_request, (row["timestamp"], row["car_number"]))


if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        delete_wrong_fees(cursor, "../wrong_fees.csv")
        conn.commit()
