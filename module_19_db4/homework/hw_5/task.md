### Перед выполнением задания запустите файл generate_practice_and_homework_db.py!

Узнайте все про группы! Количество учеников, средняя оценка, сколько человек не сдали работы и сколько опоздали со задачей работы. И сколько в каждой группе было повторных попыток сдать работу.


WITH table_group_student_grade AS (
SELECT a.group_id, student_id, grade, "date", a.due_date
FROM assignments_grades a_g
LEFT OUTER JOIN assignments a ON a_g.assisgnment_id = a.assisgnment_id),
students_number AS (
SELECT group_id, count(student_id) AS student_num
FROM students
GROUP BY group_id),
average_grade AS (
SELECT group_id, round(avg(grade), 2) AS av_grade
FROM table_group_student_grade
GROUP BY group_id),
count_of_stud_having_0 AS (
SELECT group_id, count(*) AS having_0 
FROM table_group_student_grade
WHERE grade = 0
GROUP BY group_id),
count_of_stud_over_date AS (
SELECT group_id, count(*) AS over_date 
FROM table_group_student_grade
WHERE "date" > due_date
GROUP BY group_id)

SELECT s_n.group_id, student_num, av_grade, having_0, over_date  FROM students_number s_n
LEFT OUTER JOIN average_grade a_g ON s_n.group_id = a_g.group_id
LEFT OUTER JOIN count_of_stud_having_0 c ON s_n.group_id = c.group_id
LEFT OUTER JOIN count_of_stud_over_date o ON s_n.group_id = o.group_id