### Перед выполнением задания запустите файл generate_practice_and_homework_db.py!

Дирекция школы решила наградить лучших учеников грамотами, но вот беда, в принтере картриджа хватит всего на 10 бланков. Выберите 10 лучших учеников с лучшими оценками в сроеднем. Не забудьте отсортировать список в низходящем порядке

SELECT s.student_id AS s_id, s.full_name AS student, avg(grade) AS av_grade
 FROM assignments_grades t 
 INNER JOIN students s ON s.student_id = t.student_id
 GROUP BY s_id
 ORDER BY av_grade DESC
 LIMIT 10