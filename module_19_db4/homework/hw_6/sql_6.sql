SELECT assignment_text, round(avg(grade), 2) AS av_grade FROM (
SELECT a_g.assisgnment_id, grade, a.assignment_text
FROM assignments_grades a_g
LEFT OUTER JOIN assignments a ON a_g.assisgnment_id = a.assisgnment_id)
where assignment_text LIKE 'выучить%' OR assignment_text LIKE 'прочитать%'
GROUP BY assisgnment_id
