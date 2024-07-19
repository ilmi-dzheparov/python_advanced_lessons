SELECT DISTINCT
product.maker AS Maker,
laptop.speed AS speed
FROM product
LEFT OUTER JOIN laptop
ON product.model = laptop.model
WHERE laptop.hd >= 10
