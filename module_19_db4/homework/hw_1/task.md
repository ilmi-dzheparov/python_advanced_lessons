### Перед выполнением задания запустите файл generate_practice_and_homework_db.py!

Узнайте кто из преподавателей задает самые сложные задания. Иначе говоря задания какого преподавателя получают в среднем самые худшие оценки

 SELECT t_id, min(av_grade)
 FROM (
 SELECT t.assisgnment_id AS a_id, avg(grade) AS av_grade, a.teacher_id AS t_id 
 FROM assignments_grades t 
 INNER JOIN assignments a ON a.assisgnment_id = t.assisgnment_id
 GROUP BY a_id
 ORDER BY av_grade)