SELECT s.student_id AS s_id, s.full_name AS student, avg(grade) AS av_grade
 FROM assignments_grades t
 INNER JOIN students s ON s.student_id = t.student_id
 GROUP BY s_id
 ORDER BY av_grade DESC
 LIMIT 10