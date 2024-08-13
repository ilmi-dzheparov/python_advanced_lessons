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