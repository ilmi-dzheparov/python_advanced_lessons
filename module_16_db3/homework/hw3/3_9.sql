SELECT DISTINCT
product.maker AS maker
FROM product
LEFT JOIN pc ON product.model = pc.model
WHERE pc.speed >= 450
