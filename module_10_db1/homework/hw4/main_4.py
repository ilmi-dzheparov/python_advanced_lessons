import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("hw_4_database.db") as conn:
        """
        Определение количества человек с острова N, которые находятся за чертой бедности
        """
        query_1 = "SELECT COUNT(salary) FROM salaries WHERE salary < 5000"
        cursor = conn.cursor()
        cursor.execute(query_1)
        result_1 = cursor.fetchone()[0]
        print(f"{result_1} людей с острова N находятся за чертой бедности")

        """ 
        Определение средней зарплаты по острову N
        """
        query_2 = "SELECT ROUND(AVG(salary), 2) FROM salaries"
        cursor = conn.cursor()
        cursor.execute(query_2)
        result_2 = cursor.fetchone()[0]
        print(f"Cредняя зарплата по острову N: {result_2} гульденов")

        """ 
        Определение медианной зарплаты по острову N
        """
        total = "SELECT COUNT(salary) FROM salaries"
        media_num = f"CAST((({total}) / 2 - 1) AS int)"
        query_3 = f"SELECT salary FROM salaries order BY salary ASC LIMIT 1 OFFSET {media_num}"
        cursor.execute(query_3)
        result_3 = cursor.fetchone()[0]
        print(f"Медианная зарплатф по острову: {result_3} гульденов")

        """ 
        Определение числа социального неравенства F
        """
        top_10_num = f"CAST((0.1 * ({total})) AS int)"
        top_10 = f"SELECT salary FROM salaries ORDER BY salary DESC LIMIT {top_10_num}"
        top_10_sum = f"SELECT SUM(salary) FROM ({top_10})"
        down_90_num = f"({total}) - ({top_10_num})"
        down_90 = (
            f"SELECT salary FROM salaries ORDER BY salary ASC LIMIT ({down_90_num})"
        )
        down_90_sum = f"SELECT SUM(salary) FROM ({down_90})"
        query_4 = f"SELECT (100 * ROUND((CAST(({top_10_sum}) AS float) / ({down_90_sum})), 2))"
        cursor.execute(query_4)
        result_4 = cursor.fetchone()[0]
        print(f"Число социального неравенства F: {result_4} %")
