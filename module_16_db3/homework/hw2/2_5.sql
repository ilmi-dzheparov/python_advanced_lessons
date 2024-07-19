WITH customer_manager AS (
    SELECT
        c.customer_id AS customer_id,
        c.full_name AS customer_name,
        c.city AS city,
        o.manager_id AS manager_id
    FROM "order" o
    INNER JOIN customer c ON o.customer_id = c.customer_id
),
pairs AS (
    SELECT
        cm1.customer_name AS customer_name_1,
        cm2.customer_name AS customer_name_2
    FROM customer_manager cm1
    INNER JOIN customer_manager cm2
        ON cm1.city = cm2.city
        AND cm1.manager_id = cm2.manager_id
        AND cm1.customer_id < cm2.customer_id
)
SELECT DISTINCT
    customer_name_1,
    customer_name_2
FROM pairs
ORDER BY customer_name_1, customer_name_2;