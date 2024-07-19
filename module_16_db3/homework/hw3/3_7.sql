SELECT DISTINCT
product.model AS model,
COALESCE(pc.price, printer.price, laptop.price) AS price
FROM product
LEFT OUTER JOIN pc on product.model = pc.model
LEFT OUTER JOIN printer on product.model = printer.model
LEFT OUTER JOIN laptop on product.model = laptop.model
WHERE product.maker = 'B'