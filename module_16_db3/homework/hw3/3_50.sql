WITH ship_class AS (SELECT DISTINCT
Ships.name AS name,
Classes.class AS class
FROM Ships
LEFT JOIN Classes ON Ships.class = Classes.class)
SELECT DISTINCT
Outcomes.battle AS battle
FROM Outcomes
INNER JOIN ship_class ON
Outcomes.ship = ship_class.name
WHERE ship_class.class = 'Kongo'
