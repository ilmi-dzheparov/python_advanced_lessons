import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("hw_3_database.db") as conn:
        """
        Определение количества записей в таблицах
        """
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM `table_1`")
        result_1 = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) FROM `table_2`")
        result_2 = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) FROM `table_3`")
        result_3 = cursor.fetchone()
        print(
            f"Длина table_1: {result_1[0]},\n"
            f"Длина table_2: {result_2[0]},\n"
            f"Длина table_3: {result_3[0]}"
        )

        """
        Определение количества уникальных записей в таблице 1
        """
        cursor.execute("SELECT COUNT(DISTINCT `id`) FROM `table_1`")
        result_4 = cursor.fetchone()
        print(f"Количества уникальных записей в table_1: {result_4[0]}")

        """
        Определение количества пересечений записей в таблицах
        """

        # cursor.execute("SELECT * FROM `table_1` INTERSECT SELECT * FROM `table_2`")
        cursor.execute(
            "SELECT COUNT(*) FROM table_1 INNER JOIN table_2 "
            "ON table_1.id=table_2.id "
            "AND table_1.value=table_2.value"
        )
        result_5 = cursor.fetchone()
        # print(len(result_5))
        print(f"{result_5[0]} записей из таблицы table_1 встречаются в table_2")

        cursor.execute(
            "SELECT * FROM `table_1` INTERSECT SELECT * FROM `table_2`INTERSECT SELECT * FROM `table_3`"
        )
        result_6 = cursor.fetchall()
        print(f"{len(result_6)} записей из таблицы table_1 встречаются в table_2 и table_3")

