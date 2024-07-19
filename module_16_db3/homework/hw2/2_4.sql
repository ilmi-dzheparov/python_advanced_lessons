SELECT
    c.full_name AS customer_full_name,
    o.order_no AS order_no
FROM "order" o
LEFT JOIN customer c ON o.customer_id = c.customer_id
WHERE o.manager_id IS NULL