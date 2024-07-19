SELECT
    o.order_no AS order_no,
    m.full_name AS manager_full_name,
    c.full_name AS customer_full_name
FROM "order" o
LEFT JOIN manager m ON o.manager_id = m.manager_id
LEFT JOIN customer c ON o.customer_id = c.customer_id
WHERE c.city != m.city
