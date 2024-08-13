### Перед выполнением задания запустите файл generate_practice_and_homework_db.py!

Используя вложенные запросы найдите всех учеников того преподавателя, кто задает самые простые задания (те задания, где средний бал самый высокий)

* задание со звездочкой: напишите этот же запрос с использованием одного из join

 SELECT DISTINCT full_name FROM students
 WHERE group_id IN (
 SELECT group_id FROM assignments
 WHERE teacher_id IN (
 SELECT teacher_id FROM (
 SELECT teacher_id, min(av_grade_by_teacher)
 FROM (
 SELECT teacher_id, avg(av_grade) AS av_grade_by_teacher
FROM ( 
 SELECT teacher_id,  av_grade
 FROM assignments
 INNER JOIN 
 (SELECT assisgnment_id AS a_id, avg(grade) AS av_grade 
 FROM assignments_grades 
 GROUP BY a_id)
 ON assisgnment_id = a_id)
 GROUP BY teacher_id))))
