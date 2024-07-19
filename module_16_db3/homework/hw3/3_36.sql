SELECT DISTINCT Outcomes.ship AS name
FROM Outcomes
INNER JOIN Classes
ON Outcomes.ship = Classes.class
UNION
SELECT DISTINCT Ships.name AS name
FROM Ships
INNER JOIN Classes
ON Ships.name = Classes.class