### Перед выполнением задания запустите файл generate_practice_and_homework_db.py!

Используя подзапросы выведите среднюю оценку тех заданий, где ученикам нужно было что-то прочитать и выучить


SELECT assignment_text, round(avg(grade), 2) AS av_grade FROM (
SELECT a_g.assisgnment_id, grade, a.assignment_text 
FROM assignments_grades a_g
LEFT OUTER JOIN assignments a ON a_g.assisgnment_id = a.assisgnment_id)
where assignment_text LIKE 'выучить%' OR assignment_text LIKE 'прочитать%'
GROUP BY assisgnment_id