SELECT group_id, round(avg(num), 2) as average_num, min(num) AS min_num, max(num) AS max_num
FROM (
SELECT group_id, assisgnment_id, count(*) as num from(
SELECT * FROM (
SELECT a.assisgnment_id, t.group_id, a.date AS date, t.due_date AS due_date from assignments_grades a
INNER JOIN assignments t
ON a.assisgnment_id = t.assisgnment_id)
WHERE date > due_date)
GROUP BY assisgnment_id)
GROUP BY group_id
ORDER BY group_id