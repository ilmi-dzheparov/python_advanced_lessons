select
	o.order_no AS order_no,
    c.full_name AS customer_full_name,
    m.full_name AS manager_full_name,
    o.purchase_amount AS purchase_amount,
	o.date AS date
FROM "order" o
INNER JOIN customer c ON o.customer_id = c.customer_id
INNER JOIN manager m ON o.manager_id = m.manager_id
