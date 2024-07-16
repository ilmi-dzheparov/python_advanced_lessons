import sqlite3
from datetime import datetime
from typing import Any, Optional, List
from decimal import Decimal

from flask import jsonify


class Hotel:
    def __init__(
        self,
        id: int,
        floor: int,
        beds: int,
        getNum: int,
        price: Decimal,
        is_booked: bool = False,
        checkInDate: Optional[datetime] = None,
        checkOutDate: Optional[datetime] = None,
        firstName: Optional[str] = None,
        lastName: Optional[str] = None,
    ):
        self.id: int = id
        self.floor: int = floor
        self.beds: int = beds
        self.guest_num: int = getNum
        self.price: Decimal = price
        self.is_booked: bool = is_booked
        self.checkInDate: Optional[datetime] = checkInDate
        self.checkOutDate: Optional[datetime] = checkOutDate
        self.firstName: Optional[str] = firstName
        self.lastName: Optional[str] = lastName

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


def init_db() -> None:
    with sqlite3.connect("table_hotel.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_hotel'
            """
        )
        exists: Optional[tuple(str)] = cursor.fetchone()
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE 'table_hotel' (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    floor INTEGER,
                    beds INTEGER,
                    guest_num INTEGER,
                    price NUMERIC,
                    is_booked INTEGER DEFAULT 0,
                    check_in_date TEXT DEFAULT None,
                    check_out_date TEXT DEFAULT None,
                    first_name TEXT DEFAULT None,
                    last_name TEXT DEFAULT None
                    )
                """
            )


def add_room(floor: int, beds: int, guest_num: int, price: Decimal):
    with sqlite3.connect("table_hotel.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO `table_hotel`
            (floor, beds, guest_num, price) VALUES (?, ?, ?, ?)
            """,
            (floor, beds, guest_num, price),
        )
        conn.commit()


def get_rooms():
    with sqlite3.connect("table_hotel.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM `table_hotel`
            WHERE is_booked = 0
            """
        )
        return [Hotel(*row) for row in cursor.fetchall()]


def book_room(
    room_id: int,
    first_name: str,
    last_name: str,
    check_in_date: datetime,
    check_out_date: datetime,
):
    with sqlite3.connect("table_hotel.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE table_hotel
            SET is_booked = ?, first_name = ?, last_name = ?, check_in_date = ?, check_out_date = ?
            WHERE id = ? AND is_booked = 0
            """,
            (True, first_name, last_name, check_in_date, check_out_date, room_id),
        )
        print("vbhhjsdbvhjv")
        if cursor.rowcount == 0:
            return jsonify({"error": "Room is already booked"}), 409
        conn.commit()
        return jsonify({"message": "Room is succesfully booked"}), 200
